import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Ajoute la racine du projet

from fastapi.testclient import TestClient
from main import app  # ← fonctionne maintenant
import pytest

@pytest.fixture
def client():
    return TestClient(app)
