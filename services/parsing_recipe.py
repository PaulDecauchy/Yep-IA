import re

def clean_title(text: str) -> str:
    # Supprime les caractères indésirables (*, ", etc.) tout en conservant les accents, tirets et apostrophes
    cleaned = re.sub(r"[^\w\sàâäéèêëîïôöùûüç'’\-]", "", text)
    return cleaned.strip()

def parse_ingredients(ingredient_lines):
    ingredients = []
    for line in ingredient_lines:
        line = line.lstrip("- ").strip()

        # Format : nom : quantité unité
        match = re.match(r"(?P<name>.+?)\s*:\s*(?P<quantity>[\d.,]+)?\s*(?P<unit>[^\d]*)?", line)
        if match:
            name = clean_title(match.group("name").strip())
            quantity_str = match.group("quantity")
            unit = match.group("unit").strip() if match.group("unit") else "au goût"

            try:
                quantity = float(quantity_str.replace(",", ".")) if quantity_str else None
            except ValueError:
                quantity = None
        else:
            name = clean_title(line.strip())
            quantity = None
            unit = "au goût"

        ingredients.append({
            "name": name,
            "quantity": quantity,
            "unit": unit
        })

    return ingredients

def parse_steps(text: str):
    steps_block = re.search(r"Étapes\s*:\s*\n(.+)", text, re.IGNORECASE | re.DOTALL)
    if not steps_block:
        return []

    # Capture toutes les étapes numérotées
    step_lines = re.findall(r"\d+\.\s*(.+?)(?=\n\d+\.|\Z)", steps_block.group(1).strip(), re.DOTALL)
    return [s.strip().replace("\n", " ") for s in step_lines]

def parse_recipe(text: str) -> dict:
    # Extraction avec nettoyage automatique
    title_raw = re.search(r"Titre\s*:\s*(.+)", text)
    subtitle_raw = re.search(r"Sous[-\s]?titre\s*:\s*(.+)", text)
    prep_time_match = re.search(r"Préparation\s*:\s*(\d+)", text)
    cook_time_match = re.search(r"Cuisson totale\s*:\s*(\d+)", text)

    title = clean_title(title_raw.group(1).strip()) if title_raw else "Sans titre"
    sub_title = clean_title(subtitle_raw.group(1).strip()) if subtitle_raw else ""

    prep_time = prep_time_match.group(1).strip() if prep_time_match else None
    cook_time = cook_time_match.group(1).strip() if cook_time_match else None

    ingredients_block = re.search(r"Ingrédients\s*:\s*\n(.+?)\n\nÉtapes", text, re.IGNORECASE | re.DOTALL)
    ingredient_lines = ingredients_block.group(1).strip().split("\n") if ingredients_block else []
    ingredients = parse_ingredients(ingredient_lines)

    steps = parse_steps(text)

    return {
        "title": title,
        "subTitle": sub_title,
        "preparationTime": prep_time,
        "totalCookingTime": cook_time,
        "ingredients": ingredients,
        "steps": steps
    }
