from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np
import pandas as pd
import pickle
import os
import io
import base64

app = FastAPI(
    title="Sri Lanka House Price Predictor",
    description="Predict house prices across Sri Lanka using ML with Explainable AI",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model ─────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "house_price_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print(f"Model loaded: {type(model).__name__}")

# ── Try SHAP TreeExplainer (XGBoost 2.x has known compatibility issues) ────────
EXPLAINER      = None
EXPLAINER_TYPE = "importance"   # "shap" | "importance"

def _try_init_shap():
    global EXPLAINER, EXPLAINER_TYPE
    try:
        import shap as _shap

        # Build a properly named smoke-test row (all zeros)
        _dummy = pd.DataFrame(
            [[0.0] * len(MODEL_FEATURE_NAMES)],
            columns=MODEL_FEATURE_NAMES
        )

        # Attempt 1: sklearn wrapper
        try:
            _exp = _shap.TreeExplainer(model)
            _sv  = _exp.shap_values(_dummy)   # smoke test
            _ = float(np.array(_sv).ravel()[0])  # ensure castable
            EXPLAINER      = _exp
            EXPLAINER_TYPE = "shap"
            print("SHAP TreeExplainer (sklearn wrapper) ready.")
            return
        except BaseException as _e1:
            print(f"SHAP attempt 1 failed: {_e1}")

        # Attempt 2: raw XGBoost booster
        try:
            _booster = model.get_booster()
            _exp2    = _shap.TreeExplainer(_booster)
            _sv2     = _exp2.shap_values(_dummy)
            _ = float(np.array(_sv2).ravel()[0])
            EXPLAINER      = _exp2
            EXPLAINER_TYPE = "shap"
            print("SHAP TreeExplainer (booster) ready.")
            return
        except BaseException as _e2:
            print(f"SHAP attempt 2 failed: {_e2}")

        print("SHAP unavailable — using XGBoost gain-importance fallback.")

    except ImportError:
        print("SHAP not installed — using XGBoost gain-importance fallback.")
    except BaseException as _catch_all:
        print(f"SHAP init unexpected error: {_catch_all}. Using fallback.")

_try_init_shap()

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
    "Colombo": ["Bambalapitiya", "Borella", "Dehiwala", "Kollupitiya", "Mount Lavinia",
                 "Narahenpita", "Nugegoda", "Rajagiriya", "Wellawatte"],
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
ELECTRICITY_OPTIONS  = ["Single phase", "Three phase"]

MODEL_FEATURE_NAMES = [
    "perch", "bedrooms", "bathrooms", "kitchen_area_sqft", "parking_spots",
    "has_garden", "has_ac", "floors", "house_age",
    "district_Ampara", "district_Anuradhapura", "district_Badulla",
    "district_Batticaloa", "district_Colombo", "district_Galle",
    "district_Gampaha", "district_Hambantota", "district_Jaffna",
    "district_Kalutara", "district_Kandy", "district_Kegalle",
    "district_Kilinochchi", "district_Kurunegala", "district_Mannar",
    "district_Matale", "district_Matara", "district_Monaragala",
    "district_Mullaitivu", "district_Nuwara Eliya", "district_Polonnaruwa",
    "district_Puttalam", "district_Ratnapura", "district_Trincomalee",
    "district_Vavuniya",
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
    "water_supply_Both", "water_supply_Pipe-borne", "water_supply_Well",
    "electricity_Single phase", "electricity_Three phase",
]

FEATURE_LABELS = {
    "perch":             "Land Size (Perches)",
    "bedrooms":          "Bedrooms",
    "bathrooms":         "Bathrooms",
    "kitchen_area_sqft": "Kitchen Area (sq ft)",
    "parking_spots":     "Parking Spots",
    "has_garden":        "Garden",
    "has_ac":            "Air Conditioning",
    "floors":            "Number of Floors",
    "house_age":         "House Age (years)",
}

def _label(fname: str) -> str:
    if fname in FEATURE_LABELS:
        return FEATURE_LABELS[fname]
    if fname.startswith("district_"):    return f"District: {fname[9:]}"
    if fname.startswith("area_"):        return f"Area: {fname[5:]}"
    if fname.startswith("water_supply_"):return f"Water Supply: {fname[13:]}"
    if fname.startswith("electricity_"): return f"Electricity: {fname[12:]}"
    return fname

# Pre-compute gain-based feature importances (fallback)
GAIN_IMPORTANCES = dict(zip(MODEL_FEATURE_NAMES,
                             model.feature_importances_.tolist()))


# ── Pydantic Models ────────────────────────────────────────────────────────────
class HouseInput(BaseModel):
    district:          str = Field(...)
    area:              str = Field(...)
    perch:             int = Field(..., ge=1,   le=100)
    bedrooms:          int = Field(..., ge=1,   le=10)
    bathrooms:         int = Field(..., ge=1,   le=10)
    kitchen_area_sqft: int = Field(..., ge=20,  le=300)
    parking_spots:     int = Field(..., ge=0,   le=5)
    has_garden:       bool = Field(...)
    has_ac:           bool = Field(...)
    water_supply:      str = Field(...)
    electricity:       str = Field(...)
    floors:            int = Field(..., ge=1,   le=5)
    year_built:        int = Field(..., ge=1980, le=2026)


class FeatureContribution(BaseModel):
    feature:       str
    label:         str
    value:         float   # shap value or importance score
    direction:     str     # "increase" | "decrease" | "neutral"
    percentage:    float
    method:        str     # "shap" | "gain_importance"


class PredictionResponse(BaseModel):
    predicted_price_lkr:       float
    predicted_price_formatted:  str
    base_price_lkr:            float
    input_summary:             dict
    feature_contributions:     list[FeatureContribution]
    explainer_method:          str


class OptionsResponse(BaseModel):
    districts:            list[str]
    areas:                dict[str, list[str]]
    water_supply_options: list[str]
    electricity_options:  list[str]


# ── Feature Engineering ────────────────────────────────────────────────────────
def build_feature_dataframe(house: HouseInput) -> pd.DataFrame:
    house_age = 2025 - house.year_built
    row = {col: 0.0 for col in MODEL_FEATURE_NAMES}
    row["perch"]             = float(house.perch)
    row["bedrooms"]          = float(house.bedrooms)
    row["bathrooms"]         = float(house.bathrooms)
    row["kitchen_area_sqft"] = float(house.kitchen_area_sqft)
    row["parking_spots"]     = float(house.parking_spots)
    row["has_garden"]        = 1.0 if house.has_garden else 0.0
    row["has_ac"]            = 1.0 if house.has_ac     else 0.0
    row["floors"]            = float(house.floors)
    row["house_age"]         = float(house_age)
    for col in [f"district_{house.district}", f"area_{house.area}",
                f"water_supply_{house.water_supply}", f"electricity_{house.electricity}"]:
        if col in row:
            row[col] = 1.0
    return pd.DataFrame([row], columns=MODEL_FEATURE_NAMES)


def format_lkr(amount: float) -> str:
    if amount >= 1_000_000:
        return f"Rs. {amount / 1_000_000:.2f} Million"
    if amount >= 1_000:
        return f"Rs. {amount / 1_000:.2f}K"
    return f"Rs. {amount:.2f}"


def compute_shap_contributions(df: pd.DataFrame) -> tuple[list[FeatureContribution], str]:
    """Try SHAP first, fall back to gain-based importance."""
    if EXPLAINER is not None and EXPLAINER_TYPE == "shap":
        try:
            sv_raw = EXPLAINER.shap_values(df)
            sv     = np.array(sv_raw, dtype=float).ravel()

            contribs = []
            for i, fname in enumerate(MODEL_FEATURE_NAMES):
                v = float(sv[i])
                if abs(v) < 1e-6:
                    continue
                contribs.append({"feature": fname, "label": _label(fname),
                                  "value": v, "direction": "increase" if v > 0 else "decrease"})

            contribs.sort(key=lambda x: abs(x["value"]), reverse=True)
            top = contribs[:10]
            total = sum(abs(c["value"]) for c in top) or 1.0
            return [
                FeatureContribution(feature=c["feature"], label=c["label"],
                                    value=round(c["value"], 5), direction=c["direction"],
                                    percentage=round(abs(c["value"]) / total * 100, 1),
                                    method="shap")
                for c in top
            ], "SHAP (TreeExplainer)"
        except Exception:
            pass  # fall through to importance fallback

    # ── Gain-based importance fallback ──
    # For non-zero features blended with global importance
    feat_vals = df.iloc[0].to_dict()
    contribs = []
    for fname, importance in GAIN_IMPORTANCES.items():
        if importance < 1e-8:
            continue
        fv = feat_vals.get(fname, 0.0)
        # For one-hot features, only include if active (=1)
        is_ohe = any(fname.startswith(p) for p in ("district_", "area_", "water_", "electricity_"))
        if is_ohe and fv < 0.5:
            continue
        # Weighted score: importance * (value for numerical, 1 for OHE)
        score = importance * (abs(fv) if not is_ohe else 1.0)
        contribs.append({"feature": fname, "label": _label(fname),
                          "value": score, "direction": "increase"})

    contribs.sort(key=lambda x: x["value"], reverse=True)
    top   = contribs[:10]
    total = sum(c["value"] for c in top) or 1.0
    return [
        FeatureContribution(feature=c["feature"], label=c["label"],
                            value=round(c["value"], 5), direction="increase",
                            percentage=round(c["value"] / total * 100, 1),
                            method="gain_importance")
        for c in top
    ], "XGBoost Feature Importance (Gain)"


# ── API Routes ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Sri Lanka House Price Prediction API", "version": "2.0.0",
            "explainer": EXPLAINER_TYPE, "feature_count": len(MODEL_FEATURE_NAMES)}


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "model_loaded": True,
            "explainer_type": EXPLAINER_TYPE, "model_type": type(model).__name__}


