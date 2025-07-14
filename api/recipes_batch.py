from fastapi import APIRouter
from models.schemas import RecipeChainPrompt
from services.mistral_service import ask_mistral
from services.parsing_recipe import parse_recipe
import time

router = APIRouter(prefix="/recipes-batch", tags=["recipes"])

@router.post("/generate-multiple")
def generate_multiple_recipes(prompt: RecipeChainPrompt):
    unique_titles = set()
    recipes = []
    retries = 0

    while len(recipes) < 4 and retries < 10:
        # Appel unique de la recette
        context_message = f"""
        Tu es un assistant culinaire.

        Voici les contraintes permanentes à respecter pour chaque recette :

        - Ustensiles disponibles : {', '.join(prompt.utensils) if prompt.utensils else 'non précisé'}
        - Préférences alimentaires :
          - Allergies/intolérances : {', '.join(prompt.tags.allergies) if prompt.tags and hasattr(prompt.tags, 'allergies') else 'aucune'}
          - Régime : {', '.join(prompt.tags.preferences) if prompt.tags else 'aucun'}
        - Tags culinaires : {', '.join(prompt.tags.style) if prompt.tags else 'aucun'}

        Tu dois toujours respecter ces contraintes.
        """.strip()

        ingredients_str = "\n".join(f"- {i.name}" for i in prompt.ingredients)

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

        messages = [
            {"role": "system", "content": context_message},
            {"role": "user", "content": user_prompt}
        ]

        try:
            raw_response = ask_mistral(messages)
            parsed = parse_recipe(raw_response)

            # Nettoyage du titre et vérifications
            parsed["title"] = parsed["title"].strip("* ").strip()

            if (not parsed["ingredients"] or not parsed["steps"] or parsed["title"] in unique_titles):
                retries += 1
                time.sleep(1.5)
                continue

            unique_titles.add(parsed["title"])
            recipes.append(parsed)

        except Exception as e:
            retries += 1
            time.sleep(1.5)
            continue

    return {"recipes": recipes}
