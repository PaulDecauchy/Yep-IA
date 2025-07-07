TRADITIONAL_UTENSILS = [
    "wooden spoon", "silicone spatula", "ladle", "whisk", "skimmer", "kitchen tongs", "rubber spatula",
    "chef’s knife", "paring knife", "vegetable peeler", "cutting board", "grater", "kitchen scissors",
    "frying pan", "saucepan (2 sizes)", "stockpot", "Dutch oven", "stewpot", "lids", "colander",
    "oven", "grill"
]

MODERN_UTENSILS = [
    "Thermomix", "air fryer", "pressure cooker", "food processor", "blender", "induction hob", "microwave", "electric steamer"
]

def get_utensils_by_type(utensil_type):
    if utensil_type == "modern":
        return MODERN_UTENSILS
    return TRADITIONAL_UTENSILS
