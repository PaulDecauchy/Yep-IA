# kitchen_data.py

# 🥄 Ustensiles traditionnels de base
TRADITIONAL_UTENSILS = [
    "wooden spoon",
    "silicone spatula",
    "ladle",
    "whisk",
    "skimmer",
    "kitchen tongs",
    "rubber spatula",
    "chef’s knife",
    "paring knife",
    "vegetable peeler",
    "cutting board",
    "grater",
    "kitchen scissors",
    "frying pan",
    "saucepan (2 sizes)",
    "stockpot or Dutch oven",
    "stewpot",
    "lids",
    "colander"
]

# 🤖 Ustensiles modernes (robots et appareils électriques)
MODERN_UTENSILS = [
    "blender",
    "food processor",
    "hand mixer",
    "stand mixer",
    "air fryer",
    "slow cooker",
    "pressure cooker",
    "Instant Pot",
    "rice cooker",
    "Thermomix",
    "steam oven",
    "sous-vide machine",
    "multicooker",
    "microwave oven"
]

# ✨ Pour fusionner selon le choix utilisateur
def get_utensils_by_type(utensil_type: str):
    if utensil_type == "traditional":
        return TRADITIONAL_UTENSILS
    elif utensil_type == "modern":
        return TRADITIONAL_UTENSILS + MODERN_UTENSILS
    else:
        return []  # ou raise ValueError
