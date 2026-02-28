import whisper
import re

model = whisper.load_model("base")

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def asr_node(state):

    audio_path = state["audio_path"]

    result = model.transcribe(audio_path)
    text = " ".join([seg["text"] for seg in result["segments"]])

    sentences = split_sentences(text)

    return {
        "sentences": sentences
    }