from mistralai import UserMessage, SystemMessage
from kitchen_data import get_utensils_by_type
from utils import extract_json_from_text

def generate_steps(client, model_name, recipe_title, ingredients, utensil_type="traditional"):
    ingredients_str = "\n".join(f"- {item}" for item in ingredients)
    utensils = get_utensils_by_type(utensil_type)
    utensils_text = ", ".join(utensils)

    prompt = f"""
You are a French cooking assistant.

Generate clear cooking steps for the recipe titled "{recipe_title}" using ONLY the following ingredients:
{ingredients_str}

The available utensils are:
{utensils_text}

Do not use or mention any ingredients or utensils not listed.

Return the result in JSON format ONLY like this:

```json
{{
  "title": "{recipe_title}",
  "steps": ["\u00e9tape 1", "\u00e9tape 2", "..."],
  "utensils_required": ["..."]
}}
```
"""

    messages = [
        SystemMessage(content="You generate JSON outputs for recipe steps."),
        UserMessage(content=prompt)
    ]

    response = client.chat.complete(model=model_name, messages=messages, temperature=0.7)
    content = response.choices[0].message.content.strip()

    return extract_json_from_text(content)