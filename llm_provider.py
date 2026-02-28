import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from config import MISTRAL_MODEL_MAIN, MISTRAL_MODEL_FAST

# Load environment variables once
load_dotenv()

def get_main_llm():
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found in environment.")

    return ChatMistralAI(
        model=MISTRAL_MODEL_MAIN,
        temperature=0.2,
        mistral_api_key=api_key
    )

def get_fast_llm():
    api_key = os.getenv("MISTRAL_API_KEY")

    return ChatMistralAI(
        model=MISTRAL_MODEL_FAST,
        temperature=0,
        mistral_api_key=api_key
    )