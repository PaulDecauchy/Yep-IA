from fastapi import APIRouter
from fastapi.params import Body
from typing import List
from models.schemas import RecipeChainPrompt
from services.mistral_service import ask_mistral
from services.parsing_recipe import parse_recipe
import time

router = APIRouter(prefix="/recipes-batch", tags=["recipes"])


@router.post("/generate-multiple")
def generate_multiple_recipes(
    prompt: RecipeChainPrompt,
    excludedTitles: List[str] = Body(default=[])
):
    unique_titles = set(excludedTitles)
    recipes = []
    retries = 0
    max_recipes = 4
    max_retries = 10

    # 🔁 Extraction des contraintes
    diets = prompt.tags.diet if prompt.tags else []
    tags = prompt.tags.tag if prompt.tags else []
    allergies = prompt.tags.allergies if prompt.tags else []
    utensils_str = ", ".join(prompt.utensils) if prompt.utensils else "non précisé"

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

- Ustensiles disponibles : {utensils_str}
- Préférences alimentaires :
  - Régimes : {", ".join(diets) if diets else "aucun"}
  - Allergies : {", ".join(allergies) if allergies else "aucune"}
- Tags culinaires : {", ".join(tags) if tags else "aucun"}

Tu dois toujours respecter ces contraintes.
{excluded_str}
""".strip()

        ingredients_str = "\n".join(f"- {i.name}" for i in prompt.ingredients)

        user_prompt = f"""
Voici les ingrédients disponibles :
{ingredients_str}

Génère une recette complète et réaliste en respectant toutes les contraintes, avec une **structure stricte**.

Tu dois inclure **un titre principal (≈ 30 caractères)** et un **sous-titre (≈ 20 caractères)** au début de la réponse.

La structure d'en-tête doit être exactement :

Titre : [titre principal]  
Sous-titre : [sous-titre]   
Préparation : XX [minutes]  
Cuisson totale : XX [minutes]   
Diet : [ex. végétarien, pauvre en glucides]  
Tags : [ex. street food, indien]

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
            parsed_raw = parse_recipe(raw_response)

            title = parsed_raw.get("title", "").strip("* ").strip()
            if (
                not parsed_raw.get("ingredients")
                or not parsed_raw.get("steps")
                or title.lower() in (t.lower() for t in unique_titles)
            ):
                retries += 1
                time.sleep(1.2)
                continue

            # ✅ Ajouter les tags dans le bon ordre
            parsed = {
                "title": parsed_raw["title"],
                "subTitle": parsed_raw["subTitle"],
                "preparationTime": parsed_raw["preparationTime"],
                "totalCookingTime": parsed_raw["totalCookingTime"],
                "tags": prompt.tags.dict(),
                "ingredients": parsed_raw["ingredients"],
                "steps": parsed_raw["steps"]
            }

            unique_titles.add(title)
            recipes.append(parsed)

        except Exception:
            retries += 1
            time.sleep(1.2)
            continue

    return {
        "recipes": recipes
    }
