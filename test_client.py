import requests
import json

# The base URL of the running microservice
BASE_URL = "http://127.0.0.1:5001"

def print_header(title):
    """Prints a formatted header to organize the output."""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def test_get_all_recipes():
    """Demonstrates fetching all recipes."""
    print_header("1. Fetching All Recipes")
    try:
        response = requests.get(f"{BASE_URL}/recipes")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        print("Request: GET /recipes")
        print("Status Code:", response.status_code)
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_scale_recipe():
    """Demonstrates scaling a recipe."""
    print_header("2. Scaling a Recipe")
    
    # This data is sent to the stateless scaling endpoint.
    # We are asking to scale a recipe from 2 to 5 servings.
    scale_data = {
        "original_servings": 2,
        "desired_servings": 5,
        "ingredients": [
            {"name": "Eggs", "quantity": 4, "unit": ""},
            {"name": "Milk", "quantity": 2, "unit": "tbsp"}
        ]
    }
    
    try:
        print("Request: POST /scale-recipe")
        print("Request Body:")
        print(json.dumps(scale_data, indent=2))
        
        response = requests.post(f"{BASE_URL}/scale-recipe", json=scale_data)
        response.raise_for_status()
        
        print("\nStatus Code:", response.status_code)
        print("Response Body (Scaled Recipe):")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_edit_recipe():
    """Demonstrates editing an existing recipe."""
    print_header("3. Editing a Recipe")
    
    # We will edit the "Scrambled Eggs" recipe (ID "1")
    edit_data = {
        "recipe_id": "1",
        "name": "Deluxe Scrambled Eggs",
        "servings": 3,
        "ingredients": [
            {"name": "Large Eggs", "quantity": 6, "unit": ""},
            {"name": "Heavy Cream", "quantity": 3, "unit": "tbsp"},
            {"name": "Salt", "quantity": 0.5, "unit": "tsp"},
            {"name": "Chives", "quantity": 1, "unit": "tbsp"}
        ]
    }

    try:
        print("Request: POST /edit-recipe")
        print("Request Body:")
        print(json.dumps(edit_data, indent=2))

        response = requests.post(f"{BASE_URL}/edit-recipe", json=edit_data)
        response.raise_for_status()

        print("\nStatus Code:", response.status_code)
        print("Response Body (Updated Recipe):")
        print(json.dumps(response.json(), indent=2))

        # Verify the change by fetching the recipe directly
        print("\nVerifying the change with: GET /recipes/1")
        verify_response = requests.get(f"{BASE_URL}/recipes/1")
        verify_response.raise_for_status()
        print("Status Code:", verify_response.status_code)
        print("Response Body (Verify):")
        print(json.dumps(verify_response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_favorite_recipe():
    """Demonstrates marking a recipe as a favorite."""
    print_header("4. Marking a Recipe as Favorite")

    # Mark "Scrambled Eggs" (ID "1") as a favorite
    favorite_data = {
        "recipe_id": "1",
        "favorite": True
    }
    
    try:
        print("Request: POST /favorite-recipe")
        print("Request Body:")
        print(json.dumps(favorite_data, indent=2))

        response = requests.post(f"{BASE_URL}/favorite-recipe", json=favorite_data)
        response.raise_for_status()

        print("\nStatus Code:", response.status_code)
        print("Response Body (Favorite Status Updated):")
        print(json.dumps(response.json(), indent=2))

        # Now, fetch only favorite recipes to confirm the change
        print("\nVerifying by fetching only favorite recipes: GET /recipes?favorite=true")
        verify_response = requests.get(f"{BASE_URL}/recipes?favorite=true")
        verify_response.raise_for_status()
        print("Status Code:", verify_response.status_code)
        print("Response Body (Favorites Only):")
        print(json.dumps(verify_response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Starting microservice test program...")
    print(f"Targeting microservice at: {BASE_URL}")
    
    # Run the demonstration functions
    test_get_all_recipes()
    test_scale_recipe()
    test_edit_recipe()
    test_favorite_recipe()
    
    print("\n" + "="*50)
    print(" Test program finished.")
    print("="*50)
