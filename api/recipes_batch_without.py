from fastapi import APIRouter
from fastapi.params import Body
from typing import List
from models.schemas import RecipeWithoutChainPrompt
from services.mistral_service import ask_mistral
from services.parsing_recipe import parse_recipe
import time

router = APIRouter(prefix="/recipes-batch", tags=["recipes"])

@router.post("/generate-multiple-without-ingredients")
def generate_multiple_recipes_without_ingredients(
    prompt: RecipeWithoutChainPrompt,
    excluded_titles: List[str] = Body(default=[])
):
    unique_titles = set(excluded_titles)
    recipes = []
    retries = 0
    max_recipes = 4
    max_retries = 10

    while len(recipes) < max_recipes and retries < max_retries:
        excluded_str = ""
        if unique_titles:
            excluded_str = (
                "\nAttention : tu ne dois pas générer de recette ayant un titre ou un thème proche de ceux-ci : "
                + ", ".join(f'"{t}"' for t in unique_titles) + "."
            )

        context_message = f"""
Tu es un assistant culinaire.

Voici les contraintes permanentes à respecter pour chaque recette :

- Ustensiles disponibles : {', '.join(prompt.utensils) if prompt.utensils else 'non précisé'}
- Préférences alimentaires :
  - Allergies/intolérances : {', '.join(prompt.tags.allergies) if prompt.tags and prompt.tags.allergies else 'aucune'}
  - Régime : {', '.join(prompt.tags.preferences) if prompt.tags and prompt.tags.preferences else 'aucun'}
- Tags culinaires : {', '.join(prompt.tags.style) if prompt.tags and prompt.tags.style else 'aucun'}

Tu dois toujours respecter ces contraintes.
{excluded_str}
""".strip()

        user_prompt = f"""

Génère une recette complète et réaliste en respectant toutes les contraintes, avec une **structure stricte**.

Tu dois inclure **un titre généré** au début de la réponse qui ne peut pas être "sans titre".

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

        messages = [
            {"role": "system", "content": context_message},
            {"role": "user", "content": user_prompt}
        ]

        try:
            raw_response = ask_mistral(messages)
            parsed = parse_recipe(raw_response)

            title = parsed.get("title", "").strip("* ").strip()

            if (
                not parsed.get("ingredients")
                or not parsed.get("steps")
                or title.lower() in (t.lower() for t in unique_titles)
            ):
                retries += 1
                time.sleep(1.2)
                continue

            unique_titles.add(title)
            recipes.append(parsed)

            for ing in parsed["ingredients"]:
                used_ingredients.add(ing["name"].lower())

        except Exception as e:
            retries += 1
            time.sleep(1.2)
            continue


    return {
        "recipes": recipes,
    }
