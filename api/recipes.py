from fastapi import APIRouter
from models.schemas import Prompt, RecipeChainPrompt, TitleSelected
from fastapi import APIRouter
from models.schemas import Prompt, RecipeChainPrompt
from services.mistral_service import ask_mistral, ask_mistral_json
from title_generator import generate_titles_json
from services.mistral_service import client, model_name

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/titles")
def generate_titles(prompt: Prompt):
    preferences = prompt.tags.get("preferences", [])
    styles = prompt.tags.get("style", [])

    prompt_text = f"""
Tu es un assistant culinaire.

Génère 5 idées de titres de recettes en respectant les critères suivants :

- Préférences alimentaires : {", ".join(preferences)}
- Style culinaire : {", ".join(styles)}

Répond uniquement avec un JSON au format suivant :

{{
  "titles": ["Titre 1", "Titre 2", "Titre 3", "Titre 4", "Titre 5"]
}}

Aucune explication, juste le JSON.
""".strip()

    titles = ask_mistral_json(prompt_text)
    return titles

@router.post("/ingredients")
def generate_ingredients(data: TitleSelected):
    preferences = data.tags.get("preferences", [])
    styles = data.tags.get("style", [])

    prompt = f"""
Recette : {data.title}
Préférences : {", ".join(preferences)}
Style culinaire : {", ".join(styles)}

Donne uniquement un JSON valide sous cette forme :

{{
  "ingredients": [
    {{"name": "farine", "quantity": 250, "unit": "g"}},
    {{"name": "lait", "quantity": 500, "unit": "ml"}},
    {{"name": "œufs", "quantity": 2, "unit": "pièce"}}
  ]
}}

- name : nom en français
- quantity : nombre (utilise . pour les décimales)
- unit : g, ml, cl, l, kg, pièce, pincée, cuillère...

Pas d’explication. Juste le JSON.
""".strip()

    print("🧪 Prompt ingrédients :", prompt)
    ingredients = ask_mistral_json(prompt)
    print("🧾 Réponse ingrédients :", ingredients)

    if not ingredients or "ingredients" not in ingredients:
        return {"error": "Erreur lors de la génération des ingrédients", "raw": ingredients}

    return ingredients

@router.post("/steps")
def generate_steps(prompt: Prompt):
    preferences = prompt.tags.get("preferences", [])
    styles = prompt.tags.get("style", [])

    steps_prompt = f"""
Tu es un chef spécialisé dans les recettes {", ".join(preferences)} de style {", ".join(styles)}.

Décris les étapes de la recette ci-dessous en JSON :

Message utilisateur :
{prompt.message}

Format attendu :

{{
  "steps": [
    "étape 1",
    "étape 2"
  ]
}}

Aucune explication. Juste le JSON.
""".strip()

    return ask_mistral_json(steps_prompt)

@router.post("/chain")
def generate_full_recipe(prompt: RecipeChainPrompt):
    chosen_title = prompt.title
    print("🔗 Étape 1 - Titre choisi :", chosen_title)

    # Extraction des tags
    preferences = prompt.tags.preferences if prompt.tags and prompt.tags.preferences else []
    styles = prompt.tags.style if prompt.tags and prompt.tags.style else []

    # Étape 2 : Génération des ingrédients
    ingredients_prompt = f"""
Recette : {chosen_title}
Style culinaire : {', '.join(styles)}
Préférences alimentaires : {', '.join(preferences)}

Donne uniquement un JSON valide sous cette forme :

{{
  "ingredients": [
    {{"name": "farine", "quantity": 250, "unit": "g"}},
    {{"name": "lait", "quantity": 500, "unit": "ml"}},
    {{"name": "œufs", "quantity": 2, "unit": "pièce"}}
  ]
}}

- name : nom en français
- quantity : nombre (utilise . pour les décimales)
- unit : g, ml, cl, l, kg, pièce, pincée, cuillère...

Aucune explication. Juste le JSON.
""".strip()

    print("🧪 Prompt ingrédients :", ingredients_prompt)
    ingredients_data = ask_mistral_json(ingredients_prompt)
    print("🧾 Réponse ingrédients :", ingredients_data)

    if not ingredients_data or "ingredients" not in ingredients_data:
        return {"error": "Erreur lors de la génération des ingrédients", "raw": ingredients_data}

    ingredients_text = ", ".join([
        f"{item['quantity']} {item['unit']} {item['name']}"
        for item in ingredients_data["ingredients"]
    ])

    # Étape 3 : Génération des étapes
    steps_prompt = f"""
Titre de la recette : {chosen_title}
Ingrédients : {ingredients_text}

Décris les étapes de la recette, en JSON comme ceci :

{{
  "steps": [
    "étape 1",
    "étape 2"
  ]
}}

Aucune explication. Juste le JSON.
""".strip()

    print("🧪 Prompt étapes :", steps_prompt)
    steps_data = ask_mistral_json(steps_prompt)
    print("🧾 Réponse étapes :", steps_data)

    if not steps_data or "steps" not in steps_data:
        return {"error": "Erreur lors de la génération des étapes", "raw": steps_data}

    # Résultat final
    return {
        "title": chosen_title,
        "ingredients": ingredients_data["ingredients"],
        "steps": steps_data["steps"],
        "tags": {
            "style_culinaire": styles,
            "preferences_alimentaires": preferences
        }
    }