from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import xgboost as xgb
import numpy as np
import os
import json

app = FastAPI(
    title="Sri Lanka House Price Predictor",
    description="Predict house prices across Sri Lanka using Machine Learning",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "house_price_model.json")

model = xgb.Booster()
model.load_model(MODEL_PATH)
print(f"Model loaded successfully from {MODEL_PATH}")

#Feature Constants
DISTRICTS = [
    "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle",
    "Gampaha", "Hambantota", "Jaffna", "Kalutara", "Kandy",
    "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
    "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa",
    "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya"
]

AREAS = {
    "Anuradhapura": ["Madawachchiya", "New Town", "Nuwaragam Palatha"],
    "Badulla": ["Badulla Town", "Bandarawela", "Hali Ela"],
    "Batticaloa": ["Batticaloa Town", "Eravur", "Kallady"],
    "Colombo": ["Bambalapitiya", "Borella", "Dehiwala", "Kollupitiya", "Mount Lavinia", "Narahenpita", "Nugegoda", "Rajagiriya", "Wellawatte"],
    "Galle": ["Galle Fort", "Hikkaduwa", "Karapitiya", "Unawatuna"],
    "Gampaha": ["Gampaha Town", "Ja-Ela", "Kadawatha", "Negombo", "Ragama", "Wattala"],
    "Hambantota": ["Ambalantota", "Hambantota Town", "Tangalle"],
    "Jaffna": ["Chunnakam", "Jaffna Town", "Kokuvil", "Nallur"],
    "Kalutara": ["Beruwala", "Kalutara North", "Panadura", "Wadduwa"],
    "Kandy": ["Gatambe", "Kandy City", "Katugastota", "Peradeniya", "Tennekumbura"],
    "Kegalle": ["Kegalle Central"],
    "Kilinochchi": ["Kilinochchi Central"],
    "Kurunegala": ["Kurunegala Town", "Melsiripura", "Pannala", "Polgahawela"],
    "Mannar": ["Mannar Central"],
    "Matale": ["Matale Central"],
    "Matara": ["Akurugoda", "Matara Town", "Nupe", "Weligama"],
    "Monaragala": ["Monaragala Central"],
    "Mullaitivu": ["Mullaitivu Central"],
    "Nuwara Eliya": ["Nuwara Eliya Central"],
    "Polonnaruwa": ["Polonnaruwa Central"],
    "Puttalam": ["Puttalam Central"],
    "Ratnapura": ["Kuruwita", "Pelmadulla", "Ratnapura Town"],
    "Trincomalee": ["China Bay", "Nilaveli", "Uppuveli"],
    "Vavuniya": ["Vavuniya Central"],
}

WATER_SUPPLY_OPTIONS = ["Both", "Pipe-borne", "Well"]
ELECTRICITY_OPTIONS = ["Single phase", "Three phase"]

# Feature names from the model (order matters!)
FEATURE_NAMES = [
    "perch", "bedrooms", "bathrooms", "kitchen_area_sqft", "parking_spots",
    "has_garden", "has_ac", "floors", "house_age",
    # District one-hot (24 districts, but only 22 in model after dropping 2 for reference)
    "district_Anuradhapura", "district_Badulla", "district_Batticaloa",
    "district_Colombo", "district_Galle", "district_Gampaha",
    "district_Hambantota", "district_Jaffna", "district_Kalutara",
    "district_Kandy", "district_Kegalle", "district_Kilinochchi",
    "district_Kurunegala", "district_Mannar", "district_Matale",
    "district_Matara", "district_Monaragala", "district_Mullaitivu",
    "district_Nuwara Eliya", "district_Polonnaruwa", "district_Puttalam",
    "district_Ratnapura", "district_Trincomalee", "district_Vavuniya",
    # Area one-hot
    "area_Ambalantota", "area_Ampara Central", "area_Badulla Town",
    "area_Bambalapitiya", "area_Bandarawela", "area_Batticaloa Town",
    "area_Beruwala", "area_Borella", "area_China Bay", "area_Chunnakam",
    "area_Dehiwala", "area_Eravur", "area_Galle Fort", "area_Gampaha Town",
    "area_Gatambe", "area_Hali Ela", "area_Hambantota Town", "area_Hikkaduwa",
    "area_Ja-Ela", "area_Jaffna Town", "area_Kadawatha", "area_Kallady",
    "area_Kalutara North", "area_Kandy City", "area_Karapitiya",
    "area_Katugastota", "area_Kegalle Central", "area_Kilinochchi Central",
    "area_Kokuvil", "area_Kollupitiya", "area_Kurunegala Town",
    "area_Kuruwita", "area_Madawachchiya", "area_Mannar Central",
    "area_Matale Central", "area_Matara Town", "area_Melsiripura",
    "area_Monaragala Central", "area_Mount Lavinia", "area_Mullaitivu Central",
    "area_Nallur", "area_Narahenpita", "area_Negombo", "area_New Town",
    "area_Nilaveli", "area_Nugegoda", "area_Nupe",
    "area_Nuwara Eliya Central", "area_Nuwaragam Palatha", "area_Panadura",
    "area_Pannala", "area_Pelmadulla", "area_Peradeniya", "area_Polgahawela",
    "area_Polonnaruwa Central", "area_Puttalam Central", "area_Ragama",
    "area_Rajagiriya", "area_Ratnapura Town", "area_Tangalle",
    "area_Tennekumbura", "area_Unawatuna", "area_Uppuveli",
    "area_Vavuniya Central", "area_Wadduwa", "area_Wattala", "area_Weligama",
    "area_Wellawatte",
    # Water supply one-hot (2 features, "Both" is reference)
    "water_supply_Pipe-borne", "water_supply_Well",
    # Electricity one-hot (1 feature, "Single phase" is reference)
    "electricity_Three phase",
]


