import json
import re
import datetime
import sqlite3
import json
import re
import datetime
import sqlite3
from title_generator import generate_titles_json
from ingredients_generator import generate_ingredients
from steps_generator import generate_steps
from utils import load_api_key
from mistralai import Mistral
from cuisine_styles import CUISINE_STYLES

DB_PATH = "recettes.db"

def slugify(text):
    return re.sub(r'\W+', '_', text.strip().lower())

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                ingredients_input TEXT,
                generated_ingredients TEXT,
                steps TEXT,
                created_at TEXT
            )
        """)
        cursor = conn.execute("PRAGMA table_info(recipes);")
        columns = [row[1] for row in cursor.fetchall()]
        if "tags" not in columns:
            conn.execute("ALTER TABLE recipes ADD COLUMN tags TEXT")
            print("🛠️ Colonne 'tags' ajoutée à la table 'recipes'.")

def save_recipe_to_db(recipe):
    print("💾 Insertion dans la DB en cours...")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO recipes (title, ingredients_input, generated_ingredients, steps, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            recipe["title"],
            json.dumps(recipe["ingredients_input"], ensure_ascii=False),
            json.dumps(recipe["generated_ingredients"], ensure_ascii=False),
            json.dumps(recipe["steps"], ensure_ascii=False),
            json.dumps(recipe.get("tags", {}), ensure_ascii=False),
            datetime.datetime.now().isoformat()
        ))
    print(f"🗄️ Recette sauvegardée dans la base SQLite : {DB_PATH}")

def get_utensils(utensils_type):
    if utensils_type == "traditional":
        return ["wooden spoon", "frying pan", "saucepan", "knife", "cutting board", "whisk", "colander"]
    elif utensils_type == "modern":
        return ["Thermomix", "air fryer", "pressure cooker", "food processor", "blender", "induction hob"]
    return []

def parse_ingredients(ingredient_strs):
    parsed = []
    for item in ingredient_strs:
        parts = item.strip().split(maxsplit=1)
        quantity = parts[0] if len(parts) > 1 else "1"
        name = parts[1] if len(parts) > 1 else parts[0]
        parsed.append({"quantity": quantity, "name": name})
    return parsed

def display_recipe(recipe):
    print(f"\n✅ Recette choisie : {recipe['title']}")
    print("\n🧂 Ingrédients générés :")
    for item in recipe["generated_ingredients"]:
        print(f"- {item}")
    print("\n👨‍🍳 Étapes de la recette :")
    for idx, step in enumerate(recipe["steps"], 1):
        print(f"{idx}. {step}")
    print("\n📤 JSON complet à utiliser dans le front :")
    print(json.dumps(recipe, ensure_ascii=False, indent=2))

def save_json_file(recipe):
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = slugify(recipe["title"])
    filename = f"recette_{safe_title}_{date_str}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(recipe, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Résultat sauvegardé dans le fichier : {filename}")

DB_PATH = "recettes.db"

def slugify(text):
    return re.sub(r'\W+', '_', text.strip().lower())

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                ingredients_input TEXT,
                generated_ingredients TEXT,
                steps TEXT,
                created_at TEXT
            )
        """)

def save_recipe_to_db(recipe):
    print("💾 Insertion dans la DB en cours...")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO recipes (title, ingredients_input, generated_ingredients, steps, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            recipe["title"],
            json.dumps(recipe["ingredients_input"], ensure_ascii=False),
            json.dumps(recipe["generated_ingredients"], ensure_ascii=False),
            json.dumps(recipe["steps"], ensure_ascii=False),
            datetime.datetime.now().isoformat()
        ))
    print(f"🗄️ Recette sauvegardée dans la base SQLite : {DB_PATH}")

def get_utensils(utensils_type):
    if utensils_type == "traditional":
        return ["wooden spoon", "frying pan", "saucepan", "knife", "cutting board", "whisk", "colander"]
    elif utensils_type == "modern":
        return ["Thermomix", "air fryer", "pressure cooker", "food processor", "blender", "induction hob"]
    return []

