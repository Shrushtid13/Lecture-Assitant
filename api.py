import os
import tempfile
import uuid
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graphs.notes_graph import build_note_graph
from graphs.qa_graph import build_qa_graph
from llm_provider import get_main_llm
from embeddings_provider import get_embeddings
from vector_store import build_vector_store
from formatter import DocumentFormatter


# ── App Init ──────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Lumina AI API",
    description="Backend API for Lumina AI — Lecture Intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── In-Memory Session Store ───────────────────────────────────────────────────
# Holds retriever + notes per lecture_id so they survive across requests
# within the same server session.

sessions: Dict[str, Dict[str, Any]] = {}

# Build graphs once at startup (expensive — reuse across requests)
note_graph = build_note_graph()
qa_graph   = build_qa_graph()


# ── Request / Response Schemas ────────────────────────────────────────────────

class NoteSection(BaseModel):
    topic: str
    summary: str
    keywords: List[str]

class ProcessResponse(BaseModel):
    lecture_id: str
    notes: List[NoteSection]

class ChatRequest(BaseModel):
    lecture_id: str
    question: str
    chat_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    answer: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Lumina AI API is running"}


@app.post("/process-lecture", response_model=ProcessResponse)
async def process_lecture(file: UploadFile = File(...)):
    """
    Accept an audio/video lecture file, run the notes pipeline,
    build a vector store, and return structured notes.
    """
    allowed = {"wav", "mp3", "mp4", "ogg", "m4a"}
    ext = file.filename.split(".")[-1].lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{ext}'. Allowed: {allowed}"
        )

    # Save upload to a temp file so the ASR node can read it from disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        # Run the notes LangGraph pipeline
        result = note_graph.invoke({
            "audio_path": temp_path,
            "llm": get_main_llm()
        })
    finally:
        os.unlink(temp_path)   # clean up temp file

    structured_notes: List[Dict] = result["structured_notes"]

    # Build / persist the Chroma vector store for this lecture
    lecture_id = file.filename.replace(".", "_").replace(" ", "_") + "_" + uuid.uuid4().hex[:6]
    embeddings  = get_embeddings()
    vector_store = build_vector_store(structured_notes, embeddings, lecture_id=lecture_id)

    # Cache retriever + notes in memory for subsequent chat/download calls
    sessions[lecture_id] = {
        "notes": structured_notes,
        "retriever": vector_store.as_retriever(search_kwargs={"k": 4})
    }

    return ProcessResponse(
        lecture_id=lecture_id,
        notes=[NoteSection(**n) for n in structured_notes]
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Answer a question about a previously processed lecture.
    """
    session = sessions.get(request.lecture_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Lecture '{request.lecture_id}' not found. Please process it first via /process-lecture."
        )

    result = qa_graph.invoke({
        "question": request.question,
        "retriever": session["retriever"],
        "llm": get_main_llm()
    })

    return ChatResponse(answer=result["answer"])


@app.get("/download-notes/{lecture_id}")
def download_notes(lecture_id: str):
    """
    Generate and return a DOCX file of the structured notes for a lecture.
    """
    session = sessions.get(lecture_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Lecture '{lecture_id}' not found. Please process it first via /process-lecture."
        )

    formatter   = DocumentFormatter()
    file_buffer = formatter.generate_docx(session["notes"])

    return StreamingResponse(
        file_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=Lecture_Notes_{lecture_id}.docx"}
    )


@app.get("/sessions")
def list_sessions():
    """
    List all active lecture sessions (useful for debugging).
    """
    return {
        "active_sessions": list(sessions.keys()),
        "count": len(sessions)
    }