import streamlit as st
import requests
import json


st.set_page_config(
    page_title="🏡 Sri Lanka House Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Global Reset ── */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(160deg, #0a0a1a 0%, #0d1b2a 30%, #1b0a2e 60%, #0a0a1a 100%);
    }

    /* Hide defaults */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Hero Section ── */
    .hero {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
        position: relative;
    }
    .hero-emoji {
        font-size: 3rem;
        display: inline-block;
        animation: bounce 2s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.4));
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #a78bfa 40%, #06b6d4 70%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0 0.3rem;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .hero-sub {
        color: rgba(165, 165, 201, 0.8);
        font-size: 0.95rem;
        font-weight: 300;
        margin-bottom: 0.8rem;
    }
    .hero-badges {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        flex-wrap: wrap;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.7rem;
        letter-spacing: 0.03em;
        color: rgba(165, 165, 201, 0.9);
        padding: 0.3rem 0.75rem;
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 100px;
        font-weight: 500;
    }
    .hero-badge-dot {
        width: 5px; height: 5px;
        border-radius: 50%;
        background: #34d399;
        display: inline-block;
    }

    /* ── Glass Card ── */
    .glass-card {
        background: rgba(15, 15, 40, 0.5);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow:
            0 4px 30px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        margin-bottom: 1rem;
    }

    .card-title {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(167, 139, 250, 0.9);
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }

    /* ── Price Result ── */
    .price-hero {
        text-align: center;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.08) 50%, rgba(52, 211, 153, 0.06) 100%);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.12);
        margin: 0.5rem 0 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .price-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(99, 102, 241, 0.06), transparent 60%);
        pointer-events: none;
    }
    .price-tag {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: rgba(165, 165, 201, 0.7);
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
    .price-main {
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #34d399 0%, #22d3ee 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .price-sub {
        font-size: 0.85rem;
        color: rgba(165, 165, 201, 0.6);
        margin-top: 0.4rem;
        font-weight: 400;
    }

    /* ── Summary Grid ── */
    .detail-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 0.5rem;
    }
    @media (max-width: 768px) {
        .detail-grid { grid-template-columns: 1fr 1fr; }
    }
    .detail-item {
        padding: 0.6rem 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        transition: all 0.2s ease;
    }
    .detail-item:hover {
        background: rgba(99, 102, 241, 0.06);
        border-color: rgba(99, 102, 241, 0.12);
    }
    .detail-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(165, 165, 201, 0.5);
        font-weight: 600;
    }
    .detail-value {
        font-size: 0.85rem;
        color: #f0f0ff;
        font-weight: 600;
        margin-top: 0.1rem;
    }

    /* ── Insight Metric ── */
    .insight-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        margin-bottom: 0.8rem;
    }
    .insight-card {
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        text-align: center;
    }
    .insight-number {
        font-size: 1.2rem;
        font-weight: 800;
        color: #a78bfa;
        letter-spacing: -0.02em;
    }
    .insight-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(165, 165, 201, 0.5);
        font-weight: 600;
        margin-top: 0.15rem;
    }

    /* ── Comparison Bar ── */
    .comparison-bar {
        padding: 0.8rem 1rem;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .comparison-up {
        background: rgba(52, 211, 153, 0.08);
        border: 1px solid rgba(52, 211, 153, 0.15);
        color: #34d399;
    }
    .comparison-down {
        background: rgba(6, 182, 212, 0.08);
        border: 1px solid rgba(6, 182, 212, 0.15);
        color: #22d3ee;
    }

    /* ── Empty State ── */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
    }
    .empty-icon {
        font-size: 4rem;
        opacity: 0.15;
        margin-bottom: 0.8rem;
        display: block;
    }
    .empty-text {
        color: rgba(165, 165, 201, 0.4);
        font-size: 0.9rem;
        line-height: 1.8;
        font-weight: 400;
    }
    .empty-text strong {
        color: rgba(167, 139, 250, 0.6);
    }

    /* ── Form Styling ── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        color: #f0f0ff !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div:focus-within {
        border-color: rgba(167, 139, 250, 0.4) !important;
        box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.08) !important;
    }
    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: rgba(165, 165, 201, 0.7) !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Toggle */
    .stCheckbox label span {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45) !important;
        background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.15), transparent);
        margin: 0.8rem 0;
        border: none;
    }

    /* Category label */
    .form-category {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(167, 139, 250, 0.7);
        margin: 0.6rem 0 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: rgba(165, 165, 201, 0.3);
        font-size: 0.72rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    .app-footer strong {
        color: rgba(167, 139, 250, 0.5);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 0.8rem;
        padding: 0.5rem 1.2rem;
        color: rgba(165, 165, 201, 0.6);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.15) !important;
        color: #a78bfa !important;
    }
    .stTabs [data-baseweb="tab-border"] { display: none; }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* ── Loading Spinner ── */
    .loading-container {
        text-align: center;
        padding: 3rem 2rem;
    }
    .spinner-ring {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 3px solid rgba(167, 139, 250, 0.1);
        border-top: 3px solid #a78bfa;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 1rem;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    .loading-text {
        color: rgba(165, 165, 201, 0.7);
        font-size: 0.9rem;
        font-weight: 500;
    }
    .loading-sub {
        color: rgba(165, 165, 201, 0.4);
        font-size: 0.75rem;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)



