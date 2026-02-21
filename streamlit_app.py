import streamlit as st
import requests

st.set_page_config(
    page_title="Sri Lanka House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Professional White / Light Theme CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background-color: #F1F5F9;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top Nav Bar ── */
.top-bar {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 0.9rem 2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.top-bar-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.top-bar-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.01em;
}
.top-bar-sub {
    font-size: 0.78rem;
    color: #64748B;
    font-weight: 400;
}
.top-bar-badge {
    margin-left: auto;
    background: #EFF6FF;
    color: #2563EB;
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 600;
}

/* ── Card ── */
.card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 0.85rem;
    margin-bottom: 1.1rem;
}
.card-header-icon {
    width: 30px; height: 30px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.icon-blue  { background: #EFF6FF; }
.icon-green { background: #F0FDF4; }
.icon-purple { background: #FAF5FF; }
.card-header-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #0F172A;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Section Label ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin: 0.8rem 0 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

/* ── Price Card ── */
.price-card {
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
    border-radius: 14px;
    padding: 1.6rem;
    color: white;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.25);
}
.price-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.8;
    margin-bottom: 0.4rem;
}
.price-amount {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.price-lkr {
    font-size: 0.85rem;
    opacity: 0.75;
    margin-top: 0.3rem;
    font-weight: 400;
}

/* ── Stats Row ── */
.stats-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.6rem;
    margin-bottom: 1rem;
}
.stat-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.75rem;
    text-align: center;
}
.stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.02em;
}
.stat-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    font-weight: 600;
    margin-top: 0.15rem;
}

/* ── Summary Grid ── */
.summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0.6rem;
    background: #F8FAFC;
    border-radius: 8px;
    border: 1px solid #F1F5F9;
}
.summary-key {
    font-size: 0.72rem;
    color: #64748B;
    font-weight: 500;
}
.summary-val {
    font-size: 0.75rem;
    color: #0F172A;
    font-weight: 600;
}

/* ── SHAP Bar ── */
.shap-section { margin-top: 0.5rem; }
.shap-item {
    margin-bottom: 0.6rem;
}
.shap-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.2rem;
}
.shap-label {
    font-size: 0.74rem;
    font-weight: 500;
    color: #334155;
}
.shap-pct {
    font-size: 0.68rem;
    font-weight: 600;
    color: #64748B;
}
.shap-bar-track {
    background: #F1F5F9;
    border-radius: 100px;
    height: 7px;
    overflow: hidden;
}
.shap-bar-fill-up {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #059669, #10B981);
    transition: width 0.6s ease;
}
.shap-bar-fill-down {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #DC2626, #EF4444);
    transition: width 0.6s ease;
}
.shap-direction-up {
    display: inline-block;
    background: #F0FDF4;
    color: #059669;
    border: 1px solid #BBF7D0;
    border-radius: 20px;
    padding: 0.1rem 0.45rem;
    font-size: 0.62rem;
    font-weight: 700;
    margin-right: 0.3rem;
}
.shap-direction-down {
    display: inline-block;
    background: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
    border-radius: 20px;
    padding: 0.1rem 0.45rem;
    font-size: 0.62rem;
    font-weight: 700;
    margin-right: 0.3rem;
}

