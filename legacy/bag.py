class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name  # Name of the ingredient
        self.quantity = quantity  # Amount of the ingredient
        self.unit = unit  # Unit of measurement (e.g., grams, cups)


class MagicBag:
    def __init__(self):
        self.ingredients = []  # A list to hold ingredients
    
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
    
    def view_bag(self):
        # Print all ingredients in the bag
        for ingredient in self.ingredients:
            print(f"{ingredient.quantity} {ingredient.unit} of {ingredient.name}")

# Creating an instance of MagicBag
magic_bag = MagicBag()

# Add ingredients
magic_bag.add_ingredient(Ingredient("Tomato", 2, "pieces"))
magic_bag.add_ingredient(Ingredient("Onion", 1, "pieces"))
magic_bag.add_ingredient(Ingredient("Olive Oil", 50, "ml"))

# View the ingredients in the bag
magic_bag.view_bag()


import requests

def add_to_blinkit_cart(ingredient):
    # Use Blinkit API to search and add the ingredient
    search_url = f"https://api.blinkit.com/search?query={ingredient.name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        product_data = response.json()  # Assume JSON response with product info
        blinkit_cart_url = f"https://www.blinkit.com/cart/add/{product_data['id']}"
        print(f"Added {ingredient.name} to Blinkit Cart.")
        return blinkit_cart_url
    else:
        print(f"Failed to find {ingredient.name} on Blinkit.")
        return None

# Add ingredients from the magic bag to Blinkit cart
for ingredient in magic_bag.ingredients:
    add_to_blinkit_cart(ingredient)



import streamlit as st

# Display the magic bag ingredients
def display_magic_bag(bag):
    st.title("Your Magic Bag")
    for ingredient in bag.ingredients:
        st.write(f"{ingredient.quantity} {ingredient.unit} of {ingredient.name}")
    
    if st.button("Add to Blinkit Cart"):
        for ingredient in bag.ingredients:
            add_to_blinkit_cart(ingredient)

# Streamlit UI to view and add ingredients
display_magic_bag(magic_bag)
