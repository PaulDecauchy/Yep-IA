def test_generate_recipe_without_ingredients(client):
    payload = {
        "prompt": {
            "title": "Recette sans ingrédient listé",
            "utensils": ["four", "mixeur"],
            "tags": {
                "diet": ["végétarien"],
                "tag": ["brunch", "week-end"],
                "allergies": ["gluten"]
            }
        },
        "excludedTitles": ["Pancakes au chocolat", "Tarte au fromage"]
    }

    response = client.post("/recipes/generate-without-ingredients", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "recipe" in data
    recipe = data["recipe"]

    assert "title" in recipe and isinstance(recipe["title"], str)
    assert "subTitle" in recipe and isinstance(recipe["subTitle"], str)
    assert "ingredients" in recipe and isinstance(recipe["ingredients"], list)
    assert "steps" in recipe and isinstance(recipe["steps"], list)
    assert "tags" in recipe and isinstance(recipe["tags"], dict)
