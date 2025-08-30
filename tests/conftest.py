import os, sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# PYTHONPATH propre vers la racine du repo
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

@pytest.fixture(scope="session")
def app():
    # Si ton app est exposée dans main.py à la racine
    from main import app as fastapi_app
    return fastapi_app

@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)

# Variables d'env partagées pour tous les tests
@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("MISTRAL_API_KEY", "test_key")
    yield
