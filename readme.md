# payeTonKawa_clients

Projet Python utilisant [FastAPI](https://fastapi.tiangolo.com/) pour créer une API web performante.

## Installation

```bash
git clone https://github.com/votre-utilisateur/payeTonKawa_clients.git
cd payeTonKawa_clients
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lancement du serveur API uniqument

```bash
uvicorn main:app --reload
```

## Lancement des docker

```bash
docker compose up -d
```

### Pour acceder au logs du conteneur API

```bash 
docker logs api_products -f
```

## Structure du projet

- `main.py` : Point d'entrée de l'application FastAPI
- `app/` : Dossier contenant la logique métier, les routes, les modèles, etc.

## Documentation interactive

Une fois le serveur lancé, accédez à la documentation interactive :

- Swagger UI : [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc : [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Observation du container de l'API

```bash
docker logs api_products -f
```

## Tests

```bash
PYTHONPATH=./app pytest
```

## Licence

Ce projet est sous licence MIT.
