import os
import sys
import uvicorn
from dotenv import load_dotenv

# Force UTF-8 output on Windows so print() never crashes on any character
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# Load .env before anything else so all modules receive the env vars
load_dotenv()


def check_env():
    """Validate required environment variables before starting the server."""
    required = ["MISTRAL_API_KEY"]
    missing  = [var for var in required if not os.getenv(var)]

    if missing:
        print("\n[ERROR] Missing required environment variables:")
        for var in missing:
            print(f"    - {var}")
        print("\nPlease add them to your .env file and try again.\n")
        raise SystemExit(1)

    print("[OK] Environment variables loaded successfully.")


def main():
    check_env()

    host   = os.getenv("HOST", "0.0.0.0")
    port   = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"

    print(f"\n[INFO] Starting Lumina AI backend at http://{host}:{port}")
    print(f"[INFO] API docs available at http://{host}:{port}/docs\n")

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload
    )


if __name__ == "__main__":
    main()