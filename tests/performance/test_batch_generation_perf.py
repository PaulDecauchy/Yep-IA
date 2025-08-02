def test_generate_multiple_recipes_perf(client, benchmark):
    payload = {
        "prompt": {
            "title": "Recette batch performance",
            "ingredients": [
                {"name": "riz", "quantity": 200, "unit": "g"},
                {"name": "poivron", "quantity": 1, "unit": "pièce"},
                {"name": "tomates", "quantity": 2, "unit": "pièces"}
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

    def run_batch():
        response = client.post("/recipes-batch/generate-multiple", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "recipes" in data
        assert 1 <= len(data["recipes"]) <= 4
        return data

    result = benchmark(run_batch)
    assert "recipes" in result
