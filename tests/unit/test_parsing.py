from services.parsing_recipe import parse_recipe, parse_ingredients, parse_steps, clean_title

# === TESTS POUR CLEAN_TITLE ===

def test_clean_title_basic():
    assert clean_title("Gratin de légumes *") == "Gratin de légumes"
    assert clean_title("Soupe — épicée") == "Soupe - épicée"
    assert clean_title("  Tarte à l’oignon !  ") == "Tarte à l’oignon"
    assert clean_title("Pâtes & pesto – rapide") == "Pâtes pesto - rapide"

# === TESTS POUR PARSE_INGREDIENTS ===

def test_parse_ingredients_normal():
    lines = [
        "- riz : 200 g",
        "- tomates : 2 pièces",
        "- sel : au goût"
    ]
    result = parse_ingredients(lines)
    assert result[0]["name"] == "riz"
    assert result[0]["quantity"] == 200
    assert result[0]["unit"] == "g"
    assert result[2]["quantity"] == 1.0
    assert result[2]["unit"] == "au goût"

def test_parse_ingredients_malformed():
    lines = ["- juste du sel", "- ail :"]
    result = parse_ingredients(lines)
    assert result[0]["name"] == "juste du sel"
    assert result[0]["quantity"] == 1.0
    assert result[0]["unit"] == "au goût"
    assert result[1]["name"] == "ail"

# === TESTS POUR PARSE_STEPS ===

def test_parse_steps_ok():
    raw = """
Étapes :
1. Éplucher les pommes de terre.
2. Les faire cuire à l'eau.
3. Mixer et servir.
"""
    steps = parse_steps(raw)
    assert len(steps) == 3
    assert steps[0].startswith("Éplucher")

def test_parse_steps_empty():
    raw = "Pas d'étapes ici"
    steps = parse_steps(raw)
    assert steps == []

# === TESTS POUR PARSE_RECIPE ===

def test_parse_recipe_complete():
    raw = """
Titre : Salade estivale fraîcheur
Sous-titre : Tomates et concombres
Préparation : 10
Cuisson totale : 0
Diet : végétarien
Tags : été, rapide

Ingrédients :
- tomates : 2 pièces
- concombre : 1 pièce
- huile d'olive : 2 cuillères à soupe

Étapes :
1. Laver les légumes.
2. Couper en morceaux.
3. Assaisonner et servir.
"""
    recipe = parse_recipe(raw)
    assert recipe["title"] == "Salade estivale fraîcheur"
    assert recipe["subTitle"] == "Tomates et concombres"
    assert recipe["preparationTime"] == "10"
    assert recipe["totalCookingTime"] == "0"
    assert len(recipe["ingredients"]) == 3
    assert len(recipe["steps"]) == 3

def test_parse_recipe_partial():
    raw = """
Titre : Gratin mystère
Ingrédients :
- pommes de terre : 3 pièces

Étapes :
1. Cuire au four.
"""
    recipe = parse_recipe(raw)
    assert recipe["title"] == "Gratin mystère"
    assert recipe["subTitle"] == ""
    assert recipe["preparationTime"] is None
    assert recipe["totalCookingTime"] is None
    assert len(recipe["ingredients"]) == 1
    assert recipe["steps"][0].startswith("Cuire")
