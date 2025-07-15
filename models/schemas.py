from pydantic import BaseModel
from typing import List, Optional

class Prompt(BaseModel):
    message: str

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str

class Preferences(BaseModel):
    diet: Optional[List[str]] = []
    tag: Optional[List[str]] = []
    allergies: Optional[List[str]] = []

class RecipeChainPrompt(BaseModel):
    title: Optional[str] = None
    ingredients: List[Ingredient]
    utensils: Optional[List[str]] = []
    tags: Optional[Preferences] = None

class RecipeWithoutChainPrompt(BaseModel):
    title: Optional[str] = None
    utensils: Optional[List[str]] = []
    tags: Optional[Preferences] = None


class TitleSelected(BaseModel):
    title: str
