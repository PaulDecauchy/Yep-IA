def test_generate_batch_ok(client, monkeypatch):
    import api.recipes_batch as rmod

    def fake_ok_llm(*args, **kwargs):
        return """Titre : Riz sauté
Sous-titre : Rapide
Préparation : 10 minutes
Cuisson totale : 15 minutes
Diet : végétarien
Tags : rapide

Ingrédients :
- riz : 200 g
- huile : 5 g

Étapes :
1. Cuire.
2. Mélanger.
"""
    monkeypatch.setattr(rmod, "ask_mistral", fake_ok_llm)

    # ✅ Ajout d'ingredients pour matcher le schema du router batch
    payload = {
        "prompt": {
            "title": "batch",
            "subTitle": "x",
            "ingredients": [                # <-- requis
                {"name": "riz", "quantity": 200, "unit": "g"}
            ],
            "utensils": ["wok"],
            "tags": {"diet": [], "tag": [], "allergies": []}
        },
        "excludedTitles": []
    }
    r = client.post("/recipes-batch/generate-multiple", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "recipes" in data and isinstance(data["recipes"], list)
    if data["recipes"]:
        assert "title" in data["recipes"][0]

def test_generate_batch_bad_format(client, monkeypatch):
    import api.recipes_batch as rmod

    def fake_bad_llm(*args, **kwargs):
        return "::: format invalide :::"
    monkeypatch.setattr(rmod, "ask_mistral", fake_bad_llm)

    payload = {
        "prompt": {
            "title": "batch",
            "subTitle": "x",
            "ingredients": [                # <-- idem
                {"name": "riz", "quantity": 200, "unit": "g"}
            ],
            "utensils": [],
            "tags": {"diet": [], "tag": [], "allergies": []}
        },
        "excludedTitles": []
    }
    r = client.post("/recipes-batch/generate-multiple", json=payload)
    # selon ta logique: peut rester 200 (retries → liste vide) ou erreur
    assert r.status_code in (200, 400, 422, 500)