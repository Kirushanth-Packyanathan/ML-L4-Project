from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
import pandas as pd
import pickle
import os

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

# ── Load pre-built .pkl model ──────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "house_price_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print(f"Model loaded successfully from {MODEL_PATH}")
print(f"Model type: {type(model)}")

# ── Feature Constants ──────────────────────────────────────────────────────────
DISTRICTS = [
    "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle",
    "Gampaha", "Hambantota", "Jaffna", "Kalutara", "Kandy",
    "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
    "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa",
    "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya"
]

AREAS = {
    "Ampara": ["Ampara Central"],
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

# Exact feature names the pkl model was trained on (108 total).
# Extracted directly from the XGBoost feature_names mismatch error.
# ALL categories are included - no reference-category dropping.
MODEL_FEATURE_NAMES = [
    "perch", "bedrooms", "bathrooms", "kitchen_area_sqft", "parking_spots",
    "has_garden", "has_ac", "floors", "house_age",
    # District one-hot (25 districts)
    "district_Ampara", "district_Anuradhapura", "district_Badulla",
    "district_Batticaloa", "district_Colombo", "district_Galle",
    "district_Gampaha", "district_Hambantota", "district_Jaffna",
    "district_Kalutara", "district_Kandy", "district_Kegalle",
    "district_Kilinochchi", "district_Kurunegala", "district_Mannar",
    "district_Matale", "district_Matara", "district_Monaragala",
    "district_Mullaitivu", "district_Nuwara Eliya", "district_Polonnaruwa",
    "district_Puttalam", "district_Ratnapura", "district_Trincomalee",
    "district_Vavuniya",
    # Area one-hot (all areas)
    "area_Akurugoda", "area_Ambalantota", "area_Ampara Central",
    "area_Badulla Town", "area_Bambalapitiya", "area_Bandarawela",
    "area_Batticaloa Town", "area_Beruwala", "area_Borella",
    "area_China Bay", "area_Chunnakam", "area_Dehiwala",
    "area_Eravur", "area_Galle Fort", "area_Gampaha Town",
    "area_Gatambe", "area_Hali Ela", "area_Hambantota Town",
    "area_Hikkaduwa", "area_Ja-Ela", "area_Jaffna Town",
    "area_Kadawatha", "area_Kallady", "area_Kalutara North",
    "area_Kandy City", "area_Karapitiya", "area_Katugastota",
    "area_Kegalle Central", "area_Kilinochchi Central", "area_Kokuvil",
    "area_Kollupitiya", "area_Kurunegala Town", "area_Kuruwita",
    "area_Madawachchiya", "area_Mannar Central", "area_Matale Central",
    "area_Matara Town", "area_Melsiripura", "area_Monaragala Central",
    "area_Mount Lavinia", "area_Mullaitivu Central", "area_Nallur",
    "area_Narahenpita", "area_Negombo", "area_New Town",
    "area_Nilaveli", "area_Nugegoda", "area_Nupe",
    "area_Nuwara Eliya Central", "area_Nuwaragam Palatha", "area_Panadura",
    "area_Pannala", "area_Pelmadulla", "area_Peradeniya", "area_Polgahawela",
    "area_Polonnaruwa Central", "area_Puttalam Central", "area_Ragama",
    "area_Rajagiriya", "area_Ratnapura Town", "area_Tangalle",
    "area_Tennekumbura", "area_Unawatuna", "area_Uppuveli",
    "area_Vavuniya Central", "area_Wadduwa", "area_Wattala",
    "area_Weligama", "area_Wellawatte",
    # Water supply - ALL 3 categories (no reference dropping)
    "water_supply_Both", "water_supply_Pipe-borne", "water_supply_Well",
    # Electricity - BOTH categories (no reference dropping)
    "electricity_Single phase", "electricity_Three phase",
]


# ── Pydantic Models ────────────────────────────────────────────────────────────
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


# ── Feature Engineering ────────────────────────────────────────────────────────
def build_feature_dataframe(house: HouseInput) -> pd.DataFrame:
    """Build a DataFrame with exactly the 108 features the model expects.

    ALL categorical columns are one-hot encoded with every category present
    (no reference-category dropping), matching the training-time pd.get_dummies
    behaviour with drop_first=False.
    """
    house_age = 2025 - house.year_built

    # Start with all features set to zero
    row = {col: 0.0 for col in MODEL_FEATURE_NAMES}

    # Numerical features
    row["perch"] = float(house.perch)
    row["bedrooms"] = float(house.bedrooms)
    row["bathrooms"] = float(house.bathrooms)
    row["kitchen_area_sqft"] = float(house.kitchen_area_sqft)
    row["parking_spots"] = float(house.parking_spots)
    row["has_garden"] = 1.0 if house.has_garden else 0.0
    row["has_ac"] = 1.0 if house.has_ac else 0.0
    row["floors"] = float(house.floors)
    row["house_age"] = float(house_age)

    # District one-hot
    d_col = f"district_{house.district}"
    if d_col in row:
        row[d_col] = 1.0

    # Area one-hot
    a_col = f"area_{house.area}"
    if a_col in row:
        row[a_col] = 1.0

    # Water supply one-hot (all 3 categories encoded)
    ws_col = f"water_supply_{house.water_supply}"
    if ws_col in row:
        row[ws_col] = 1.0

    # Electricity one-hot (both categories encoded)
    el_col = f"electricity_{house.electricity}"
    if el_col in row:
        row[el_col] = 1.0

    # Return DataFrame with columns in exact model order
    return pd.DataFrame([row], columns=MODEL_FEATURE_NAMES)


# ── Helpers ────────────────────────────────────────────────────────────────────
def format_lkr(amount: float) -> str:
    if amount >= 1_000_000:
        return f"Rs. {amount / 1_000_000:.2f} Million"
    elif amount >= 1_000:
        return f"Rs. {amount / 1_000:.2f}K"
    return f"Rs. {amount:.2f}"


# ── API Routes ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Sri Lanka House Price Prediction API",
        "version": "1.0.0",
        "model_type": type(model).__name__,
        "feature_count": len(MODEL_FEATURE_NAMES),
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": type(model).__name__,
        "feature_count": len(MODEL_FEATURE_NAMES),
    }


@app.get("/api/options", response_model=OptionsResponse, tags=["Options"])
async def get_options():
    return OptionsResponse(
        districts=DISTRICTS,
        areas=AREAS,
        water_supply_options=WATER_SUPPLY_OPTIONS,
        electricity_options=ELECTRICITY_OPTIONS,
    )


@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_price(house: HouseInput):
    if house.district not in DISTRICTS:
        raise HTTPException(status_code=400, detail=f"Invalid district: {house.district}")
    if house.district in AREAS and house.area not in AREAS[house.district]:
        raise HTTPException(status_code=400, detail=f"Invalid area '{house.area}' for district '{house.district}'")
    if house.water_supply not in WATER_SUPPLY_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid water supply: {house.water_supply}")
    if house.electricity not in ELECTRICITY_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid electricity: {house.electricity}")

    try:
        df = build_feature_dataframe(house)
        log_prediction = model.predict(df)
        # Model was trained on log-transformed prices — reverse with exp()
        predicted_price = max(float(np.exp(np.array(log_prediction).ravel()[0])), 0)

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
