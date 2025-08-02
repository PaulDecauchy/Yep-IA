from fastapi import APIRouter, Body
from typing import List
from models.schemas import RecipeChainPrompt
from services.mistral_service import ask_mistral
import json

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/generate-json")
def generate_json_recipe(
    prompt: RecipeChainPrompt,
    excludedTitles: List[str] = Body(default=[])
):
    diets = prompt.tags.diet if prompt.tags else []
    tag = prompt.tags.tag if prompt.tags else []
    allergies = prompt.tags.allergies if prompt.tags else []
    utensils = prompt.utensils or []

    ingredient_names = [i.name for i in prompt.ingredients]
    ingredients_str = "\n".join(f"- {i}" for i in ingredient_names)
    utensils_str = ", ".join(utensils) if utensils else "non précisé"

    excluded_str = ""
    if excludedTitles:
        excluded_str = (
            "\nAttention : ne génère pas de recette similaire à : "
            + ", ".join(f'"{title}"' for title in excludedTitles) + "."
        )

    context_message = f"""
Tu es un assistant d’API culinaire. Tu dois générer des objets JSON strictement conformes au format demandé, utilisables directement par une API backend.

Les contraintes à respecter sont :

- Ustensiles disponibles : {utensils_str}
- Régimes : {", ".join(diets) if diets else "aucun"}
- Allergies : {", ".join(allergies) if allergies else "aucune"}
- Tags : {", ".join(tag) if tag else "aucun"}

{excluded_str}
""".strip()

    user_prompt = f"""
Voici les ingrédients disponibles :
{ingredients_str}

Tu dois générer une **recette complète et réaliste** au format **JSON brut**, avec la structure suivante :

{{
  "title": "...",
  "subTitle": "...",
  "preparationTime": "...",
  "totalCookingTime": "...",
  "tags": {{
    "diet": [...],
    "tag": [...],
    "allergies": [...]
  }},
  "ingredients": [
    {{
      "name": "...",
      "quantity": ...,
      "unit": "..."
    }}
  ],
  "steps": [
    "Étape 1...",
    "Étape 2..."
  ]
}}

INSTRUCTIONS OBLIGATOIRES :

- Tu dois répondre **uniquement** avec un objet JSON valide.
- **Aucun encadré** (pas de ```json ni ```).
- **Aucune explication, aucun commentaire, aucun texte supplémentaire**.
- La réponse doit commencer par une **accolade ouvrante** `.
- Il ne doit y avoir **aucun retour à la ligne ou espace** avant ou après le JSON.

La réponse doit être strictement conforme à ce format, sans rien d'autre.
""".strip()

    messages = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": user_prompt}
    ]

    raw_response = ask_mistral(messages)

    try:
        cleaned_response = raw_response.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response.replace("```json", "").strip()
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3].strip()

        recipe_json = json.loads(cleaned_response)
        return {"recipe": recipe_json}
    except Exception as e:
        return {
            "error": "Réponse Mistral invalide (JSON attendu)",
            "details": str(e),
            "raw_response": raw_response
        }
