import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    if not OPENAI_API_KEY:
        raise ValueError("Missing OpenAI API Key. Define it in the .env file")

settings = Settings()