class HouseInput(BaseModel):
    district: str = Field(..., description="District name")
    area: str = Field(..., description="Area name within the district")
    perch: int = Field(..., ge=1, le=100, description="Land size in perches")
    bedrooms: int = Field(..., ge=1, le=10, description="Number of bedrooms")
    bathrooms: int = Field(..., ge=1, le=10, description="Number of bathrooms")
    kitchen_area_sqft: int = Field(..., ge=20, le=300, description="Kitchen area in sq ft")
    parking_spots: int = Field(..., ge=0, le=5, description="Number of parking spots")
    has_garden: bool = Field(..., description="Whether the house has a garden")
    has_ac: bool = Field(..., description="Whether the house has AC")
    water_supply: str = Field(..., description="Water supply type")
    electricity: str = Field(..., description="Electricity type")
    floors: int = Field(..., ge=1, le=5, description="Number of floors")
    year_built: int = Field(..., ge=1980, le=2026, description="Year the house was built")


class PredictionResponse(BaseModel):
    predicted_price_lkr: float
    predicted_price_formatted: str
    input_summary: dict


class OptionsResponse(BaseModel):
    districts: list[str]
    areas: dict[str, list[str]]
    water_supply_options: list[str]
    electricity_options: list[str]


def prepare_features(house: HouseInput) -> np.ndarray:
    """Convert HouseInput to feature array matching model's expected input."""
    
    # Calculate house_age (reference year from dataset is 2025)
    house_age = 2025 - house.year_built
    
    features = np.zeros(len(FEATURE_NAMES), dtype=np.float32)
    
    # Numerical features
    features[0] = house.perch
    features[1] = house.bedrooms
    features[2] = house.bathrooms
    features[3] = house.kitchen_area_sqft
    features[4] = house.parking_spots
    features[5] = 1 if house.has_garden else 0
    features[6] = 1 if house.has_ac else 0
    features[7] = house.floors
    features[8] = house_age
    
    # District one-hot
    district_col = f"district_{house.district}"
    if district_col in FEATURE_NAMES:
        features[FEATURE_NAMES.index(district_col)] = 1
    
    # Area one-hot
    area_col = f"area_{house.area}"
    if area_col in FEATURE_NAMES:
        features[FEATURE_NAMES.index(area_col)] = 1
    
    # Water supply one-hot
    if house.water_supply == "Pipe-borne":
        features[FEATURE_NAMES.index("water_supply_Pipe-borne")] = 1
    elif house.water_supply == "Well":
        features[FEATURE_NAMES.index("water_supply_Well")] = 1
    # "Both" is the reference category (all zeros)
    
    # Electricity one-hot
    if house.electricity == "Three phase":
        features[FEATURE_NAMES.index("electricity_Three phase")] = 1
    # "Single phase" is the reference category (zero)
    
    return features


def format_lkr(amount: float) -> str:
    """Format amount as Sri Lankan Rupees."""
    if amount >= 1_000_000:
        return f"Rs. {amount / 1_000_000:.2f} Million"
    elif amount >= 1_000:
        return f"Rs. {amount / 1_000:.2f}K"
    else:
        return f"Rs. {amount:.2f}"


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "🏠 Sri Lanka House Price Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/predict",
            "options": "/api/options",
            "health": "/api/health",
        }
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "model_loaded": True}


@app.get("/api/options", response_model=OptionsResponse, tags=["Options"])
async def get_options():
    """Get all available dropdown options for the prediction form."""
    return OptionsResponse(
        districts=DISTRICTS,
        areas=AREAS,
        water_supply_options=WATER_SUPPLY_OPTIONS,
        electricity_options=ELECTRICITY_OPTIONS,
    )


@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_price(house: HouseInput):
    """Predict the price of a house based on input features."""

    # Validate district
    if house.district not in DISTRICTS:
        raise HTTPException(status_code=400, detail=f"Invalid district: {house.district}")
    
    # Validate area
    if house.district in AREAS and house.area not in AREAS[house.district]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid area '{house.area}' for district '{house.district}'"
        )
    
    # Validate water supply
    if house.water_supply not in WATER_SUPPLY_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid water supply: {house.water_supply}")
    
    # Validate electricity
    if house.electricity not in ELECTRICITY_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid electricity: {house.electricity}")
    
    try:
        features = prepare_features(house)
        dmatrix = xgb.DMatrix(features.reshape(1, -1), feature_names=FEATURE_NAMES)
        prediction = model.predict(dmatrix)[0]

        # Ensure prediction is positive
        predicted_price = max(float(prediction), 0)
        
        return PredictionResponse(
            predicted_price_lkr=round(predicted_price, 2),
            predicted_price_formatted=format_lkr(predicted_price),
            input_summary={
                "district": house.district,
                "area": house.area,
                "perch": house.perch,
                "bedrooms": house.bedrooms,
                "bathrooms": house.bathrooms,
                "kitchen_area_sqft": house.kitchen_area_sqft,
                "parking_spots": house.parking_spots,
                "has_garden": house.has_garden,
                "has_ac": house.has_ac,
                "water_supply": house.water_supply,
                "electricity": house.electricity,
                "floors": house.floors,
                "year_built": house.year_built,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
