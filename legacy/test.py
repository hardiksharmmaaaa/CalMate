import streamlit as st 
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
from gtts import gTTS
from io import BytesIO
import base64
import sqlite3

# Loading all the environment variables
load_dotenv()

# Configuring Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Database setup
def create_database():
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_name TEXT NOT NULL,
            ingredient_name TEXT NOT NULL,
            quantity TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_ingredients(dish_name, ingredients):
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    for ingredient in ingredients:
        cursor.execute('''
            INSERT INTO ingredients (dish_name, ingredient_name, quantity)
            VALUES (?, ?, ?)
        ''', (dish_name, ingredient['name'], ingredient['quantity']))
    conn.commit()
    conn.close()

def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel("gemini-1.5-pro")
    if image:
        response = model.generate_content([prompt, image[0]])
    else:
        response = model.generate_content([prompt])
    return response.text

def image_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None

def parse_ingredients(response):
    ingredients = []
    lines = response.split('\n')
    for line in lines:
        if ':' in line and line.lower().startswith('ingredients:'):
            continue
        if line.strip() and ':' in line:
            parts = line.split(':', 1)
            ingredient_name = parts[0].strip()
            quantity = parts[1].strip()
            ingredients.append({"name": ingredient_name, "quantity": quantity})
    return ingredients

prompt = """
Imagine you are a personal chef providing guidance on creating a specific dish. When someone asks you how to make a dish, respond by including:

Whenever given a dish name (e.g., ‘Spaghetti Carbonara’) followed by quantity, provide a detailed recipe including:

Dish Name: Sure, lets Cook this , Start with the dish name provided.
Ingredients: List precise quantities for each ingredient based on the given quantity.
Procedure: Outline a clear, beginner-friendly procedure with steps separated by line breaks.
Example Input: ‘Spaghetti Carbonara, for 2 people’

Desired Response:
Dish: Spaghetti Carbonara

Ingredients:

200g spaghetti
100g pancetta or guanciale, diced
2 large eggs
50g grated Parmesan cheese
1 clove garlic, peeled
Salt and black pepper, to taste

Procedure:

Step 1 - Cook the Spaghetti: Bring a large pot of salted water to a boil, then add the spaghetti. Cook until al dente, about 8-10 minutes. Reserve a cup of pasta water before draining.

Step 2 - Prepare the Sauce: In a bowl, beat the eggs and mix in the grated Parmesan cheese until smooth. Season with black pepper.

step 3 - Cook the Pancetta: In a large pan, heat a little olive oil over medium heat. Add the garlic clove and cook for 1 minute, then remove it. Add the pancetta and cook until crispy, about 4-5 minutes.

Step 4 - Combine Ingredients: Add the hot, drained spaghetti to the pan with the pancetta. Toss well to combine.

Step 5 - Add the Sauce: Remove the pan from heat, wait a few seconds, then pour the egg and cheese mixture over the pasta, stirring quickly to create a creamy sauce. If needed, add a bit of reserved pasta water to reach your desired consistency.

Step 6 - Serve: Season with additional black pepper, garnish with extra Parmesan, and serve immediately.

Note that the steps should be seperated by the next line 
Repeat this structure for all dishes, ensuring the response includes clear ingredients and easy-to-follow instructions."
"""

def main():
    # Set up the database
    create_database()

    # Streamlit App
    logo = Image.open("chef.png")
    st.image(logo, width=100)
    st.header("Dishify - Your Personal Chef, One Chat Away!")

    user_input = st.text_input("Enter dish or ingredient query here:", key="user_input")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    submit = st.button("Generate Recipe")

    if submit:
        if uploaded_file:
            image_data = image_image_setup(uploaded_file)
            response = get_gemini_response(prompt, image_data)
        elif user_input:
            response = get_gemini_response(user_input)
        else:
            st.warning("Please provide either an image or a text query.")
            return

        st.session_state.response = response
        st.header("The Response is:")
        st.write(response)

        # Parse and store ingredients in the database
        ingredients = parse_ingredients(response)
        dish_name = user_input.split(',')[0] if user_input else "Unknown Dish"
        store_ingredients(dish_name, ingredients)
        st.success(f"Ingredients for '{dish_name}' have been stored in the database.")

if __name__ == "__main__":
    main()
