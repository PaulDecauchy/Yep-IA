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
    allergies: Optional[List[str]] = []

class RecipeChainPrompt(BaseModel):
    title: Optional[str] = None
    ingredients: List[Ingredient]
    utensils: Optional[List[str]] = []
    tags: Optional[Tags] = None
    excluded_titles: Optional[List[str]] = []

class TitleSelected(BaseModel):
    title: str
