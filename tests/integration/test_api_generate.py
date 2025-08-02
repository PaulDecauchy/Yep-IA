# tests/integration/test_api_generate.py

def test_generate_recipe_full_prompt(client):
    payload = {
        "prompt": {
            "title": "Curry de légumes express",
            "ingredients": [
                {"name": "carottes", "quantity": 2, "unit": "pièces"},
                {"name": "lait de coco", "quantity": 20, "unit": "cl"},
                {"name": "pomme de terre", "quantity": 3, "unit": "pièces"}
            ],
            "utensils": ["casserole", "poêle"],
            "tags": {
                "diet": ["végétarien"],
                "tag": ["rapide", "hiver"],
                "allergies": []
            }
        },
        "excluded_titles": []
    }

    response = client.post("/recipes/generate", json=payload)
    assert response.status_code == 200

    json_data = response.json()
    assert "recipe" in json_data

    recipe = json_data["recipe"]
    assert isinstance(recipe, dict)
    assert "ingredients" in recipe
    assert isinstance(recipe["ingredients"], list)
    assert "steps" in recipe
    assert isinstance(recipe["steps"], list)
    assert "title" in recipe
