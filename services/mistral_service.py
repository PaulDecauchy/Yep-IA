# mistral_service.py

import os
import json
import re
from dotenv import load_dotenv
from mistralai import Mistral, UserMessage, SystemMessage


load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)
model_name = "mistral-medium-latest"


def ask_mistral(message: str, context: str = "") -> str:
    """
    Envoie un prompt simple à Mistral et retourne une réponse en texte brut.
    """
    prompt = f"{context.strip()}\n{message.strip()}"
    messages = [
        SystemMessage(content="Tu es un assistant culinaire."),
        UserMessage(content=prompt)
    ]
    response = client.chat.complete(
        model=model_name,
        messages=messages,
        temperature=1.0
    )
    return response.choices[0].message.content.strip()
