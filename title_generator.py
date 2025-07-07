import json
import re
from mistralai import UserMessage, SystemMessage

def generate_titles_json(client, model_name, ingredients, utensils=None, tags=None):
    ing = ", ".join(ingredients)
    utensils_list = ", ".join(utensils or [])
    style_list = ", ".join(tags.get("style", []))
    difficulty = tags.get("difficulte", "")
    calories = tags.get("calories", "")
    preferences = tags.get("preferences", "")

    prompt = f"""
You are a recipe assistant. Given the following ingredients: {ing}.

Available kitchen utensils:
{utensils_list}

Preferred cooking style(s): {style_list}
Difficulty level: {difficulty}
Caloric level: {calories}
Dietary preferences: {preferences}

Return 3 creative recipe **titles** in **French** that use ONLY the ingredients provided and are compatible with the utensils and tags. DO NOT add any other ingredients.
Try to respect the cooking styles and dietary preferences as much as possible.
Return the result as a JSON object like this:

{{
  "titles": ["title1", "title2", "title3"]
}}

If it's not possible to create any recipes, respond with:
{{
  "error": "Not enough ingredients to generate recipe titles."
}}
"""

    messages = [
        SystemMessage(content="You generate JSON outputs for a cooking app."),
        UserMessage(content=prompt.strip())
    ]

    response = client.chat.complete(model=model_name, messages=messages, temperature=1.0)
    content = response.choices[0].message.content.strip()

    # Nettoyage si réponse encodée comme ```json ... ```
    content = re.sub(r"^```json\s*|```$", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("🧠 Réponse non-parsable détectée :", content)
        return {"error": "Invalid JSON format from model", "raw": content}