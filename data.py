import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    # Create a table to store ingredients
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
    # Connect to SQLite database
    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    # Insert ingredients into the table
    for ingredient in ingredients:
        cursor.execute('''
            INSERT INTO ingredients (dish_name, ingredient_name, quantity)
            VALUES (?, ?, ?)
        ''', (dish_name, ingredient['name'], ingredient['quantity']))

    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    # Create the database and table if it doesn't exist
    create_database()

    # Example dish and ingredients
    dish_name = "Pav Bhaji"
    ingredients = [
        {"name": "Potato", "quantity": "1 medium, boiled and mashed"},
        {"name": "Carrot", "quantity": "1 medium, finely chopped"},
        {"name": "Cauliflower", "quantity": "1/2 medium, finely chopped"},
        {"name": "Onion", "quantity": "1/2 medium, finely chopped"},
        {"name": "Tomato", "quantity": "1 medium, finely chopped"},
        {"name": "Green chili", "quantity": "1, finely chopped"},
        {"name": "Ginger", "quantity": "1 inch, grated"},
        {"name": "Garlic", "quantity": "2 cloves, minced"},
        {"name": "Pav bhaji masala", "quantity": "1 tbsp"},
        {"name": "Red chili powder", "quantity": "1/2 tsp (optional)"},
        {"name": "Turmeric powder", "quantity": "1/4 tsp"},
        {"name": "Cilantro", "quantity": "1/4 cup, chopped"},
        {"name": "Butter", "quantity": "2 tbsp"},
        {"name": "Salt", "quantity": "to taste"},
        {"name": "Pav rolls", "quantity": "4"},
        {"name": "Butter (for Pav)", "quantity": "1 tbsp"}
    ]

    # Store ingredients in the database
    store_ingredients(dish_name, ingredients)

    print(f"Ingredients for {dish_name} have been stored in the database.")