@app.get("/api/options", response_model=OptionsResponse, tags=["Options"])
async def get_options():
    return OptionsResponse(districts=DISTRICTS, areas=AREAS,
                           water_supply_options=WATER_SUPPLY_OPTIONS,
                           electricity_options=ELECTRICITY_OPTIONS)


@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_price(house: HouseInput):
    if house.district not in DISTRICTS:
        raise HTTPException(400, f"Invalid district: {house.district}")
    if house.district in AREAS and house.area not in AREAS[house.district]:
        raise HTTPException(400, f"Invalid area '{house.area}' for '{house.district}'")
    if house.water_supply not in WATER_SUPPLY_OPTIONS:
        raise HTTPException(400, f"Invalid water supply: {house.water_supply}")
    if house.electricity not in ELECTRICITY_OPTIONS:
        raise HTTPException(400, f"Invalid electricity: {house.electricity}")

    try:
        df = build_feature_dataframe(house)

        log_pred        = float(np.squeeze(model.predict(df)))
        predicted_price = max(float(np.exp(log_pred)), 0)

        # Compute base price using mean of log predictions ≈ expected value
        # We estimate it from the model's base score or use a fixed reference
        try:
            base_log   = float(model.get_params().get("base_score", 0.5))
            base_price = float(np.exp(base_log))
        except Exception:
            base_price = 0.0

        contributions, method = compute_shap_contributions(df)

        return PredictionResponse(
            predicted_price_lkr=round(predicted_price, 2),
            predicted_price_formatted=format_lkr(predicted_price),
            base_price_lkr=round(base_price, 2),
            input_summary={
                "district": house.district, "area": house.area,
                "perch": house.perch, "bedrooms": house.bedrooms,
                "bathrooms": house.bathrooms, "kitchen_area_sqft": house.kitchen_area_sqft,
                "parking_spots": house.parking_spots, "has_garden": house.has_garden,
                "has_ac": house.has_ac, "water_supply": house.water_supply,
                "electricity": house.electricity, "floors": house.floors,
                "year_built": house.year_built,
            },
            feature_contributions=contributions,
            explainer_method=method,
        )

    except Exception as e:
        raise HTTPException(500, f"Prediction failed: {str(e)}")


