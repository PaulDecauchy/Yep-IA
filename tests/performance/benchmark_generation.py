def test_generate_recipe_perf(client, benchmark):
    payload = {
        "prompt": {
            "title": "Performance test",
            "ingredients": [
                {"name": "riz", "quantity": 200, "unit": "g"},
                {"name": "courgette", "quantity": 2, "unit": "pièces"}
            ],
            "utensils": ["casserole"],
            "tags": {
                "diet": ["végétarien"],
                "tag": ["rapide", "été"],
                "allergies": []
            }
        },
        "excluded_titles": []
    }

    def run():
        response = client.post("/recipes/generate", json=payload)
        assert response.status_code == 200
        return response.json()

    result = benchmark(run)
    assert "recipe" in result
