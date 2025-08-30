import pytest

# Fake LLM renvoie une recette bien formée
def make_ok_recipe(title="Recette test"):
    return {
        "title": title,
        "subTitle": "Sous-titre",
        "preparationTime": "10",
        "totalCookingTime": "20",
        "ingredients": [
            {"name": "farine", "quantity": 200, "unit": "g"}
        ],
        "steps": ["mélanger", "cuire"]
    }

@pytest.fixture
def fake_parse_ok(monkeypatch):
    def _fake_parse(raw):
        # raw_response n’est pas utilisé ici → on renvoie un dict direct
        return make_ok_recipe()
    monkeypatch.setattr("api.recipes_batch_without.parse_recipe", _fake_parse)

@pytest.fixture
def fake_parse_empty(monkeypatch):
    def _fake_parse(raw):
        return {
            "title": "Vide",
            "subTitle": "X",
            "preparationTime": "10",
            "totalCookingTime": "20",
            "ingredients": [],  # ⛔ vide
            "steps": []         # ⛔ vide
        }
    monkeypatch.setattr("api.recipes_batch_without.parse_recipe", _fake_parse)

def test_generate_multiple_ok(client, monkeypatch, fake_parse_ok):
    async def fake_ask(messages):
        return "RAW_OK"
    monkeypatch.setattr("api.recipes_batch_without.ask_mistral", fake_ask)

    payload = {
        "prompt": {
            "title": "x",
            "subTitle": "y",
            "utensils": ["casserole"],
            "tags": {"diet": [], "tag": [], "allergies": []}
        },
        "excludedTitles": []
    }
    r = client.post("/recipes-batch/generate-multiple-without-ingredients", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "recipes" in data
    assert len(data["recipes"]) >= 1
    assert data["recipes"][0]["ingredients"]

def test_generate_with_excluded_title(client, monkeypatch):
    # Patch parse_recipe pour renvoyer un titre exclu
    def _fake_parse(raw):
        return make_ok_recipe(title="Déjà pris")
    monkeypatch.setattr("api.recipes_batch_without.parse_recipe", _fake_parse)

    async def fake_ask(messages):
        return "RAW"
    monkeypatch.setattr("api.recipes_batch_without.ask_mistral", fake_ask)

    payload = {
        "prompt": {
            "title": "x",
            "subTitle": "y",
            "utensils": [],
            "tags": {"diet": [], "tag": [], "allergies": []}
        },
        "excludedTitles": ["Déjà pris"]
    }
    r = client.post("/recipes-batch/generate-multiple-without-ingredients", json=payload)
    assert r.status_code == 200
    data = r.json()
    # Pas de doublon avec le titre exclu
    assert all(rec["title"] != "Déjà pris" for rec in data["recipes"])

def test_generate_with_parse_error(client, monkeypatch):
    # simulate parse_recipe qui lève une exception
    def _fake_parse(raw):
        raise ValueError("bad format")
    monkeypatch.setattr("api.recipes_batch_without.parse_recipe", _fake_parse)

    async def fake_ask(messages):
        return "RAW_BAD"
    monkeypatch.setattr("api.recipes_batch_without.ask_mistral", fake_ask)

    payload = {
        "prompt": {
            "title": "x",
            "subTitle": "y",
            "utensils": [],
            "tags": {"diet": [], "tag": [], "allergies": []}
        },
        "excludedTitles": []
    }
    r = client.post("/recipes-batch/generate-multiple-without-ingredients", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["recipes"], list)

def test_generate_with_empty_recipe(client, monkeypatch, fake_parse_empty):
    async def fake_ask(messages):
        return "RAW_EMPTY"
    monkeypatch.setattr("api.recipes_batch_without.ask_mistral", fake_ask)

    payload = {
        "prompt": {
            "title": "x",
            "subTitle": "y",
            "utensils": [],
            "tags": {"diet": [], "tag": [], "allergies": []}
        },
        "excludedTitles": []
    }
    r = client.post("/recipes-batch/generate-multiple-without-ingredients", json=payload)
    assert r.status_code == 200
    data = r.json()
    # Même si retries → la sortie est bien une liste
    assert "recipes" in data
