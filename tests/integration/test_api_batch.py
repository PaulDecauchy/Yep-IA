def test_generate_multiple_recipes(client):
    payload = {
        "prompt": {
            "title": "Recette batch test",
            "ingredients": [
                {"name": "riz", "quantity": 200, "unit": "g"},
                {"name": "courgette", "quantity": 1, "unit": "pièce"},
                {"name": "ail", "quantity": 1, "unit": "gousse"}
            ],
            "utensils": ["poêle", "casserole"],
            "tags": {
                "diet": ["végétarien"],
                "tag": ["été", "rapide"],
                "allergies": []
            }
        },
        "excludedTitles": []
    }

    response = client.post("/recipes-batch/generate-multiple", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "recipes" in data
    recipes = data["recipes"]

    assert isinstance(recipes, list)
    assert 1 <= len(recipes) <= 4  # max 4 recettes attendues

    for r in recipes:
        assert "title" in r
        assert "ingredients" in r
        assert isinstance(r["ingredients"], list)
        assert "steps" in r
        assert isinstance(r["steps"], list)
