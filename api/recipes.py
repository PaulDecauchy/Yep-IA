from fastapi import APIRouter
from fastapi.params import Body
from typing import List
from models.schemas import RecipeChainPrompt
from services.mistral_service import ask_mistral
from services.parsing_recipe import parse_recipe

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/parse-recipe")
def parse_recipe_endpoint(result: str = Body(..., embed=True)):
    return parse_recipe(result)


@router.post("/generate")
def generate_recipe(
    prompt: RecipeChainPrompt,
    excludedTitles: List[str] = Body(default=[])
):
    # Extraction des contraintes
    diets = prompt.tags.diet if prompt.tags else []
    tag = prompt.tags.tag if prompt.tags else []
    allergies = prompt.tags.allergies if prompt.tags else []
    utensils = prompt.utensils or []

    # Mise en forme
    ingredient_names = [i.name for i in prompt.ingredients]
    ingredients_str = "\n".join(f"- {i}" for i in ingredient_names)
    utensils_str = ", ".join(utensils) if utensils else "non précisé"

    # Titre à exclure
    excluded_str = ""
    if excludedTitles:
        excluded_str = (
            "\nAttention : tu ne dois en aucun cas générer une recette avec un titre ou un thème proche de ceux-ci : "
            + ", ".join(f'"{title}"' for title in excludedTitles) + "."
        )

    # Contexte pour Mistral
    context_message = f"""
Tu es un assistant culinaire.

Voici les contraintes permanentes à respecter pour chaque recette :

- Ustensiles disponibles : {utensils_str}
- Préférences alimentaires :
  - Régimes : {", ".join(diets) if diets else "aucun"}
  - Allergies : {", ".join(allergies) if allergies else "aucune"}
- Tags culinaires : {", ".join(tag) if tag else "aucun"}

Tu dois toujours respecter ces contraintes.
{excluded_str}
""".strip()

    # Prompt utilisateur
    user_prompt = f"""
Voici les ingrédients disponibles :
{ingredients_str}

Génère une recette complète et réaliste en respectant toutes les contraintes, avec une **structure stricte**.

Tu dois inclure **un titre généré** au début de la réponse.

La réponse doit être structurée **exactement** ainsi :

Titre :  
Préparation : XX minutes  
Cuisson totale : XX minutes  
Diet : [liste des régimes si présents]  
Tags : [liste des tags si présents]  

Ingrédients :  
- [nom] : [quantité] [unité]  
(ex. farine : 200 g, œufs : 2 pièce, sel : au goût)

Étapes :  
1. ...  
2. ...

Utilise uniquement les ingrédients et ustensiles fournis. Respecte impérativement la structure. Aucun encadré, aucun JSON.
""".strip()

    messages = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": user_prompt}
    ]

    # Appel au LLM
    raw_response = ask_mistral(messages)

    # Parsing recette
    parsed_raw = parse_recipe(raw_response)

    # Reconstruction dans le bon ordre
    parsed = {
        "title": parsed_raw["title"],
        "preparationTime": parsed_raw["preparationTime"],
        "totalCookingTime": parsed_raw["totalCookingTime"],
        "tags": prompt.tags.dict(),
        "ingredients": parsed_raw["ingredients"],
        "steps": parsed_raw["steps"]
    }

    return {
        "recipe": parsed
    }