# ── SHAP Plot Endpoint ────────────────────────────────────────────────────────
@app.post("/api/shap-plot", tags=["Explanation"])
async def shap_plot(house: HouseInput):
    """Return a base64-encoded PNG of the SHAP waterfall (or importance) chart."""
    import matplotlib
    matplotlib.use("Agg")          # headless – no display needed
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    # ── Build feature dataframe ──
    if house.district not in DISTRICTS:
        raise HTTPException(400, f"Invalid district: {house.district}")

    df = build_feature_dataframe(house)

    # ── Colour palette (dark theme matching the Streamlit UI) ──
    BG      = "#141B2D"
    SURFACE = "#1A2340"
    TEXT    = "#E8EAF0"
    TEXT2   = "#8892A4"
    GREEN   = "#10D9A0"
    RED     = "#F56565"
    BLUE    = "#4F8EF7"
    ORANGE  = "#FF6B2B"
    GRID    = "rgba(255,255,255,0.06)"

    try:
        # ════════════ SHAP waterfall path ════════════
        if EXPLAINER is not None and EXPLAINER_TYPE == "shap":
            import shap
            sv_raw = EXPLAINER.shap_values(df)
            sv     = np.array(sv_raw, dtype=float).ravel()

            # Build (label, value) pairs, sort by |value|, take top 10
            pairs = []
            for i, fname in enumerate(MODEL_FEATURE_NAMES):
                v = float(sv[i])
                if abs(v) < 1e-4:
                    continue
                pairs.append((_label(fname), v))
            pairs.sort(key=lambda x: abs(x[1]), reverse=True)
            pairs = pairs[:10]
            pairs.reverse()          # bottom-to-top so largest is at top

            labels = [p[0] for p in pairs]
            values = [p[1] for p in pairs]
            colors = [GREEN if v > 0 else RED for v in values]

            fig, ax = plt.subplots(figsize=(9, 5))
            fig.patch.set_facecolor(BG)
            ax.set_facecolor(SURFACE)

            bars = ax.barh(labels, values, color=colors,
                           height=0.6, edgecolor="none", zorder=3)

            # Value annotations
            for bar, val in zip(bars, values):
                sign = "+" if val > 0 else ""
                ax.text(
                    bar.get_width() + (max(abs(v) for v in values) * 0.015 * (1 if val > 0 else -1)),
                    bar.get_y() + bar.get_height() / 2,
                    f"{sign}Rs.{val/1e6:.2f}M" if abs(val) >= 1e6 else f"{sign}Rs.{val/1e3:.1f}K",
                    va="center", ha="left" if val >= 0 else "right",
                    color=GREEN if val > 0 else RED,
                    fontsize=8.5, fontweight="bold"
                )

            ax.axvline(0, color=TEXT2, linewidth=0.8, zorder=2)
            ax.set_xlabel("SHAP Value (impact on price)", color=TEXT2, fontsize=10)
            ax.set_title("SHAP Waterfall — Feature Impact on Price",
                         color=TEXT, fontsize=12, fontweight="bold", pad=14)

            graph_type = "SHAP (TreeExplainer)"

        else:
            # ════════════ Gain importance fallback ════════════
            feat_vals = df.iloc[0].to_dict()
            pairs = []
            for fname, importance in GAIN_IMPORTANCES.items():
                if importance < 1e-8:
                    continue
                fv = feat_vals.get(fname, 0.0)
                is_ohe = any(fname.startswith(p) for p in ("district_","area_","water_","electricity_"))
                if is_ohe and fv < 0.5:
                    continue
                score = importance * (abs(fv) if not is_ohe else 1.0)
                pairs.append((_label(fname), score))

            pairs.sort(key=lambda x: x[1])
            pairs = pairs[-10:]

            labels = [p[0] for p in pairs]
            values = [p[1] for p in pairs]
            colors = [BLUE] * len(values)

            fig, ax = plt.subplots(figsize=(9, 5))
            fig.patch.set_facecolor(BG)
            ax.set_facecolor(SURFACE)

            bars = ax.barh(labels, values, color=colors,
                           height=0.6, edgecolor="none", zorder=3)

            max_val = max(values) or 1.0
            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_width() + max_val * 0.015,
                    bar.get_y() + bar.get_height() / 2,
                    f"{val:.3f}",
                    va="center", ha="left",
                    color=BLUE, fontsize=8.5, fontweight="bold"
                )

            ax.set_xlabel("Feature Importance (Gain)", color=TEXT2, fontsize=10)
            ax.set_title("XGBoost Feature Importance — Top Factors",
                         color=TEXT, fontsize=12, fontweight="bold", pad=14)

            graph_type = "XGBoost Gain Importance"

        # ── Shared styling ──
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(colors=TEXT2, labelsize=9)
        ax.xaxis.label.set_color(TEXT2)
        ax.yaxis.set_tick_params(labelcolor=TEXT)
        ax.set_yticklabels(labels, fontsize=9.5)
        ax.grid(axis="x", color="#2A3550", linewidth=0.7, zorder=1)
        ax.set_xlim(left=min(0, min(values)) * 1.25 if values else 0,
                    right=max(values) * 1.22 if values else 1)

        # Legend
        if EXPLAINER_TYPE == "shap":
            up_patch   = mpatches.Patch(color=GREEN, label="↑ Increases price")
            down_patch  = mpatches.Patch(color=RED,   label="↓ Decreases price")
            ax.legend(handles=[up_patch, down_patch], loc="lower right",
                      facecolor=SURFACE, edgecolor="#2A3550",
                      labelcolor=TEXT, fontsize=9)

        plt.tight_layout(pad=1.5)

        # ── Encode to base64 ──
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                    facecolor=BG, edgecolor="none")
        plt.close(fig)
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")

        return JSONResponse({"image": img_b64, "graph_type": graph_type})

    except Exception as e:
        raise HTTPException(500, f"Plot generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
