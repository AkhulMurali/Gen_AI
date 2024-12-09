import openai
import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Edamam API credentials
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")
EDAMAM_URL = "https://api.edamam.com/api/nutrition-data"

# Define Recipe Generation Function
def generate_recipe(ingredients, dietary_preferences, cooking_expertise):
    prompt = f"""
    Generate a personalized recipe based on the following:
    Ingredients: {', '.join(ingredients)}
    Dietary Preferences: {dietary_preferences}
    Cooking Expertise: {cooking_expertise}.
    Include step-by-step instructions and a brief description.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.AuthenticationError:
        return "Authentication failed. Please check your OpenAI API key."
    except openai.error.OpenAIError as e:
        return f"An error occurred with the OpenAI API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Define Nutrition Analysis Function
def analyze_nutrition(ingredients):
    ingredient_query = ", ".join(ingredients)
    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "ingr": ingredient_query
    }
    response = requests.get(EDAMAM_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Nutrition analysis failed. Please check your Edamam credentials."}

# Streamlit User Interface
def main():
    st.title('Personalized Recipe Generator')

    # User input for ingredients, dietary preferences, and cooking expertise
    ingredients_input = st.text_area('Enter Ingredients (comma-separated):')
    dietary_preferences = st.text_input('Dietary Preferences (e.g., Keto, Vegetarian):', 'None')
    cooking_expertise = st.selectbox('Cooking Expertise Level:', ['Beginner', 'Intermediate', 'Expert'])

    # If the user presses the button, generate the recipe and nutrition data
    if st.button('Generate Recipe'):
        # Clean and validate ingredient input
        ingredients = [i.strip() for i in ingredients_input.split(',') if i.strip()]
        
        if not ingredients:
            st.error("Please enter at least one ingredient.")
            return

        # Check if API keys are provided
        if not openai.api_key:
            st.error("OpenAI API key is not set. Please configure it in the environment variables.")
            return
        
        if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
            st.error("Edamam API credentials are not set. Please configure them in the environment variables.")
            return

        # Generate recipe
        recipe = generate_recipe(ingredients, dietary_preferences, cooking_expertise)
        
        # Analyze nutrition
        nutrition_data = analyze_nutrition(ingredients)
        
        # Display results
        st.subheader('Generated Recipe:')
        st.write(recipe)

        st.subheader('Nutrition Analysis:')
        if "error" in nutrition_data:
            st.write(nutrition_data["error"])
        else:
            st.json(nutrition_data)

# Run the app
if __name__ == "__main__":
    main()