API_BASE = "http://localhost:8000"

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

WATER_SUPPLY = ["Both", "Pipe-borne", "Well"]
ELECTRICITY = ["Single phase", "Three phase"]


def format_lkr(amount: float) -> str:
    if amount >= 1_000_000:
        return f"Rs. {amount / 1_000_000:.2f} M"
    elif amount >= 1_000:
        return f"Rs. {amount / 1_000:.1f}K"
    return f"Rs. {amount:.0f}"


def check_backend():
    try:
        r = requests.get(f"{API_BASE}/api/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


st.markdown("""
<div class="hero">
    <span class="hero-emoji">🏡</span>
    <h1>Sri Lanka House Price Predictor</h1>
    <p class="hero-sub">Get instant AI-powered property valuations across 24 districts</p>
    <div class="hero-badges">
        <span class="hero-badge"><span class="hero-badge-dot"></span> XGBoost Model</span>
        <span class="hero-badge"><span class="hero-badge-dot"></span> 20K+ Data Points</span>
        <span class="hero-badge"><span class="hero-badge-dot"></span> 24 Districts</span>
        <span class="hero-badge"><span class="hero-badge-dot"></span> 70+ Areas</span>
    </div>
</div>
""", unsafe_allow_html=True)


backend_ok = check_backend()
if not backend_ok:
    st.error("⚠️ **Backend not running!** Start FastAPI: `cd backend && .\\venv\\Scripts\\python -m uvicorn main:app --port 8000`")


form_col, spacer, result_col = st.columns([5, 0.5, 5])

with form_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 Property Details</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-category">📍 Location</div>', unsafe_allow_html=True)
    loc1, loc2 = st.columns(2)
    with loc1:
        district = st.selectbox("District", DISTRICTS, index=DISTRICTS.index("Colombo"), key="district")
    with loc2:
        available_areas = AREAS.get(district, [])
        area = st.selectbox("Area", available_areas, key="area")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="form-category">📐 Size & Structure</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        perch = st.number_input("Land (Perches)", min_value=1, max_value=100, value=10, key="perch")
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3, key="bed")
    with s2:
        kitchen_area = st.number_input("Kitchen (sq ft)", min_value=20, max_value=300, value=100, key="kitchen")
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2, key="bath")
    with s3:
        floors = st.number_input("Floors", min_value=1, max_value=5, value=1, key="floors")
        parking = st.number_input("Parking Spots", min_value=0, max_value=5, value=1, key="park")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="form-category">⚡ Amenities & Utilities</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        has_garden = st.checkbox("🌿 Garden", value=True, key="garden")
    with a2:
        has_ac = st.checkbox("❄️ AC", value=False, key="ac")
    with a3:
        water_supply = st.selectbox("💧 Water", WATER_SUPPLY, key="water")
    with a4:
        electricity = st.selectbox("⚡ Electricity", ELECTRICITY, key="elec")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="form-category">📅 Construction Year</div>', unsafe_allow_html=True)
    year_built = st.number_input("Year Built", min_value=1980, max_value=2026, value=2020, step=1, key="year")

    st.markdown("", unsafe_allow_html=True)


    predict_btn = st.button("🔮  Predict Price", use_container_width=True, type="primary", disabled=not backend_ok)

    st.markdown('</div>', unsafe_allow_html=True)


if predict_btn:
    payload = {
        "district": district, "area": area, "perch": perch,
        "bedrooms": bedrooms, "bathrooms": bathrooms,
        "kitchen_area_sqft": kitchen_area, "parking_spots": parking,
        "has_garden": has_garden, "has_ac": has_ac,
        "water_supply": water_supply, "electricity": electricity,
        "floors": floors, "year_built": year_built,
    }
    st.session_state["loading"] = True
    try:
        r = requests.post(f"{API_BASE}/api/predict", json=payload, timeout=10)
        if r.status_code == 200:
            st.session_state["result"] = r.json()
            st.session_state["payload"] = payload
        else:
            st.session_state["error"] = r.json().get("detail", "Unknown error")
    except requests.exceptions.ConnectionError:
        st.session_state["error"] = "Cannot connect to backend server."
    except Exception as e:
        st.session_state["error"] = str(e)
    finally:
        st.session_state["loading"] = False


