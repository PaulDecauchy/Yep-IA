from title_generator import generate_titles_json
from ingredients_generator import generate_ingredients
from steps_generator import generate_steps
from utils import load_api_key
from mistralai import Mistral

def main():
    api_key = load_api_key()
    client = Mistral(api_key=api_key)
    model_name = "mistral-medium-latest"

    # Récupération ingrédients
    raw_ingredients = input("Entrez vos ingrédients avec quantité (ex: 3 carottes, 200g jambon) : ").split(",")
    ingredients_input = [i.strip() for i in raw_ingredients if i.strip()]
    dietary_pref = input("Préférence alimentaire (optionnel) : ").strip()
    utensils_type = input("Type d’ustensiles disponibles (traditional / modern) : ").strip().lower()

    utensils = []
    if utensils_type == "traditional":
        utensils = [
            "wooden spoon", "frying pan", "saucepan", "knife", "cutting board", "whisk", "colander"
        ]
    elif utensils_type == "modern":
        utensils = [
            "Thermomix", "air fryer", "pressure cooker", "food processor", "blender", "induction hob"
        ]

    print("\n🔎 Recherche de recettes avec les seuls ingrédients donnés...")
    response = generate_titles_json(client, model_name, ingredients_input, dietary_pref, utensils)

    print("\n🧠 Réponse brute Mistral :")
    print(response)

    titles = response.get("titles")
    if not titles:
        print("\n⚠️ Aucun titre de recette n’a pu être généré uniquement avec les ingrédients fournis.")
        print("Vous pouvez ajouter d'autres ingrédients pour générer une recette.")
        add_more = input("Souhaitez-vous ajouter des ingrédients supplémentaires ? (oui/non) : ").strip().lower()
        if add_more == "oui":
            new_ingredients = input("Entrez les nouveaux ingrédients avec quantités (ex: 1 oignon, 2 œufs) : ").split(",")
            ingredients_input += [i.strip() for i in new_ingredients if i.strip()]
            response = generate_titles_json(client, model_name, ingredients_input, dietary_pref, utensils)
            print("\n🧠 Nouvelle réponse brute Mistral :")
            print(response)
            titles = response.get("titles")
            if not titles:
                print("❌ Même avec les nouveaux ingrédients, aucune recette n’a pu être générée.")
                return
        else:
            return

    print("\n🍽️ Recettes proposées :")
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title}")

    try:
        choice = int(input("\nChoisissez une recette (numéro) : ")) - 1
        chosen_title = titles[choice]
    except (ValueError, IndexError):
        print("❌ Choix invalide.")
        return

    # Transformer les ingrédients en dict avec nom et quantité
    parsed_ingredients = []
    for item in ingredients_input:
        parts = item.split(maxsplit=1)
        if len(parts) == 2:
            parsed_ingredients.append({"quantity": parts[0], "name": parts[1]})
        else:
            parsed_ingredients.append({"quantity": "1", "name": parts[0]})

    ingredients_list = generate_ingredients(client, model_name, chosen_title, parsed_ingredients, utensils_type)
    print("\n🧂 Ingrédients nécessaires :")
    print(ingredients_list)

    steps = generate_steps(client, model_name, chosen_title, parsed_ingredients, utensils_type)
    print("\n👨‍🍳 Étapes de la recette :")
    print(steps)

if __name__ == "__main__":
    main()
