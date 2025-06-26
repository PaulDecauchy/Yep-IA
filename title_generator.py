import json
import re
from mistralai import UserMessage, SystemMessage

def generate_titles_json(client, model_name, ingredients, dietary_preference=None, utensils=None):
    ing = ", ".join(ingredients)
    dietary = f"Dietary preference: {dietary_preference}" if dietary_preference else ""
    utensils_list = ", ".join(utensils or [])

    prompt = f"""
You are a recipe assistant. Given the following ingredients: {ing}.
{dietary}

The user has the following kitchen utensils available:
{utensils_list}

Return 3 creative recipe **titles** in **French** that use ONLY the ingredients provided and are compatible with the available utensils.
DO NOT add any other ingredients. 
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

    # 💡 Nettoyage si réponse encodée comme ```json ... ```
    content = re.sub(r"^```json\s*|```$", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Pour le debug dans la console
        print("🧠 Réponse non-parsable détectée :", content)
        return {"error": "Invalid JSON format from model", "raw": content}
