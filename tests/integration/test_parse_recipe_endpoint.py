def test_parse_recipe_ok(client):
    text = """Titre : Salade
Sous-titre : Verte
Préparation : 10 minutes
Cuisson totale : 0 minutes
Diet : végétarien
Tags : été

Ingrédients :
- concombre : 1 pièce
- sel : au goût

Étapes :
1. Couper
"""
    r = client.post("/recipes/parse-recipe", json={"result": text})
    assert r.status_code == 200
    data = r.json()
    recipe = data.get("recipe", data)
    assert "ingredients" in recipe and recipe["ingredients"]

def test_parse_recipe_bad(client):
    r = client.post("/recipes/parse-recipe", json={"result": "pas de structure"})
    assert r.status_code in (200, 400, 422)
