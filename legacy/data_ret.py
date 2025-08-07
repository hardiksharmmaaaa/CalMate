dish_name = "Pav Bhaji"
retrieved_ingredients = retrieve_ingredients(dish_name)
print(f"Ingredients for {dish_name}:")
for ingredient_name, quantity in retrieved_ingredients:
    print(f"- {ingredient_name}: {quantity}")
