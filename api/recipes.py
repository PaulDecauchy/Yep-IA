from fastapi import APIRouter
from ingredients_generator import generate_ingredients_text
from models.schemas import Prompt, RecipeChainPrompt, TitleSelected
from fastapi import APIRouter
from models.schemas import Prompt, RecipeChainPrompt
from services.mistral_service import ask_mistral
from title_generator import generate_titles_text
from services.mistral_service import client, model_name

router = APIRouter(prefix="/recipes", tags=["recipes"])
@router.post("/titles")
def generate_titles(prompt: RecipeChainPrompt):
    preferences = prompt.tags.preferences if prompt.tags else []
    styles = prompt.tags.style if prompt.tags else []

    ingredients = [ingredient.name for ingredient in prompt.ingredients]
    utensils = prompt.utensils or []
    tags = {
        "style": styles,
        "preferences": preferences,
        "difficulte": prompt.tags.difficulte if prompt.tags else "",
        "calories": prompt.tags.calories if prompt.tags else ""
    }

    titles_text = generate_titles_text(client, "mistral-medium", ingredients, utensils, tags)

    return {"result": titles_text}

@router.post("/ingredients")
def generate_ingredients(data: TitleSelected):
    # Tu dois décider comment tu veux récupérer les préférences/styles → soit tu les ajoutes dans TitleSelected, soit tu les ignores ici
    # Voici une version simple sans préférences
    recipe_title = data.title
    # simulate list of available ingredients (à remplacer selon ton cas réel)
    available_ingredients = ["pommes de terre", "lentilles corail", "oignons", "lait de coco", "ail", "huile d'olive"]
    
    # On utilise un type d’ustensiles générique pour l’instant
    ingredient_text = generate_ingredients_text(client, "mistral-medium", recipe_title, available_ingredients)

    return {"result": ingredient_text}

@router.post("/steps")
def generate_steps(prompt: Prompt):
    preferences = prompt.tags.get("preferences", []) if hasattr(prompt, "tags") else []
    styles = prompt.tags.get("style", []) if hasattr(prompt, "tags") else []

    steps_prompt = f"""
Tu es un chef cuisinier spécialisé dans les recettes {", ".join(preferences) or "traditionnelles"} de style {", ".join(styles) or "français"}.

Ta tâche est de décrire clairement les **étapes de préparation** de cette recette :  
"{prompt.message}"

Contraintes :
- Ne propose **aucun ingrédient ou ustensile** non mentionné dans la recette.
- Rédige des étapes simples, concises, numérotées, en **français**.
- Ne donne **aucune explication supplémentaire**, résumé ou introduction.

🧾 Exemple de format attendu :

1. Épluchez les légumes.  
2. Faites-les revenir dans une casserole.  
3. Ajoutez les épices et laissez mijoter.
""".strip()

    result = ask_mistral(steps_prompt)
    return {"result": result}

@router.post("/chain")
def generate_full_recipe(prompt: RecipeChainPrompt):
    chosen_title = prompt.title

    preferences = prompt.tags.preferences if prompt.tags and prompt.tags.preferences else []
    styles = prompt.tags.style if prompt.tags and prompt.tags.style else []
    available_ingredients = [f"{ing.quantity} {ing.unit} {ing.name}" for ing in prompt.ingredients]
    ingredient_names = [ing.name for ing in prompt.ingredients]
    utensils = prompt.utensils or []
    utensil_text = ", ".join(utensils)

    # Génération des ingrédients
    ingredients_prompt = f"""
Titre : {chosen_title}
Préférences : {", ".join(preferences) or "aucune"}
Style : {", ".join(styles) or "non précisé"}
Ingrédients disponibles :
{chr(10).join(f"- {ing}" for ing in ingredient_names)}
Ustensiles disponibles : {utensil_text or "non précisé"}

Donne la liste des ingrédients nécessaires avec leurs quantités. Utilise uniquement les ingrédients disponibles. Format clair, pas de liste JSON, pas d'explication.
""".strip()

    ingredients_text = ask_mistral(ingredients_prompt)

    # Génération des étapes
    steps_prompt = f"""
Titre : {chosen_title}
Ingrédients à utiliser :
{ingredients_text}

Ustensiles disponibles : {utensil_text or "non précisé"}

Décris les étapes de la recette. Format : liste numérotée, phrases courtes et précises. Pas d'introduction, pas de résumé.
""".strip()

    steps_text = ask_mistral(steps_prompt)

    # Format final
    full_text = f"""
Titre : {chosen_title}

Préférences : {", ".join(preferences) or "aucune"}
Style : {", ".join(styles) or "non précisé"}
Ustensiles : {utensil_text or "non précisé"}

Ingrédients :
{ingredients_text.strip()}

Étapes :
{steps_text.strip()}
""".strip()

    return {"result": full_text}
