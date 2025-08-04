from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn

app = FastAPI(
    title="Recipe Microservice",
    description="A microservice to scale, edit, and manage favorite recipes.",
    version="1.0.0"
)

# --- In-Memory Database ---
# Pre-populated with two example recipes for demonstration purposes.
recipes_db: Dict[str, Dict[str, Any]] = {
    "1": {
        "name": "Scrambled Eggs",
        "servings": 2,
        "ingredients": [
            {"name": "Eggs", "quantity": 4, "unit": ""},
            {"name": "Milk", "quantity": 2, "unit": "tbsp"},
            {"name": "Salt", "quantity": 0.25, "unit": "tsp"}
        ],
        "favorite": False
    },
    "2": {
        "name": "Pancakes",
        "servings": 4,
        "ingredients": [
            {"name": "Flour", "quantity": 1.5, "unit": "cup"},
            {"name": "Baking Powder", "quantity": 3.5, "unit": "tsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"},
            {"name": "White Sugar", "quantity": 1, "unit": "tbsp"},
            {"name": "Milk", "quantity": 1.25, "unit": "cup"},
            {"name": "Egg", "quantity": 1, "unit": ""},
            {"name": "Melted Butter", "quantity": 3, "unit": "tbsp"}
        ],
        "favorite": True
    }
}

# --- Pydantic Models for Data Validation ---

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: Optional[str] = ""

class Recipe(BaseModel):
    name: str
    servings: float
    ingredients: List[Ingredient]
    favorite: bool

class ScaleRequest(BaseModel):
    original_servings: float = Field(..., gt=0, description="The original number of servings the recipe is for.")
    desired_servings: float = Field(..., gt=0, description="The number of servings you want to scale to.")
    ingredients: List[Ingredient]

class ScaleResponse(BaseModel):
    original_servings: float
    desired_servings: float
    scaled_ingredients: List[Ingredient]
    
class EditRequest(BaseModel):
    recipe_id: str
    name: Optional[str] = None
    servings: Optional[float] = None
    ingredients: Optional[List[Ingredient]] = None

class FavoriteRequest(BaseModel):
    recipe_id: str
    favorite: bool

# --- API Endpoints ---

@app.get("/recipes", response_model=Dict[str, Recipe])
def get_recipes(favorite: bool = False):
    """
    Retrieve all recipes, or filter for only favorite recipes.
    Set `favorite=true` in the query to see only favorited recipes.
    """
    if favorite:
        return {rid: r for rid, r in recipes_db.items() if r.get("favorite")}
    return recipes_db

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: str):
    """
    Retrieve a single recipe by its unique ID.
    """
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipes_db[recipe_id]

@app.post("/scale-recipe", response_model=ScaleResponse)
def scale_recipe(request: ScaleRequest):
    """
    Calculates scaled ingredient quantities based on desired servings.
    This is a stateless endpoint that does not modify stored recipes.
    """
    scale_factor = request.desired_servings / request.original_servings
    
    scaled_ingredients = []
    for ingredient in request.ingredients:
        scaled_ingredients.append(
            Ingredient(
                name=ingredient.name,
                quantity=ingredient.quantity * scale_factor,
                unit=ingredient.unit
            )
        )
        
    return ScaleResponse(
        original_servings=request.original_servings,
        desired_servings=request.desired_servings,
        scaled_ingredients=scaled_ingredients
    )

@app.post("/edit-recipe", response_model=Recipe)
def edit_recipe(request: EditRequest):
    """
    Update the details of an existing recipe.
    You can update the name, servings, or ingredients list.
    """
    if request.recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe = recipes_db[request.recipe_id]
    if request.name is not None:
        recipe["name"] = request.name
    if request.servings is not None:
        recipe["servings"] = request.servings
    if request.ingredients is not None:
        # Pydantic models are converted to dicts when assigned
        recipe["ingredients"] = [ing.dict() for ing in request.ingredients]
        
    return recipe

@app.post("/favorite-recipe", response_model=Recipe)
def favorite_recipe(request: FavoriteRequest):
    """
    Mark or unmark a recipe as a favorite.
    """
    if request.recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipes_db[request.recipe_id]["favorite"] = request.favorite
    return recipes_db[request.recipe_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
