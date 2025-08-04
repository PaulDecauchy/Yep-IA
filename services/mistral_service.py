import os
from dotenv import load_dotenv
from mistralai import Mistral, UserMessage, SystemMessage

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)
model_name = "mistral-small-latest"

def ask_mistral(messages: list[dict]) -> str:
    """
    Envoie une liste de messages [{"role": "system", "content": ...}, {"role": "user", "content": ...}]
    Retourne la réponse texte brute de Mistral.
    """
    formatted_messages = []
    for msg in messages:
        if msg["role"] == "system":
            formatted_messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            formatted_messages.append(UserMessage(content=msg["content"]))

    response = client.chat.complete(
        model=model_name,
        messages=formatted_messages,
        temperature=1.3
    )
    return response.choices[0].message.content.strip()
