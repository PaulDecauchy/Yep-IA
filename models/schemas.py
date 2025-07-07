from pydantic import BaseModel
from typing import List, Optional

class Prompt(BaseModel):
    message: str

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str

class Tags(BaseModel):
    style: Optional[List[str]] = []
    difficulte: Optional[str] = None
    calories: Optional[str] = None
    preferences: Optional[List[str]] = []

class RecipeChainPrompt(BaseModel):
    title: str
    ingredients: List[Ingredient]
    utensils: Optional[List[str]] = []
    tags: Optional[Tags] = None

class TitleSelected(BaseModel):
    title: str
