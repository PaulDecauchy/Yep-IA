from typing import Union
from fastapi import FastAPI
from api import recipes  # ← importe ton router (chemin selon ton projet)

app = FastAPI()

app.include_router(recipes.router, prefix="/recipes")  # ← ajoute ton router

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
