import streamlit as st
import requests
import os
import subprocess
import sys
import time
from dotenv import load_dotenv

load_dotenv()

# ── API Base URL (reads from env for deployment flexibility) ──────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Lumina AI", layout="wide")


# ── Dark Blue Theme CSS (intact) ──────────────────────────────────────────────

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
        background-color: #050d1a;
        color: #e8edf5;
    }

    .stApp {
        background: linear-gradient(135deg, #050d1a 0%, #0a1628 50%, #071020 100%);
        min-height: 100vh;
    }

    /* Subtle animated grid background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(30, 90, 200, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(30, 90, 200, 0.04) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Title ── */
    h1 {
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.6rem !important;
        background: linear-gradient(90deg, #4da6ff, #1a6bdc, #7ec8ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: -0.02em !important;
        padding-bottom: 0.3rem;
    }

    /* ── Headings ── */
    h2, h3, h4 {
        font-family: 'Sora', sans-serif !important;
        color: #a8c8f0 !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }

    /* ── Subheader ── */
    .stSubheader {
        color: #7eb8f5 !important;
    }

    /* ── File Uploader ── */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #0d1f3c, #0f2347) !important;
        border: 1.5px dashed #1e5ab8 !important;
        border-radius: 14px !important;
        padding: 1.5rem !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #4da6ff !important;
        box-shadow: 0 0 24px rgba(77, 166, 255, 0.12) !important;
    }

    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploaderDropzone"] * {
        color: #a8c8f0 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
        border: none !important;
    }

    /* ── Browse Files Button ── */
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploader"] button,
    button[kind="secondary"] {
        background: linear-gradient(135deg, #1a5cb8, #2470d8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(77, 166, 255, 0.4) !important;
        border-radius: 8px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 14px rgba(26, 92, 184, 0.35) !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(135deg, #2470d8, #3d8fe8) !important;
        box-shadow: 0 6px 20px rgba(77, 166, 255, 0.45) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1a5cb8, #2470d8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(77, 166, 255, 0.3) !important;
        border-radius: 10px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.03em !important;
        padding: 0.55rem 1.6rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 16px rgba(26, 92, 184, 0.35) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2470d8, #3d8fe8) !important;
        border-color: rgba(77, 166, 255, 0.7) !important;
        box-shadow: 0 6px 24px rgba(77, 166, 255, 0.45) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Download Button ── */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #0f3d80, #1a5cb8) !important;
        color: #cce0ff !important;
        border: 1px solid rgba(77, 166, 255, 0.4) !important;
        border-radius: 10px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 16px rgba(15, 61, 128, 0.4) !important;
    }

    [data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(135deg, #1a5cb8, #2470d8) !important;
        box-shadow: 0 6px 24px rgba(77, 166, 255, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Chat Input Footer ── */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stBottom,
    .stBottom > div {
        background: #050d1a !important;
        border-top: 1px solid rgba(30, 74, 158, 0.4) !important;
    }

    div[style*="position: sticky"],
    div[style*="position:sticky"],
    div[style*="position: fixed"],
    div[style*="position:fixed"] {
        background: #050d1a !important;
    }

    /* ── Chat Input Box ── */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {
        background: #0d1f3c !important;
        border: 1.5px solid #1e4a9e !important;
        border-radius: 12px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    [data-testid="stChatInput"]:focus-within,
    [data-testid="stChatInput"]:focus-within > div,
    [data-testid="stChatInput"]:focus-within > div > div {
        border-color: #4da6ff !important;
        box-shadow: 0 0 20px rgba(77, 166, 255, 0.15) !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] textarea:active {
        background: #0d1f3c !important;
        background-color: #0d1f3c !important;
        color: #ffffff !important;
        caret-color: #4da6ff !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.95rem !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #4a6fa5 !important;
        -webkit-text-fill-color: #4a6fa5 !important;
    }

    [data-testid="stChatInput"] textarea:-webkit-autofill,
    [data-testid="stChatInput"] textarea:-webkit-autofill:hover,
    [data-testid="stChatInput"] textarea:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px #0d1f3c inset !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stChatInputSubmitButton"] > button {
        background: linear-gradient(135deg, #1a5cb8, #2470d8) !important;
        border-radius: 8px !important;
        border: none !important;
        color: #ffffff !important;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        background: rgba(13, 31, 60, 0.7) !important;
        border: 1px solid rgba(30, 74, 158, 0.4) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 0.6rem !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(26, 92, 184, 0.15) !important;
        border-color: rgba(77, 166, 255, 0.25) !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #4da6ff !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(30, 74, 158, 0.4) !important;
        margin: 2rem 0 !important;
    }

    /* ── Markdown text ── */
    .stMarkdown p, .stMarkdown li {
        color: #c8d9ee !important;
        line-height: 1.7 !important;
    }

    /* ── Notes cards ── */
    [data-testid="stMarkdownContainer"] h3 {
        color: #7ec8ff !important;
        border-left: 3px solid #2470d8;
        padding-left: 0.75rem;
        margin-top: 1.5rem !important;
    }

    /* ── Error / Info boxes ── */
    .stAlert {
        background: rgba(13, 31, 60, 0.8) !important;
        border: 1px solid rgba(77, 166, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #a8c8f0 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #050d1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e4a9e;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2470d8;
    }

    /* ── Streamlit Top Header Bar ── */
    header[data-testid="stHeader"] {
        background: #050d1a !important;
        border-bottom: 1px solid rgba(30, 74, 158, 0.4) !important;
    }

    header[data-testid="stHeader"] button {
        color: #7eb8f5 !important;
        background: transparent !important;
    }

    header[data-testid="stHeader"] button:hover {
        background: rgba(26, 92, 184, 0.2) !important;
        color: #ffffff !important;
    }

    #MainMenu button {
        color: #7eb8f5 !important;
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        background: #050d1a !important;
    }

    [data-testid="stDecoration"] {
        background: linear-gradient(90deg, #1a5cb8, #4da6ff, #2470d8) !important;
        height: 2px !important;
        opacity: 1 !important;
    }

    [data-testid="stBaseButton-headerNoPadding"],
    .stActionButton button {
        color: #7eb8f5 !important;
        background: transparent !important;
        border: none !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #080f1f !important;
        border-right: 1px solid rgba(30, 74, 158, 0.3) !important;
    }

    /* ── Code blocks ── */
    code, pre {
        background: #0a1a35 !important;
        color: #7ec8ff !important;
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 6px !important;
        border: 1px solid rgba(30, 74, 158, 0.4) !important;
    }

    /* ── Spinner text ── */
    .stSpinner p {
        color: #7eb8f5 !important;
    }

    /* Remove default Streamlit padding weirdness */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Title ─────────────────────────────────────────────────────────────────────

st.title("✦ Lumina AI — Lecture Intelligence")


# ── Backend Auto-Start ────────────────────────────────────────────────────────
# Runs once per Streamlit browser session.
# If the FastAPI server isn't reachable, launches main.py as a background
# subprocess and waits up to 20 seconds for it to become available.

def _is_backend_alive() -> bool:
    try:
        r = requests.get(f"{API_BASE_URL}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


if "backend_started" not in st.session_state:
    st.session_state.backend_started = False

if not st.session_state.backend_started:

    if not _is_backend_alive():
        # Resolve absolute path to main.py so this works from any working directory
        main_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend.log")

        with st.spinner("🔧 Starting Lumina AI backend..."):
            with open(log_path, "w") as log_file:
                subprocess.Popen(
                    [sys.executable, main_py],
                    stdout=log_file,
                    stderr=log_file,
                    close_fds=True
                )

            # Poll every second until backend responds (max 20s)
            for _ in range(20):
                time.sleep(1)
                if _is_backend_alive():
                    break
            else:
                # Read last 30 lines of log to show the real error
                try:
                    with open(log_path, "r") as f:
                        log_tail = "".join(f.readlines()[-30:])
                except Exception:
                    log_tail = "Could not read backend.log"

                st.error("⚠️ Backend failed to start. See error below:")
                st.code(log_tail, language="bash")
                st.stop()

    # Mark as started so we never re-run this block on rerenders
    st.session_state.backend_started = True


# ── Session State Init ────────────────────────────────────────────────────────

if "notes" not in st.session_state:
    st.session_state.notes = None

if "lecture_id" not in st.session_state:
    st.session_state.lecture_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "docx_bytes" not in st.session_state:
    st.session_state.docx_bytes = None


# ── File Upload ───────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Upload Lecture",
    type=["wav", "mp3", "mp4", "ogg", "m4a"]
)

if uploaded_file:

    if st.button("⚡ Generate Notes"):

        with st.spinner("Processing lecture... this may take a minute."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/process-lecture",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.lecture_id   = data["lecture_id"]
                    st.session_state.notes        = data["notes"]
                    st.session_state.chat_history = []
                    st.session_state.docx_bytes   = None  # reset before fetching

                    # Fetch and cache DOCX bytes immediately while session is live
                    try:
                        docx_resp = requests.get(
                            f"{API_BASE_URL}/download-notes/{data['lecture_id']}",
                            timeout=60
                        )
                        if docx_resp.status_code == 200:
                            st.session_state.docx_bytes = docx_resp.content
                    except Exception:
                        pass  # non-fatal — warning shown below if bytes are None

                    st.success("✅ Notes generated successfully!")

                else:
                    detail = response.json().get("detail", response.text)
                    st.error(f"❌ Backend error: {detail}")

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The lecture may be too long — try a shorter clip.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Lost connection to the backend. Please check that the API server is still running.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")


# ── Download Notes Button ─────────────────────────────────────────────────────

if st.session_state.docx_bytes:
    st.download_button(
        label="⬇ Download Notes",
        data=st.session_state.docx_bytes,
        file_name="Lecture_Notes.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
elif st.session_state.notes and not st.session_state.docx_bytes:
    st.warning("⚠️ DOCX could not be prepared. Notes are still displayed below.")


# ── Display Notes ─────────────────────────────────────────────────────────────

if st.session_state.notes:

    st.subheader("Generated Notes")

    for note in st.session_state.notes:
        st.markdown(f"### {note['topic']}")
        st.write(note["summary"])
        st.write("Keywords:", ", ".join(note["keywords"]))

    st.divider()
    st.subheader("Lecture Q&A Chat")


    # ── Chat History Display ──────────────────────────────────────────────────

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])


    # ── Chat Input ────────────────────────────────────────────────────────────

    user_question = st.chat_input("Ask anything about this lecture...")

    if user_question:

        if not st.session_state.lecture_id:
            st.error("No active lecture session. Please upload and process a lecture first.")

        else:
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        chat_response = requests.post(
                            f"{API_BASE_URL}/chat",
                            json={
                                "lecture_id":   st.session_state.lecture_id,
                                "question":     user_question,
                                "chat_history": st.session_state.chat_history
                            },
                            timeout=60
                        )

                        if chat_response.status_code == 200:
                            answer = chat_response.json()["answer"]
                        elif chat_response.status_code == 404:
                            answer = (
                                "⚠️ Your session has expired (the backend was restarted). "
                                "Please re-upload and process your lecture to continue."
                            )
                        else:
                            detail = chat_response.json().get("detail", chat_response.text)
                            answer = f"❌ Backend error: {detail}"

                    except requests.exceptions.Timeout:
                        answer = "⏱️ The request timed out. Please try again."
                    except requests.exceptions.ConnectionError:
                        answer = "🔌 Lost connection to the backend. Please check the API server."
                    except Exception as e:
                        answer = f"Unexpected error: {e}"

                    st.markdown(answer)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
