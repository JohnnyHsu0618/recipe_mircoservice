# Recipe Management Microservice

This microservice provides functionality for scaling recipe ingredients, editing recipes, and managing a list of favorite recipes. It is designed to be a backend component for a larger recipe application.

## Communication Contract

This document outlines how another program (the "Main Program") can communicate with this microservice. The contract is stable and should be relied upon for integration.

### How to Request Data

The microservice exposes a REST API over HTTP. All data is sent and received in JSON format. The base URL for the service will be provided to you separately.

#### Endpoints

The following endpoints are available:

**1. Scale a Recipe**

This endpoint calculates new ingredient quantities based on a desired number of servings. It is a stateless calculation and does not save or modify any recipe.

*   **URL:** `/scale-recipe`
*   **Method:** `POST`
*   **Description:** Provide the original serving size, desired serving size, and a list of ingredients. The service will return the same list with quantities adjusted.
*   **Request Body:**

    ```json
    {
      "original_servings": 2,
      "desired_servings": 4,
      "ingredients": [
        { "name": "Flour", "quantity": 1.5, "unit": "cup" },
        { "name": "Sugar", "quantity": 1, "unit": "tbsp" }
      ]
    }
    ```

**2. Edit a Recipe**

This endpoint modifies an existing recipe in the database.

*   **URL:** `/edit-recipe`
*   **Method:** `POST`
*   **Description:** Provide the `recipe_id` and any fields you wish to update (`name`, `servings`, or `ingredients`).
*   **Request Body:**

    ```json
    {
      "recipe_id": "1",
      "name": "New Recipe Name",
      "servings": 3
    }
    ```

**3. Mark/Unmark a Recipe as Favorite**

This endpoint toggles the favorite status of a recipe.

*   **URL:** `/favorite-recipe`
*   **Method:** `POST`
*   **Description:** Provide the `recipe_id` and the new `favorite` status (`true` or `false`).
*   **Request Body:**

    ```json
    {
      "recipe_id": "1",
      "favorite": true
    }
    ```

**4. Get All Recipes**

This endpoint retrieves all stored recipes. It can also be used to fetch only favorite recipes.

*   **URL:** `/recipes` or `/recipes?favorite=true`
*   **Method:** `GET`
*   **Description:** Make a GET request to `/recipes` to get all recipes. To get only favorites, append the query parameter `?favorite=true`.

### How to Receive Data

The microservice will respond with JSON objects.

#### Example Responses

**1. Response for `/scale-recipe`**

The service returns a new JSON object with the scaled ingredients.

*   **Success (200 OK):**
    ```json
    {
      "original_servings": 2,
      "desired_servings": 4,
      "scaled_ingredients": [
        { "name": "Flour", "quantity": 3.0, "unit": "cup" },
        { "name": "Sugar", "quantity": 2.0, "unit": "tbsp" }
      ]
    }
    ```

**2. Response for `/edit-recipe` or `/favorite-recipe`**

The service returns the complete, updated recipe object.

*   **Success (200 OK):**
    ```json
    {
      "name": "New Recipe Name",
      "servings": 3,
      "ingredients": [
        { "name": "Flour", "quantity": 1.5, "unit": "cup" }
      ],
      "favorite": true
    }
    ```

**3. Error Response**

If a request is invalid or a resource is not found, the service will return an error message with a corresponding HTTP status code (e.g., 400 for bad request, 404 for not found).

*   **Error (404 Not Found):**
    ```json
    {
      "detail": "Recipe not found"
    }
    ```

### UML Sequence Diagram

This diagram illustrates the interaction between the Main Program and the Recipe Microservice for the three main functions.

```mermaid
sequenceDiagram
    participant MainProgram as Main Program
    participant Microservice as Recipe Microservice

    Note over MainProgram, Microservice: Scenario 1: Scaling a Recipe

    MainProgram->>+Microservice: POST /scale-recipe (JSON with ingredients & servings)
    Microservice->>Microservice: calculateScalingFactor(orig_servings, new_servings)
    Microservice->>Microservice: adjustIngredientQuantities(ingredients, factor)
    Microservice-->>-MainProgram: 200 OK (JSON with scaled ingredients)

    Note over MainProgram, Microservice: Scenario 2: Editing a Recipe

    MainProgram->>+Microservice: POST /edit-recipe (JSON with recipe_id & changes)
    Microservice->>Microservice: findRecipeById(recipe_id)
    alt Recipe Found
        Microservice->>Microservice: updateRecipeDetails(updates)
        Microservice-->>-MainProgram: 200 OK (JSON with full updated recipe)
    else Recipe Not Found
        Microservice-->>-MainProgram: 404 Not Found (JSON with error detail)
    end

    Note over MainProgram, Microservice: Scenario 3: Favoriting a Recipe and Fetching Favorites

    MainProgram->>+Microservice: POST /favorite-recipe (JSON with recipe_id & favorite=true)
    Microservice->>Microservice: findRecipeById(recipe_id)
    Microservice->>Microservice: setFavoriteStatus(true)
    Microservice-->>-MainProgram: 200 OK (JSON with updated recipe)

    MainProgram->>+Microservice: GET /recipes?favorite=true
    Microservice->>Microservice: queryRecipes(filter="favorite")
    Microservice-->>-MainProgram: 200 OK (JSON with list of favorite recipes)

```