def parse_ingredients(ingredient_strs):
    parsed = []
    for item in ingredient_strs:
        parts = item.strip().split(maxsplit=1)
        quantity = parts[0] if len(parts) > 1 else "1"
        name = parts[1] if len(parts) > 1 else parts[0]
        parsed.append({"quantity": quantity, "name": name})
    return parsed

def display_recipe(recipe):
    print(f"\n✅ Recette choisie : {recipe['title']}")
    print("\n🧂 Ingrédients générés :")
    for item in recipe["generated_ingredients"]:
        print(f"- {item}")
    print("\n👨‍🍳 Étapes de la recette :")
    for idx, step in enumerate(recipe["steps"], 1):
        print(f"{idx}. {step}")
    print("\n📤 JSON complet à utiliser dans le front :")
    print(json.dumps(recipe, ensure_ascii=False, indent=2))

def save_json_file(recipe):
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = slugify(recipe["title"])
    filename = f"recette_{safe_title}_{date_str}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(recipe, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Résultat sauvegardé dans le fichier : {filename}")

def main():
    init_db()
    api_key = load_api_key()
    client = Mistral(api_key=api_key)
    model_name = "mistral-medium-latest"

    # Récupération ingrédients
    raw_ingredients = input("Entrez vos ingrédients avec quantité (ex: 3 carottes, 200g jambon) : ").split(",")
    ingredients_input = [i.strip() for i in raw_ingredients if i.strip()]

    utensils_type = input("Type d’ustensiles disponibles (traditional / modern) : ").strip().lower()
    utensils = get_utensils(utensils_type)

    print("\n✨ Styles de cuisine disponibles :")
    print(", ".join(CUISINE_STYLES))
    selected_tags = input("Entre un ou plusieurs styles de cuisine (séparés par des virgules) : ")
    style_tags = [tag.strip() for tag in selected_tags.split(",") if tag.strip() in CUISINE_STYLES]

    difficulty = input("Niveau de difficulté (facile / difficile) : ").strip().lower()
    calories = input("Type de plat (léger / moyen / lourd) : ").strip().lower()
    dietary_pref = input("Préférences alimentaires (ex: sans gluten, vegan, etc.) : ").strip()

    tags = {
        "style": style_tags,
        "difficulte": difficulty,
        "calories": calories,
        "preferences": dietary_pref
    }

    print("\n🔎 Recherche de recettes avec les seuls ingrédients donnés...")
    response = generate_titles_json(client, model_name, ingredients_input, utensils, tags)
    titles = response.get("titles", [])

    if not titles:
        print("\n⚠️ Aucun titre de recette n’a été généré.")
        if input("Ajouter d'autres ingrédients ? (oui/non) : ").strip().lower() == "oui":
            new_ingredients = input("Nouveaux ingrédients (ex: 1 oignon, 2 œufs) : ").split(",")
            ingredients_input += [i.strip() for i in new_ingredients if i.strip()]
            response = generate_titles_json(client, model_name, ingredients_input, utensils, tags)
            titles = response.get("titles", [])
            if not titles:
                print(json.dumps({"error": "Toujours aucune recette générée."}))
                return
        else:
            print(json.dumps({"error": "Aucune recette trouvée."}))
            return

    print("\n🍽️ Recettes proposées :")
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title}")

    try:
        choice = int(input("\nChoisissez une recette (numéro) : ")) - 1
        chosen_title = titles[choice]
    except (ValueError, IndexError):
        print(json.dumps({"error": "Choix invalide."}))
        print(json.dumps({"error": "Choix invalide."}))
        return

    parsed_ingredients = parse_ingredients(ingredients_input)
    parsed_ingredients = parse_ingredients(ingredients_input)
    ingredients_list = generate_ingredients(client, model_name, chosen_title, parsed_ingredients, utensils_type)
    steps = generate_steps(client, model_name, chosen_title, parsed_ingredients, utensils_type)

    result = {
        "title": chosen_title,
        "ingredients_input": parsed_ingredients,
        "generated_ingredients": ingredients_list,
        "steps": steps,
        "tags": tags
    }

    display_recipe(result)
    save_json_file(result)
    save_recipe_to_db(result)

    print("\n📚 Recettes en base :")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, title, created_at FROM recipes ORDER BY id DESC")
        for row in cursor.fetchall():
            print(row)

if __name__ == "__main__":
    main()
