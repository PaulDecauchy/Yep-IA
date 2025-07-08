from mistralai import UserMessage, SystemMessage
from kitchen_data import get_utensils_by_type

def generate_steps_text(client, model_name, recipe_title, ingredients, utensil_type="traditional"):
    ingredients_str = "\n".join(f"- {item}" for item in ingredients)
    utensils = get_utensils_by_type(utensil_type)
    utensils_text = ", ".join(utensils)

    prompt = f"""
Tu es un assistant culinaire français.

Ta mission est de générer les **étapes de préparation** de la recette suivante :  
**{recipe_title}**

Ingrédients à utiliser :  
{ingredients_str}

Ustensiles disponibles : {utensils_text}

Contraintes :  
- Utilise uniquement les ingrédients et ustensiles fournis.  
- Décris les étapes **clairement, en français**, dans l’ordre chronologique.  
- Réponds uniquement avec les étapes, numérotées.  
- Ne donne **aucune explication supplémentaire**, ni résumé, ni JSON.

🧾 Exemple de format attendu :

1. Épluchez et émincez l’oignon.  
2. Faites-le revenir dans une casserole avec un peu d’huile d’olive.  
3. Ajoutez les lentilles corail et le lait de coco, puis laissez mijoter...

À toi de jouer !
""".strip()

    messages = [
        SystemMessage(content="Tu es un assistant IA qui rédige les étapes d’une recette de cuisine en français."),
        UserMessage(content=prompt)
    ]

    response = client.chat.complete(model=model_name, messages=messages, temperature=0.7)
    content = response.choices[0].message.content.strip()

    return content
