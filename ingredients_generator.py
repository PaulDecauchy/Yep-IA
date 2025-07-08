from mistralai import UserMessage, SystemMessage
from kitchen_data import get_utensils_by_type
from utils import extract_json_from_text

def generate_ingredients_text(client, model_name, recipe_title, available_ingredients, utensil_type="traditional"):
    ingredients_str = "\n".join(f"- {item}" for item in available_ingredients)
    utensils = get_utensils_by_type(utensil_type)
    utensils_text = ", ".join(utensils)

    prompt = f"""
Tu es un assistant culinaire français.

Ta tâche est de proposer la **liste complète des ingrédients nécessaires** pour réaliser la recette suivante :  
**{recipe_title}**

Contraintes :
- Ingrédients disponibles :
{ingredients_str}

- Ustensiles disponibles : {utensils_text}
- N’utilise **que** les ingrédients fournis.
- Donne les **quantités précises** et les **unités** (g, ml, cl, pièce, etc.)

🧾 Réponds uniquement avec la liste des ingrédients au format suivant (exemple) :

- 250 g de farine  
- 500 ml de lait  
- 2 œufs  
- 1 pincée de sel

Ne donne **aucune explication** ni JSON. Juste la liste.
""".strip()

    messages = [
        SystemMessage(content="Tu es un assistant IA qui génère des listes d'ingrédients de cuisine en français."),
        UserMessage(content=prompt)
    ]

    response = client.chat.complete(model=model_name, messages=messages, temperature=0.7)
    content = response.choices[0].message.content.strip()

    return content

