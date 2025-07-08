import re

def parse_ingredients(ingredient_lines):
    ingredients = []
    for line in ingredient_lines:
        line = line.lstrip("- ").strip()

        # Format attendu : "nom : quantité unité"
        match = re.match(r"(?P<name>.+?)\s*:\s*(?P<quantity>[\d.,]+)?\s*(?P<unit>.+)?", line)

        if match:
            name = match.group("name").strip()
            quantity_str = match.group("quantity")
            unit = match.group("unit").strip() if match.group("unit") else "au goût"

            try:
                quantity = float(quantity_str.replace(",", ".")) if quantity_str else None
            except:
                quantity = None
        else:
            name = line.strip()
            quantity = None
            unit = "au goût"

        ingredients.append({
            "name": name,
            "quantity": quantity,
            "unit": unit
        })

    return ingredients


def parse_steps(text):
    steps_block = re.search(r"Étapes\s*:\s*\n(.+)", text, re.IGNORECASE | re.DOTALL)
    steps = []
    if steps_block:
        step_lines = re.findall(r"\d+\.\s*(.+?)(?=\n\d+\.|\Z)", steps_block.group(1).strip(), re.DOTALL)
        steps = [s.strip().replace("\n", " ") for s in step_lines]
    return steps


def parse_recipe(text: str) -> dict:
    title_match = re.search(r"Titre\s*:\s*(.+)", text)
    prep_time_match = re.search(r"Préparation\s*:\s*(.+)", text)
    cook_time_match = re.search(r"Cuisson totale\s*:\s*(.+)", text)
    tags_match = re.search(r"Tags\s*:\s*(.+)", text)

    title = title_match.group(1).strip() if title_match else "Sans titre"
    prep_time = prep_time_match.group(1).strip() if prep_time_match else None
    cook_time = cook_time_match.group(1).strip() if cook_time_match else None
    tags = [tag.strip() for tag in tags_match.group(1).split(",")] if tags_match else []

    # Ingrédients
    ingredients_block = re.search(r"Ingrédients\s*:\s*\n(.+?)\n\nÉtapes", text, re.IGNORECASE | re.DOTALL)
    ingredient_lines = ingredients_block.group(1).strip().split("\n") if ingredients_block else []
    ingredients = parse_ingredients(ingredient_lines)

    # Étapes
    steps = parse_steps(text)

    return {
        "title": title,
        "preparation_time": prep_time,
        "total_cooking_time": cook_time,
        "tags": tags,
        "ingredients": ingredients,
        "steps": steps
    }
