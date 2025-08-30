import json, os

def test_recipe_regression(client, monkeypatch):
    import api.recipes as rmod

    def _stable(*args, **kwargs):
        return """Titre : Gratin de Pommes de Terre Crémeux
Sous-titre : X
Préparation : 15 minutes
Cuisson totale : 30 minutes
Diet : végétarien
Tags : hiver

Ingrédients :
- pommes de terre : 500 g
- crème : 20 cl

Étapes :
1. ...
"""
    monkeypatch.setattr(rmod, "ask_mistral", _stable)

    payload = {
        "prompt": {
            "title": "Gratin test régression",
            "ingredients": [
                {"name":"pommes de terre", "quantity":500, "unit":"g"},
                {"name":"crème", "quantity":20, "unit":"cl"}
            ],
            "utensils": ["four", "plat à gratin"],
            "tags": {"diet":["végétarien"], "tag":["gratin","hiver"], "allergies":[]}
        },
        "excluded_titles": []
    }

    r = client.post("/recipes/generate", json=payload)
    assert r.status_code == 200
    result = r.json()

    snap_path = "tests/regression/snapshots/recipe_snapshot_001.json"
    if os.getenv("UPDATE_SNAPSHOT") == "1":
        with open(snap_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    with open(snap_path, "r", encoding="utf-8") as f:
        expected = json.load(f)

    assert result["recipe"]["title"] == expected["recipe"]["title"]