/* ── Empty / Placeholder ── */
.empty-state {
    text-align: center;
    padding: 2.5rem 1rem;
}
.empty-icon {
    font-size: 3rem;
    opacity: 0.2;
    display: block;
    margin-bottom: 0.6rem;
}
.empty-text {
    color: #94A3B8;
    font-size: 0.85rem;
    line-height: 1.7;
}
.empty-text strong { color: #64748B; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F8FAFC;
    border-radius: 10px;
    padding: 3px;
    gap: 0;
    border: 1px solid #E2E8F0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.78rem;
    color: #64748B;
    padding: 0.45rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #2563EB !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"] { display: none; }

/* ── Form Controls ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
.stSelectbox label,
.stNumberInput label,
.stSlider label,
.stCheckbox label span {
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.4) !important;
    background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    font-size: 0.82rem !important;
    color: #374151 !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: #F1F5F9;
    margin: 0.7rem 0;
}

/* ── XAI Banner ── */
.xai-banner {
    background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.xai-banner-text {
    font-size: 0.75rem;
    color: #1E40AF;
    font-weight: 500;
    line-height: 1.4;
}

/* ── Error ── */
.stAlert { border-radius: 10px; font-family: 'Inter', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000"

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

WATER_SUPPLY = ["Both", "Pipe-borne", "Well"]
ELECTRICITY  = ["Single phase", "Three phase"]


# ── Helpers ────────────────────────────────────────────────────────────────────
def fmt_lkr(v: float) -> str:
    if v >= 1_000_000:
        return f"Rs. {v/1_000_000:.2f} M"
    if v >= 1_000:
        return f"Rs. {v/1_000:.1f}K"
    return f"Rs. {v:.0f}"

def check_backend() -> bool:
    try:
        return requests.get(f"{API_BASE}/api/health", timeout=3).status_code == 200
    except Exception:
        return False


# ── Top Navigation Bar ─────────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  <div class="top-bar-logo">🏠</div>
  <div>
    <div class="top-bar-title">Sri Lanka House Price Predictor</div>
    <div class="top-bar-sub">AI-powered property valuation across 25 districts</div>
  </div>
  <div class="top-bar-badge">⚡ XGBoost + SHAP XAI</div>
</div>
""", unsafe_allow_html=True)

backend_ok = check_backend()
if not backend_ok:
    st.error("⚠️ **Backend offline.** Run: `cd backend && .\\venv\\Scripts\\python -m uvicorn main:app --port 8000`")

# ── Main Layout ────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# ─────────────────────────── LEFT: Form ───────────────────────────────────────
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-header">
      <div class="card-header-icon icon-blue">📋</div>
      <span class="card-header-title">Property Details</span>
    </div>
    """, unsafe_allow_html=True)

    # Location
    st.markdown('<div class="section-label">📍 Location</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        district = st.selectbox("District", DISTRICTS, index=DISTRICTS.index("Colombo"), key="district")
    with c2:
        area = st.selectbox("Area", AREAS.get(district, []), key="area")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Size & Structure
    st.markdown('<div class="section-label">📐 Size & Structure</div>', unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        perch    = st.number_input("Land (Perches)", 1, 100,  10, key="perch")
        bedrooms = st.number_input("Bedrooms",        1,  10,   3, key="bed")
    with r1c2:
        kitchen  = st.number_input("Kitchen (sq ft)", 20, 300, 100, key="kit")
        bathrooms= st.number_input("Bathrooms",        1,  10,   2, key="bath")
    with r1c3:
        floors   = st.number_input("Floors",           1,   5,   1, key="floors")
        parking  = st.number_input("Parking Spots",    0,   5,   1, key="park")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Amenities
    st.markdown('<div class="section-label">⚡ Amenities & Utilities</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        has_garden = st.checkbox("🌿 Garden", value=True,  key="garden")
    with a2:
        has_ac     = st.checkbox("❄️ AC",     value=False, key="ac")
    with a3:
        water_supply = st.selectbox("💧 Water",       WATER_SUPPLY, key="water")
    with a4:
        electricity  = st.selectbox("⚡ Electricity", ELECTRICITY,  key="elec")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Year Built
    st.markdown('<div class="section-label">📅 Construction</div>', unsafe_allow_html=True)
    year_built = st.number_input("Year Built", 1980, 2026, 2015, step=1, key="year")

    st.markdown("", unsafe_allow_html=True)
    predict_btn = st.button("🔍  Predict Property Price",
                            use_container_width=True,
                            type="primary",
                            disabled=not backend_ok)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────── RIGHT: Results ───────────────────────────────────
with right:
    # — Trigger prediction —
    if predict_btn:
        payload = {
            "district": district, "area": area, "perch": perch,
            "bedrooms": bedrooms, "bathrooms": bathrooms,
            "kitchen_area_sqft": kitchen, "parking_spots": parking,
            "has_garden": has_garden, "has_ac": has_ac,
            "water_supply": water_supply, "electricity": electricity,
            "floors": floors, "year_built": year_built,
        }
        try:
            with st.spinner("Running XGBoost model + SHAP analysis…"):
                r = requests.post(f"{API_BASE}/api/predict", json=payload, timeout=15)
            if r.status_code == 200:
                st.session_state["result"]  = r.json()
                st.session_state["payload"] = payload
                st.session_state.pop("error", None)
            else:
                st.session_state["error"] = r.json().get("detail", "Unknown error")
                st.session_state.pop("result", None)
        except requests.exceptions.ConnectionError:
            st.session_state["error"] = "Cannot connect to backend."
        except Exception as e:
            st.session_state["error"] = str(e)

    # — Error —
    if "error" in st.session_state:
        st.error(f"❌ {st.session_state['error']}")

    # — Show results —
    if "result" in st.session_state:
        res     = st.session_state["result"]
        payload = st.session_state["payload"]

        price_lkr  = res["predicted_price_lkr"]
        price_fmt  = res["predicted_price_formatted"]
        price_full = f"LKR {price_lkr:,.0f}"
        house_age  = 2025 - payload["year_built"]
        ppp        = price_lkr / payload["perch"]   if payload["perch"]    > 0 else 0
        ppb        = price_lkr / payload["bedrooms"] if payload["bedrooms"] > 0 else 0

        # ── Price hero card ──
        st.markdown(f"""
        <div class="price-card">
          <div class="price-label">Estimated Property Value</div>
          <div class="price-amount">{price_fmt}</div>
          <div class="price-lkr">{price_full}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quick stats ──
        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-value">{fmt_lkr(ppp)}</div>
            <div class="stat-label">Per Perch</div>
          </div>
          <div class="stat-box">
            <div class="stat-value">{fmt_lkr(ppb)}</div>
            <div class="stat-label">Per Bedroom</div>
          </div>
          <div class="stat-box">
            <div class="stat-value">{house_age} yrs</div>
            <div class="stat-label">House Age</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Tabs: Summary | XAI Explanation ──
        tab_sum, tab_xai = st.tabs(["📋  Summary", "🧠  AI Explanation (SHAP)"])

        with tab_sum:
            st.markdown('<div class="card" style="margin-top:0.5rem">', unsafe_allow_html=True)
            st.markdown("""
            <div class="card-header">
              <div class="card-header-icon icon-blue">🏡</div>
              <span class="card-header-title">Property Summary</span>
            </div>
            """, unsafe_allow_html=True)

            items = [
                ("District",    payload["district"]),
                ("Area",        payload["area"]),
                ("Land",        f"{payload['perch']} perches"),
                ("Bedrooms",    str(payload["bedrooms"])),
                ("Bathrooms",   str(payload["bathrooms"])),
                ("Kitchen",     f"{payload['kitchen_area_sqft']} sq ft"),
                ("Parking",     f"{payload['parking_spots']} spots"),
                ("Floors",      str(payload["floors"])),
                ("Year Built",  str(payload["year_built"])),
                ("House Age",   f"{house_age} years"),
                ("Garden",      "✅ Yes" if payload["has_garden"] else "❌ No"),
                ("AC",          "✅ Yes" if payload["has_ac"]     else "❌ No"),
                ("Water",       payload["water_supply"]),
                ("Electricity", payload["electricity"]),
            ]
            html = '<div class="summary-grid">'
            for k, v in items:
                html += f'<div class="summary-row"><span class="summary-key">{k}</span><span class="summary-val">{v}</span></div>'
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_xai:
            st.markdown('<div class="card" style="margin-top:0.5rem">', unsafe_allow_html=True)
            st.markdown("""
            <div class="card-header">
              <div class="card-header-icon icon-purple">🧠</div>
              <span class="card-header-title">SHAP Feature Contributions</span>
            </div>
            """, unsafe_allow_html=True)

            method = res.get("explainer_method", "Feature Importance")
            st.markdown(f"""
            <div class="xai-banner">
              <span>🔍</span>
              <span class="xai-banner-text">
                <strong>How was this price determined?</strong>
                Using <strong>{method}</strong> — features with
                <span style="color:#059669;font-weight:700">▲ green bars increased</span> the price
                and <span style="color:#DC2626;font-weight:700">▼ red bars decreased</span> it.
                Bar width shows relative importance.
              </span>
            </div>
            """, unsafe_allow_html=True)

            shap_data = res.get("feature_contributions", [])
            if shap_data:
                html = '<div class="shap-section">'
                for item in shap_data:
                    direction = item["direction"]
                    label     = item["label"]
                    pct       = item["percentage"]
                    badge_cls = "shap-direction-up"   if direction == "increase" else "shap-direction-down"
                    fill_cls  = "shap-bar-fill-up"    if direction == "increase" else "shap-bar-fill-down"
                    arrow     = "▲ Increases Price"   if direction == "increase" else "▼ Decreases Price"
                    html += f"""
                    <div class="shap-item">
                      <div class="shap-header">
                        <span class="shap-label">
                          <span class="{badge_cls}">{arrow}</span>{label}
                        </span>
                        <span class="shap-pct">{pct:.1f}%</span>
                      </div>
                      <div class="shap-bar-track">
                        <div class="{fill_cls}" style="width:{pct:.1f}%"></div>
                      </div>
                    </div>"""
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.info("SHAP data not available.")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # ── Empty state ──
        st.markdown("""
        <div class="card">
          <div class="empty-state">
            <span class="empty-icon">🏠</span>
            <p class="empty-text">
              Fill in the property details on the left<br>
              and click <strong>Predict Property Price</strong><br>
              to get an AI-powered valuation with<br>
              full explainability via SHAP.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#CBD5E1;font-size:0.7rem;font-family:'Inter',sans-serif;">
  Sri Lanka House Price Predictor &nbsp;·&nbsp; XGBoost Model &nbsp;·&nbsp; SHAP Explainability &nbsp;·&nbsp; 25 Districts
</div>
""", unsafe_allow_html=True)
