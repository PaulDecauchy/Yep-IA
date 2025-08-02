from typing import Union
from fastapi import FastAPI
from api import recipes  # ← importe ton router (chemin selon ton projet)
from api.recipes import router as recipe_router
from api.recipes_batch import router as recipe_batch_router
from api.recipes_without_ingredients import router as recipe_without_router
from api.recipes_batch_without import router as recipe_batch_without_router
from api.recipes_with_json import router as recipe_with_json_router



app = FastAPI()

app.include_router(recipe_router)
app.include_router(recipe_batch_router)
app.include_router(recipe_without_router)
app.include_router(recipe_batch_without_router)
app.include_router(recipe_with_json_router)



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
