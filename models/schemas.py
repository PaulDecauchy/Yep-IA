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
    title: Optional[str] = None         # ≈ 30 caractères
    subTitle: Optional[str] = None      # ≈ 20 caractères
    ingredients: List[Ingredient]
    utensils: Optional[List[str]] = []
    tags: Optional[Preferences] = None

class RecipeWithoutChainPrompt(BaseModel):
    title: Optional[str] = None         # ≈ 30 caractères
    subTitle: Optional[str] = None      # ≈ 20 caractères
    utensils: Optional[List[str]] = []
    tags: Optional[Preferences] = None


class TitleSelected(BaseModel):
    title: str
