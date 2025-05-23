from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
import json
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load meal data from JSON file
def load_meals_data():
    file_path = os.path.join(os.path.dirname(__file__), "DEdata.json")
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: DEdata.json not found at {file_path}")
        return []

class Meal(BaseModel):
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    category: str

def generate_daily_plan(target_macros):
    meals_data = load_meals_data()
    
    # Categorize meals
    breakfast_options = [m for m in meals_data if m["category"] == "Breakfast"]
    lunch_options = [m for m in meals_data if m["category"] == "Lunch"]
    dinner_options = [m for m in meals_data if m["category"] == "Dinner"]
    snack_options = [m for m in meals_data if m["category"] == "Snack"]
    
    # Simple selection based on target macros
    daily_plan = {
        "breakfast": random.choice(breakfast_options),
        "lunch": random.choice(lunch_options),
        "dinner": random.choice(dinner_options),
        "snack": random.choice(snack_options)
    }
    
    return daily_plan

@app.get("/")
async def root():
    return {"message": "Diet Plan API is running"}

@app.get("/test")
async def test():
    return {"status": "OK", "message": "API is working"}

@app.get("/weekly-plan")
async def get_weekly_plan(
    target_calories: float = Query(...),
    target_protein: float = Query(...),
    target_fat: float = Query(...),
    target_carbs: float = Query(...)
):
    try:
        print(f"Received request with targets: calories={target_calories}, protein={target_protein}, fat={target_fat}, carbs={target_carbs}")
        
        target_macros = {
            "calories": target_calories,
            "protein": target_protein,
            "fat": target_fat,
            "carbs": target_carbs
        }
        
        meals_data = load_meals_data()
        if not meals_data:
            raise Exception("No meal data available")
            
        weekly_plan = []
        for day in range(7):
            daily_plan = generate_daily_plan(target_macros)
            daily_plan["day"] = f"Day {day + 1}"
            weekly_plan.append(daily_plan)
        
        print(f"Generated plan: {weekly_plan}")
        return weekly_plan
    
    except Exception as e:
        print(f"Error generating meal plan: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
