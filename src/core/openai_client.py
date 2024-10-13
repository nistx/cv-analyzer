import openai
from src.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_openai_client():
    return openai

