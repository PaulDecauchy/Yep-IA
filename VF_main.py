import os
import time
from mistralai import Mistral, UserMessage, SystemMessage

def load_api_key():
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("La variable d’environnement MISTRAL_API_KEY n’est pas définie !")
    return api_key

def get_recipe_from_inventory(client, model_name, ingredients, dietary_preference=None):
    ingredients_list = "\n".join([f"- {ingredient}" for ingredient in ingredients])
    dietary_info = f"Préférence alimentaire : {dietary_preference}\n" if dietary_preference else ""
    prompt = f"""
Tu es un assistant culinaire spécialisé dans la création de recettes à partir d'ingrédients disponibles.
Réponds de manière très concise (environ 2000 caractères maximum).

Voici une liste des ingrédients que j'ai actuellement :
{ingredients_list}

{dietary_info}
Propose-moi 1 recette en utilisant ces ingrédients. Pour chaque recette :
1. Liste simplement les ingrédients principaux utilisés parmi ceux listés.
2. Décris en quelques phrases les étapes principales.
"""

    messages = [
        SystemMessage(content="Tu es un assistant culinaire spécialisé dans la création de recettes à partir d'ingrédients disponibles."),
        UserMessage(content=prompt.strip())
    ]

    try:
        start_time = time.perf_counter()
        chat_response = client.chat.complete(
            model=model_name,
            messages=messages,
            max_tokens=1000
        )
        end_time = time.perf_counter()
        duration = end_time - start_time

        if chat_response.choices:
            content = chat_response.choices[0].message.content
            print(content)
            print("\n📊 Statistiques :")
            print(f"- Temps de génération : {duration:.2f} secondes")
            print(f"- Longueur de la réponse : {len(content)} caractères")
            return content
        else:
            print("Aucune réponse reçue.")
            return ""
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return ""

def main():
    api_key = load_api_key()
    client = Mistral(api_key=api_key)
    model_name = "mistral-medium-latest"
    print(f"Modèle utilisé : {model_name}")

    ingredients_sets = [
        ["4 carottes", "2 pommes de terre", "1 oignon", "250g de champignons",
         "2 courgettes", "1 aubergine", "250g de tomates", "1 poivron"]
    ]

    dietary_preference = input("Entrez votre préférence alimentaire (optionnel, par exemple, végétarien, végan) : ").strip()

    for idx, ingredients in enumerate(ingredients_sets):
        print(f"\nRecettes pour l'ensemble d'ingrédients {idx + 1} :")
        get_recipe_from_inventory(client, model_name, ingredients, dietary_preference or None)

if __name__ == "__main__":
    main()
