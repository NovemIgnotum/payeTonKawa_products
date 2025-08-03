from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from database.session import engine
from routes import products

app = FastAPI()


@app.get("/")
def read_root():
    try:
        with engine.connect() as connection:
            return {"message": "Connexion à la base de données réussie !"}
    except OperationalError as e:
        return {"error": f"Erreur de connexion à la base de données : {e}"}

app.include_router(products.router, prefix="/api", tags=["products"])
