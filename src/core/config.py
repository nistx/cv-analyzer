import os
from dotenv import load_dotenv

load_dotenv()

class Constants:
    RANKING_MIN: int = 0
    RANKING_MAX: int = 5
    QUALIFIED_THRESHOLD: int = 3
    ROUNDED_THRESHOLD: float = 0.5
    INTEGER_THRESHOLD: int = 1

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    if not OPENAI_API_KEY:
        raise ValueError("Missing OpenAI API Key. Define it in the .env file")

settings = Settings()
constants = Constants()