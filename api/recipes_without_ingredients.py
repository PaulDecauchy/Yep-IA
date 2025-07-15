from fastapi import APIRouter
from fastapi.params import Body
from typing import List
from models.schemas import RecipeWithoutChainPrompt
from services.mistral_service import ask_mistral
from services.parsing_recipe import parse_recipe

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/parse-recipe")
def parse_recipe_endpoint(result: str = Body(..., embed=True)):
    return parse_recipe(result)

@router.post("/generate-without-ingredients")
def generate_recipe_without_ingredients(
    prompt: RecipeWithoutChainPrompt,
    excluded_titles: List[str] = Body(default=[])
):
    # ✅ Nouveau mapping des préférences
    diets = prompt.tags.diet if prompt.tags else []
    tags = prompt.tags.tag if prompt.tags else []
    allergies = prompt.tags.allergies if prompt.tags else []
    utensils = prompt.utensils or []
    utensils_str = ", ".join(utensils) if utensils else "non précisé"

    excluded_str = ""
    if excluded_titles:
        excluded_str = (
            "\nAttention : tu ne dois en aucun cas générer une recette avec un titre ou un thème proche de ceux-ci : "
            + ", ".join(f'"{title}"' for title in excluded_titles) + "."
        )

    context_message = f"""
Tu es un assistant culinaire.

Voici les contraintes permanentes à respecter pour chaque recette :

- Ustensiles disponibles : {utensils_str}
- Préférences alimentaires :
  - Régimes : {", ".join(diets) if diets else "aucun"}
  - Allergies : {", ".join(allergies) if allergies else "aucune"}
- Tags culinaires : {", ".join(tags) if tags else "aucun"}

Tu dois toujours respecter ces contraintes.
{excluded_str}
""".strip()

    user_prompt = f"""
Génère une recette complète et réaliste en respectant toutes les contraintes, avec une **structure stricte**.

Tu dois inclure **un titre généré** au début de la réponse qui ne peut pas être **sans titre**.

La réponse doit être structurée **exactement** ainsi :

Titre :  
Préparation : XX minutes  
Cuisson totale : XX minutes  
Diet : [ex. végétarien, pauvre en glucides]  
Tags : [ex. street food, indien]

Ingrédients :  
- [nom] : [quantité] [unité]  
(ex. farine : 200 g, œufs : 2 pièce, sel : au goût)

Étapes :  
1. ...  
2. ...

Utilise uniquement les ustensiles fournis. Respecte impérativement la structure. Aucun encadré, aucun JSON.
""".strip()

    messages = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": user_prompt}
    ]

    raw_response = ask_mistral(messages)
    parsed = parse_recipe(raw_response)

    parsed_ingredients = parsed.get("ingredients", [])
    parsed_steps = parsed.get("steps", [])

    return {
        "recipe": parsed,
    }

