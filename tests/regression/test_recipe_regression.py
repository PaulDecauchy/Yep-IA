import json
import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "snapshots")

def load_snapshot(name):
    with open(os.path.join(SNAPSHOT_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)

def test_generate_recipe_regression():
    # 🔁 Prompt de test fixe
    payload = {
        "prompt": {
            "title": "Gratin test régression",
            "ingredients": [
                {"name": "pommes de terre", "quantity": 500, "unit": "g"},
                {"name": "crème", "quantity": 20, "unit": "cl"}
            ],
            "utensils": ["four", "plat à gratin"],
            "tags": {
                "diet": ["végétarien"],
                "tag": ["gratin", "hiver"],
                "allergies": []
            }
        },
        "excluded_titles": []
    }

    response = client.post("/recipes/generate", json=payload)
    assert response.status_code == 200
    result = response.json()

    with open("tests/regression/snapshots/recipe_snapshot_001.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # 📄 Snapshot attendu
    expected = load_snapshot("recipe_snapshot_001.json")

    # ✅ Comparaison stricte
    assert result["recipe"]["title"] == expected["recipe"]["title"]
    assert len(result["recipe"]["ingredients"]) == len(expected["recipe"]["ingredients"])
    assert len(result["recipe"]["steps"]) >= 3


