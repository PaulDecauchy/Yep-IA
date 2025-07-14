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
    excluded_titles: List[str] = Body(default=[])
):
    preferences = prompt.tags.preferences if prompt.tags else []
    allergies = prompt.tags.allergies if prompt.tags and hasattr(prompt.tags, "allergies") else []
    styles = prompt.tags.style if prompt.tags else []
    utensils = prompt.utensils or []

    ingredient_names = [i.name for i in prompt.ingredients]
    ingredients_str = "\n".join(f"- {i}" for i in ingredient_names)
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
  - Allergies/intolérances : {", ".join(allergies) if allergies else "aucune"}
  - Régime : {", ".join(preferences) if preferences else "aucun"}
- Tags culinaires : {", ".join(styles) if styles else "aucun"}

Tu dois toujours respecter ces contraintes.
{excluded_str}
""".strip()

    user_prompt = f"""
Voici les ingrédients disponibles :
{ingredients_str}

Génère une recette complète et réaliste en respectant toutes les contraintes, avec une **structure stricte**.

Tu dois inclure **un titre généré** au début de la réponse.

La réponse doit être structurée **exactement** ainsi :

Titre :  
Préparation : XX minutes  
Cuisson totale : XX minutes  
Tags : tag1, tag2, tag3  

Ingrédients :  
- [nom] : [quantité] [unité]  
(ex. farine : 200 g, œufs : 2 pièce, sel : au goût)

Étapes :  
1. ...  
2. ...

Utilise uniquement les ingrédients et ustensiles fournis. Respecte impérativement la structure. Aucun encadré, aucun JSON.
""".strip()

    # ✅ messages au format dict pour `ask_mistral`
    messages = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": user_prompt}
    ]

    response = ask_mistral(messages)
    return {"result": response}
