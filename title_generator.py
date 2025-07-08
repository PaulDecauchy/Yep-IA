from mistralai import SystemMessage, UserMessage


def generate_titles_text(client, model_name, ingredients, utensils=None, tags=None):
    ing = ", ".join(ingredients)
    utensils_list = ", ".join(utensils or [])
    style_list = ", ".join(tags.get("style", []))
    difficulty = tags.get("difficulte", "")
    calories = tags.get("calories", "")
    preferences = ", ".join(tags.get("preferences", []))

    prompt = f"""
Tu es un assistant culinaire.

Génère entre 3 et 5 idées de recettes à partir des informations suivantes :

Ingrédients disponibles : {ing}
Ustensiles disponibles : {utensils_list if utensils_list else "non précisé"}
Style culinaire : {style_list if style_list else "non précisé"}
Préférences alimentaires : {preferences if preferences else "aucune"}
Niveau de difficulté : {difficulty if difficulty else "non précisé"}
Niveau calorique : {calories if calories else "non précisé"}

Pour chaque idée, indique :
- Le titre de la recette
- Le temps total estimé de préparation et de cuisson (en minutes)

N’utilise que les ingrédients donnés. Ne propose pas d’autres aliments.
Réponds uniquement avec une liste numérotée comme ceci :

1. Titre de la recette – 40 minutes  
2. Autre titre – 25 minutes

Pas de commentaire, pas de texte additionnel.
""".strip()

    messages = [
        SystemMessage(content="Tu es un assistant IA qui génère des idées de recettes."),
        UserMessage(content=prompt)
    ]

    response = client.chat.complete(model=model_name, messages=messages, temperature=1.0)
    content = response.choices[0].message.content.strip()

    # Plus de parsing JSON ici
    return content