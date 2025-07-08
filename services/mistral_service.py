import os
from dotenv import load_dotenv
from mistralai import Mistral, UserMessage, SystemMessage

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)
model_name = "mistral-medium-latest"

def ask_mistral(messages: list) -> str:
    """
    Envoie une liste de messages (SystemMessage, UserMessage, etc.) à Mistral
    et retourne une réponse en texte brut.
    """
    response = client.chat.complete(
        model=model_name,
        messages=messages,
        temperature=1.0
    )
    return response.choices[0].message.content.strip()
