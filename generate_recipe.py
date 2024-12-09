import openai
import os

# Ensure that OpenAI API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure the environment variable is set correctly

# Define Recipe Generation Function using new OpenAI API
def generate_recipe(ingredients, dietary_preferences, cooking_expertise):
    """
    Generate a personalized recipe using OpenAI based on user input.
    
    Args:
    ingredients (list): List of ingredients for the recipe.
    dietary_preferences (str): User's dietary preferences (e.g., "Vegan", "Keto").
    cooking_expertise (str): User's cooking expertise level (e.g., "Beginner", "Expert").
    
    Returns:
    str: Generated recipe text.
    """
    prompt = f"""
    Generate a personalized recipe based on the following:
    Ingredients: {', '.join(ingredients)}
    Dietary Preferences: {dietary_preferences}
    Cooking Expertise: {cooking_expertise}.
    Include step-by-step instructions and a brief description.
    """

    try:
        response = openai.chat_completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating recipe: {e}"
