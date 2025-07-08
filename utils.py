import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set!")
    return api_key