with result_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Prediction Result</div>', unsafe_allow_html=True)

    if st.session_state.get("loading", False):
        st.markdown("""
        <div class="loading-container">
            <div class="spinner-ring"></div>
            <div class="loading-text">🔮 Running prediction model...</div>
            <div class="loading-sub">Analyzing property features with XGBoost</div>
        </div>
        """, unsafe_allow_html=True)

    if "error" in st.session_state:
        st.error(f"❌ {st.session_state['error']}")
        del st.session_state["error"]

    if "result" in st.session_state:
        result = st.session_state["result"]
        payload = st.session_state["payload"]
        price_lkr = result["predicted_price_lkr"]
        price_fmt = result["predicted_price_formatted"]
        price_full = f"LKR {price_lkr:,.0f}"
        house_age = 2025 - payload["year_built"]

        # ── Price Card ──
        st.markdown(f"""
        <div class="price-hero">
            <div class="price-tag">Estimated Property Value</div>
            <div class="price-main">{price_fmt}</div>
            <div class="price-sub">{price_full}</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📋 Summary", "💡 Insights"])

        with tab1:
            items = [
                ("District", payload["district"]),
                ("Area", payload["area"]),
                ("Land Size", f"{payload['perch']} perches"),
                ("Bedrooms", str(payload["bedrooms"])),
                ("Bathrooms", str(payload["bathrooms"])),
                ("Kitchen", f"{payload['kitchen_area_sqft']} sq ft"),
                ("Parking", f"{payload['parking_spots']} spots"),
                ("Floors", str(payload["floors"])),
                ("Year Built", str(payload["year_built"])),
                ("House Age", f"{house_age} yrs"),
                ("Garden", "✅" if payload["has_garden"] else "❌"),
                ("AC", "✅" if payload["has_ac"] else "❌"),
                ("Water", payload["water_supply"]),
                ("Electricity", payload["electricity"]),
            ]
            grid = '<div class="detail-grid">'
            for lbl, val in items:
                grid += f'<div class="detail-item"><div class="detail-label">{lbl}</div><div class="detail-value">{val}</div></div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)

        with tab2:
            # Insight metrics
            ppp = price_lkr / payload["perch"] if payload["perch"] > 0 else 0
            ppb = price_lkr / payload["bedrooms"] if payload["bedrooms"] > 0 else 0
            ppf = price_lkr / payload["floors"] if payload["floors"] > 0 else 0

            st.markdown(f"""
            <div class="insight-row">
                <div class="insight-card">
                    <div class="insight-number">{format_lkr(ppp)}</div>
                    <div class="insight-label">Per Perch</div>
                </div>
                <div class="insight-card">
                    <div class="insight-number">{format_lkr(ppb)}</div>
                    <div class="insight-label">Per Bedroom</div>
                </div>
            </div>
            <div class="insight-row">
                <div class="insight-card">
                    <div class="insight-number">{format_lkr(ppf)}</div>
                    <div class="insight-label">Per Floor</div>
                </div>
                <div class="insight-card">
                    <div class="insight-number">{house_age} yrs</div>
                    <div class="insight-label">House Age</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # District comparison
            avg_prices = {
                "Colombo": 30_000_000, "Gampaha": 20_000_000, "Kandy": 18_000_000,
                "Galle": 16_000_000, "Kalutara": 14_000_000, "Nuwara Eliya": 15_000_000,
                "Jaffna": 12_000_000, "Kurunegala": 11_000_000, "Ratnapura": 10_000_000,
                "Matara": 13_000_000, "Hambantota": 11_000_000, "Badulla": 9_000_000,
                "Trincomalee": 10_000_000, "Batticaloa": 9_500_000,
            }
            avg = avg_prices.get(payload["district"], 10_000_000)
            diff = ((price_lkr - avg) / avg) * 100
            if diff > 0:
                st.markdown(f'<div class="comparison-bar comparison-up">📈 {diff:.1f}% above avg. for {payload["district"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="comparison-bar comparison-down">📉 {abs(diff):.1f}% below avg. for {payload["district"]}</div>', unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div class="empty-state">
            <span class="empty-icon">🏠</span>
            <p class="empty-text">
                Fill in the property details on the left<br>
                and click <strong>🔮 Predict Price</strong> to get an<br>
                AI-powered property valuation
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
