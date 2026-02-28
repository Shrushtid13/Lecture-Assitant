
Lumina AI is an end-to-end lecture intelligence platform. Upload any audio or video recording of a lecture and Lumina AI will automatically transcribe it, extract key topics, generate structured summaries, identify keywords, and build a vector store — all powered by a multi-node LangGraph pipeline and Mistral AI.
Once notes are generated, an interactive Q&A chat lets you ask anything about the lecture, with answers grounded in the actual content via retrieval-augmented generation (RAG). Notes can be exported as a formatted .docx file.


<img width="1892" height="940" alt="Screenshot 2026-02-28 152015" src="https://github.com/user-attachments/assets/ff98b183-9947-45b1-967c-af257a2038fb" />

Features

Automatic Transcription — Supports .wav, .mp3, .mp4, .ogg, .m4a via ASR node
Intelligent Note Generation — Multi-stage LangGraph pipeline: transcription → relevance filtering → normalization → chunking → topic detection → summarization → keyword extraction → validation → structuring
Interactive Q&A Chat — RAG-powered chat grounded in your lecture content using ChromaDB and Mistral embeddings
DOCX Export — Download structured notes as a formatted Word document
FastAPI Backend — Clean REST API separating backend logic from the Streamlit frontend
Auto-Start Backend — Streamlit app automatically launches the FastAPI server on startup
Dark Blue UI Theme — Custom professional dark interface built with Streamlit  

Endpoints with Description

GET /health – Health check
POST /process-lecture – Upload audio/video, run pipeline, return notes
POST /chat – Ask a question about a processed lecture
GET /download-notes/{lecture_id} – Download notes as .docx
GET /sessions – List active lecture sessions

<img width="1024" height="1536" alt="ChatGPT Image Feb 28, 2026, 09_18_35 PM" src="https://github.com/user-attachments/assets/ddbe8991-51b0-4381-871a-4294c306bbda" />



