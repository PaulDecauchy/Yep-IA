import os
import json
import re
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()  # Charge les variables du fichier .env
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set!")
    return api_key

def extract_json_from_text(content, debug_prefix=""):
    """
    Extrait et parse un objet JSON depuis une chaîne contenant potentiellement
    du texte avant/après, ou des balises Markdown (ex: ```json ... ```).
    """
    try:
        # Nettoyage initial : suppression des balises markdown éventuelles
        content = content.strip()
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

        # Extraction avec regex du premier bloc JSON valide
        match = re.search(r'\{[\s\S]*?\}', content)
        if match:
            return json.loads(match.group(0))
        else:
            raise json.JSONDecodeError("No JSON object found", content, 0)
    except json.JSONDecodeError as e:
        print(f"\n❌ Erreur de parsing JSON {debug_prefix}: {e}")
        print("🔴 Contenu brut reçu :\n", content)
        return {"error": "Invalid JSON format from model"}
