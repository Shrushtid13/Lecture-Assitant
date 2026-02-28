
Lumina AI is an end-to-end lecture intelligence platform. Upload any audio or video recording of a lecture and Lumina AI will automatically transcribe it, extract key topics, generate structured summaries, identify keywords, and build a vector store — all powered by a multi-node LangGraph pipeline and Mistral AI.
Once notes are generated, an interactive Q&A chat lets you ask anything about the lecture, with answers grounded in the actual content via retrieval-augmented generation (RAG). Notes can be exported as a formatted .docx file.


<img width="1892" height="864" alt="Screenshot 2026-02-28 152015" src="https://github.com/user-attachments/assets/a9ae94cd-e29a-47fa-abd4-274fd007323d" />


Features

Automatic Transcription — Supports .wav, .mp3, .mp4, .ogg, .m4a via ASR node .
Intelligent Note Generation — Multi-stage LangGraph pipeline: transcription → relevance filtering → normalization → chunking → topic detection → summarization → keyword extraction → validation → structuring .
Interactive Q&A Chat — RAG-powered chat grounded in your lecture content using ChromaDB and Mistral embeddings .
DOCX Export — Download structured notes as a formatted Word document .
FastAPI Backend — Clean REST API separating backend logic from the Streamlit frontend .
Auto-Start Backend — Streamlit app automatically launches the FastAPI server on startup .
Dark Blue UI Theme — Custom professional dark interface built with Streamlit .

<img width="900" height="767" alt="ChatGPT Image Feb 28, 2026, 09_18_35 PM" src="https://github.com/user-attachments/assets/1d5a47cb-9382-4db9-ba4e-af23f75d150c" />


Endpoints with Description

GET /health – Health check .
POST /process-lecture – Upload audio/video, run pipeline, return notes .
POST /chat – Ask a question about a processed lecture .
GET /download-notes/{lecture_id} – Download notes as .docx .
GET /sessions – List active lecture sessions .

Running the App

Option 1 — Single command (recommended)
The Streamlit app automatically starts the FastAPI backend in the background:
streamlit run app.py

The app will:

Detect that the backend is not running .
Launch main.py as a background process .
Wait for the backend to become available .
Open the Streamlit UI at http://localhost:8501 .

Option 2 -  Run separately
Terminal 1 — Start the backend
python main.py

Terminal 2 — Start the frontend
streamlit run app.py

Usage

Upload a lecture file (.wav, .mp3, .mp4, .ogg, .m4a) .
Click Generate Notes — the pipeline transcribes and processes the lecture .
View structured notes with topics, summaries, and keywords .
Click Download Notes to export as a .docx file .
Use the Q&A Chat to ask questions about the lecture content .





