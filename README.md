# API Backend Recip'IA

Une API backend développée avec FastAPI et Mistral IA pour l'application mobile Recip'IA.

## Prérequis

- Python 3.8+
- pip
- Environnement virtuel (venv)

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/PaulDecauchy/Yep-IA
cd https://github.com/PaulDecauchy/Yep-IA
```

2. Créez et activez l'environnement virtuel :

**Ubuntu/Linux/macOS :**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell) :**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Démarrage de l'application

### Mode développement local
```bash
uvicorn main:app --reload
```

### Mode développement avec émulateur Android Studio
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> **Note :** Adaptez l'adresse IP selon votre configuration d'émulateur Android Studio.

L'API sera accessible à l'adresse :
- Local : `http://localhost:8000`
- Avec émulateur : `http://0.0.0.0:8000`

## Documentation de l'API

Une fois l'application démarrée, vous pouvez accéder à :
- **Documentation interactive (Swagger)** : `/docs`
- **Documentation alternative (ReDoc)** : `/redoc`

## Déploiement

### Production (Render)
L'application est déployée sur Render : https://yep-ia.onrender.com/

**Documentation API en ligne :** https://yep-ia.onrender.com/docs

### Déploiement manuel
Pour déployer les dernières modifications :
1. Mergez vos changements sur la branche `main`
2. Effectuez un "Deploy latest commit" sur Render pour obtenir les dernières modifications

## Application Mobile

L'application mobile utilise cette API backend. Le déploiement se fait via :
- **APK** pour la distribution
- **Documentation API** : https://yep-ia.onrender.com/docs

## Structure du projet

```
.
├── api/                # Modules API
├── models/             # Modèles de données
├── myenv/              # Environnement virtuel
├── services/           # Services métier
├── tests/              # Tests unitaires
├── main.py             # Point d'entrée de l'application FastAPI
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

## Tests

Le projet utilise pytest pour les tests unitaires.

### Exécuter les tests

```bash
# Exécuter tous les tests
pytest

# Exécuter les tests avec plus de détails
pytest -v

# Exécuter un fichier de test spécifique
pytest tests/test_example.py

# Exécuter les tests avec couverture de code
pytest --cov
```

### Configuration

La configuration des tests se trouve dans le fichier `pytest.ini`.

## Contribution

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request


## Commandes utiles

```bash
# Démarrage rapide (développement local)
uvicorn main:app --reload

# Démarrage pour tests avec émulateur
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Activation environnement virtuel (Ubuntu)
source venv/bin/activate

# Activation environnement virtuel (Windows PowerShell)
venv\Scripts\Activate.ps1
```

---
