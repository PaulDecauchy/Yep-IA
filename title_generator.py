from mistralai import SystemMessage, UserMessage


def generate_titles_text(client, model_name, ingredients, utensils=None, tags=None):
    ing = ", ".join(ingredients)
    utensils_list = ", ".join(utensils or [])
    style_list = ", ".join(tags.get("style", []))
    difficulty = tags.get("difficulte", "")
    calories = tags.get("calories", "")
    preferences = ", ".join(tags.get("preferences", []))

    prompt = f"""
Tu es un assistant culinaire intelligent.

Ta tâche est de proposer entre 3 et 5 **titres de recettes en français**, en te basant sur :

- Les ingrédients disponibles : {ing}
- Les ustensiles disponibles : {utensils_list if utensils_list else "aucun renseigné"}
- Les styles culinaires préférés : {style_list if style_list else "non précisé"}
- Les préférences alimentaires : {preferences if preferences else "aucune"}
- Le niveau de difficulté souhaité : {difficulty if difficulty else "non précisé"}
- Le niveau calorique souhaité : {calories if calories else "non précisé"}

Contraintes :
- N'utilise **que** les ingrédients disponibles.
- Respecte autant que possible les préférences et styles donnés.
- Ne rajoute **aucun autre ingrédient**.
- Les recettes doivent pouvoir être réalisées avec les ustensiles listés.

Réponds uniquement avec la liste des titres, numérotée, sans autre texte ni explication. Exemple :

1. Soupe froide de tomates au basilic  
2. Curry doux de lentilles corail au lait de coco  
3. Poêlée de pommes de terre aux herbes

Si tu ne peux pas proposer de recettes valides, indique simplement :
"Impossible de générer des titres avec les ingrédients fournis."
""".strip()

    messages = [
        SystemMessage(content="Tu es un assistant IA qui génère des idées de recettes."),
        UserMessage(content=prompt)
    ]

    response = client.chat.complete(model=model_name, messages=messages, temperature=1.0)
    content = response.choices[0].message.content.strip()

    # Plus de parsing JSON ici
    return content