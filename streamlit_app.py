import streamlit as st
import requests

st.set_page_config(
    page_title="LankaEstimate · AI Property Valuation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ─── Reset & Base ─────────────────────────── */
*, html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-sizing: border-box;
}
.stApp {
    background: #F7F8FC;
    min-height: 100vh;
}
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

/* ─── Hero Banner ───────────────────────────── */
.hero-wrap {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 45%, #0f3460 100%);
    padding: 2.2rem 2.5rem 2rem;
    margin: -1rem -1rem 1.8rem -1rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='20'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(253,126,20,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-inner {
    position: relative; z-index: 1;
    display: flex; align-items: center; gap: 1rem;
}
.hero-icon {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #fd7e14, #e8590c);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    box-shadow: 0 8px 24px rgba(253,126,20,0.35);
    flex-shrink: 0;
}
.hero-text { flex: 1; }
.hero-brand {
    font-size: 1.9rem; font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.hero-brand span { color: #fd7e14; }
.hero-tagline {
    font-size: 1rem; font-weight: 400;
    color: rgba(255,255,255,0.55);
    line-height: 1.4;
}
.hero-chips {
    display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.65rem;
}
.hero-chip {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.7);
    border-radius: 100px;
    padding: 0.3rem 0.85rem;
    font-size: 0.8rem; font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.hero-chip.active {
    background: rgba(253,126,20,0.15);
    border-color: rgba(253,126,20,0.3);
    color: #fd7e14;
}

/* ─── Card ─────────────────────────────────── */
.card {
    background: #FFFFFF;
    border: 1px solid #EAECF0;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(16,24,40,0.06), 0 1px 2px rgba(16,24,40,0.04);
    margin-bottom: 1.2rem;
}
.card-head {
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid #F2F4F7;
}
.card-icon {
    width: 32px; height: 32px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; flex-shrink: 0;
}
.ci-orange { background: #FFF4ED; }
.ci-blue   { background: #EFF8FF; }
.ci-green  { background: #ECFDF3; }
.ci-purple { background: #F4F3FF; }
.card-title {
    font-size: 0.95rem; font-weight: 700;
    color: #101828;
    text-transform: uppercase; letter-spacing: 0.07em;
}
.card-sub {
    font-size: 0.83rem; color: #98A2B3; font-weight: 400;
    margin-top: 0.1rem;
}

/* ─── Form Section Label ────────────────────── */
.sec-label {
    font-size: 0.83rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #98A2B3;
    margin: 1rem 0 0.4rem;
    display: flex; align-items: center; gap: 0.35rem;
}
.sec-label span { color: #D0D5DD; }
hr.sep {
    border: none; border-top: 1px solid #F2F4F7;
    margin: 0.8rem 0;
}

/* ─── Predict Button ────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #fd7e14 0%, #e8590c 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.72rem 1.5rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.25s cubic-bezier(.4,0,.2,1) !important;
    box-shadow: 0 4px 14px rgba(253,126,20,0.35) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(253,126,20,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
    background: #D0D5DD !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ─── Form Controls ────────────────────────── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #FFFFFF !important;
    border: 1.5px solid #D0D5DD !important;
    border-radius: 9px !important;
    color: #101828 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    transition: border-color 0.15s ease !important;
}
.stSelectbox > div > div:hover,
.stNumberInput > div > div > input:hover {
    border-color: #98A2B3 !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within {
    border-color: #fd7e14 !important;
    box-shadow: 0 0 0 3px rgba(253,126,20,0.12) !important;
}
.stSelectbox label, .stNumberInput label,
.stCheckbox label span {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #344054 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ─── Price Result ──────────────────────────── */
.price-band {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}
.price-band::before {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(253,126,20,0.18) 0%, transparent 70%);
}
.price-band::after {
    content: '';
    position: absolute;
    top: -40px; left: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(15,52,96,0.5) 0%, transparent 70%);
}
.pb-eyebrow {
    font-size: 0.82rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.45);
    margin-bottom: 0.5rem;
    position: relative; z-index: 1;
}
.pb-price {
    font-size: 2.9rem; font-weight: 800;
    letter-spacing: -0.04em;
    color: #FFFFFF;
    line-height: 1;
    position: relative; z-index: 1;
}
.pb-price span { color: #fd7e14; }
.pb-sub {
    font-size: 0.95rem; color: rgba(255,255,255,0.45);
    margin-top: 0.4rem; font-weight: 400;
    position: relative; z-index: 1;
}
.pb-badge {
    display: inline-block;
    background: rgba(253,126,20,0.15);
    border: 1px solid rgba(253,126,20,0.3);
    color: #fd7e14;
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem; font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 0.8rem;
    position: relative; z-index: 1;
}

/* ─── KPI Strip ─────────────────────────────── */
.kpi-strip {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 0.7rem; margin-bottom: 1rem;
}
.kpi {
    background: #FFFFFF;
    border: 1px solid #EAECF0;
    border-radius: 12px;
    padding: 0.85rem 0.75rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(16,24,40,0.04);
}
.kpi-val {
    font-size: 1.25rem; font-weight: 800;
    color: #101828; letter-spacing: -0.02em;
}
.kpi-lbl {
    font-size: 0.75rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #98A2B3; margin-top: 0.2rem;
}

/* ─── Tabs ──────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #F2F4F7;
    border-radius: 10px;
    padding: 3px; gap: 2px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; border: none;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600; font-size: 0.92rem;
    color: #667085;
    padding: 0.42rem 1rem;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #101828 !important;
    box-shadow: 0 1px 4px rgba(16,24,40,0.1) !important;
}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"] { display: none; }

/* ─── Summary Grid ──────────────────────────── */
.sum-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}
.sum-row {
    background: #F9FAFB;
    border: 1px solid #F2F4F7;
    border-radius: 10px;
    padding: 0.5rem 0.75rem;
    display: flex; justify-content: space-between; align-items: center;
}
.sum-key { font-size: 0.88rem; color: #667085; font-weight: 500; }
.sum-val { font-size: 0.9rem; color: #101828; font-weight: 700; }

/* ─── XAI ───────────────────────────────────── */
.xai-header {
    background: linear-gradient(135deg, #EFF8FF, #F4F3FF);
    border: 1px solid #B2DDFF;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin-bottom: 1rem;
    display: flex; align-items: flex-start; gap: 0.6rem;
}
.xai-icon { font-size: 1.2rem; margin-top: 0.05rem; }
.xai-body { flex: 1; }
.xai-title { font-size: 0.95rem; font-weight: 700; color: #1849A9; margin-bottom: 0.2rem; }
.xai-desc  { font-size: 0.85rem; color: #1849A9; opacity: 0.75; line-height: 1.5; }
.xai-method {
    display: inline-block;
    background: #EFF8FF;
    border: 1px solid #B2DDFF;
    color: #1849A9;
    border-radius: 100px;
    padding: 0.2rem 0.65rem;
    font-size: 0.78rem; font-weight: 700;
    margin-top: 0.35rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ─── Feature Bar ───────────────────────────── */
.feat-item { margin-bottom: 0.85rem; }
.feat-row {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.3rem;
}
.feat-name {
    font-size: 0.9rem; font-weight: 600; color: #344054;
    display: flex; align-items: center; gap: 0.4rem;
}
.feat-arrow-up {
    display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 50%;
    background: #ECFDF3; color: #039855;
    font-size: 0.6rem; font-weight: 800; flex-shrink: 0;
}
.feat-arrow-dn {
    display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 50%;
    background: #FEF3F2; color: #D92D20;
    font-size: 0.6rem; font-weight: 800; flex-shrink: 0;
}
.feat-pct {
    font-size: 0.85rem; font-weight: 700; color: #98A2B3;
    background: #F2F4F7; border-radius: 100px;
    padding: 0.1rem 0.45rem;
}
.feat-track {
    width: 100%; height: 8px;
    background: #F2F4F7; border-radius: 100px;
    overflow: hidden;
}
.feat-fill-up {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #12B76A, #6CE9A6);
}
.feat-fill-dn {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #F04438, #FDA29B);
}
.feat-fill-neutral {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #1570EF, #53B1FD);
}

/* ─── Empty State ───────────────────────────── */
.empty {
    text-align: center; padding: 3rem 1.5rem;
}
.empty-illo {
    width: 80px; height: 80px;
    background: linear-gradient(135deg, #F2F4F7, #EAECF0);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; margin: 0 auto 1rem;
}
.empty-title { font-size: 1.15rem; font-weight: 700; color: #344054; margin-bottom: 0.4rem; }
.empty-desc  { font-size: 0.95rem; color: #98A2B3; line-height: 1.7; }
.empty-step {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: #F9FAFB; border: 1px solid #EAECF0;
    border-radius: 8px; padding: 0.5rem 1rem;
    font-size: 0.88rem; font-weight: 600; color: #344054;
    margin: 0.25rem;
}
.step-num {
    width: 18px; height: 18px; border-radius: 50%;
    background: #101828; color: #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.55rem; font-weight: 800;
}

/* ─── Footer ────────────────────────────────── */
.footer {
    text-align: center; padding: 1.5rem 0 0.5rem;
    font-size: 0.85rem; color: #D0D5DD;
    border-top: 1px solid #F2F4F7; margin-top: 1rem;
}
.footer a { color: #98A2B3; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
API_BASE   = "http://localhost:8000"
DISTRICTS  = [
    "Ampara","Anuradhapura","Badulla","Batticaloa","Colombo","Galle",
    "Gampaha","Hambantota","Jaffna","Kalutara","Kandy","Kegalle",
    "Kilinochchi","Kurunegala","Mannar","Matale","Matara","Monaragala",
    "Mullaitivu","Nuwara Eliya","Polonnaruwa","Puttalam","Ratnapura",
    "Trincomalee","Vavuniya"
]
AREAS = {
    "Ampara":["Ampara Central"],
    "Anuradhapura":["Madawachchiya","New Town","Nuwaragam Palatha"],
    "Badulla":["Badulla Town","Bandarawela","Hali Ela"],
    "Batticaloa":["Batticaloa Town","Eravur","Kallady"],
    "Colombo":["Bambalapitiya","Borella","Dehiwala","Kollupitiya","Mount Lavinia",
               "Narahenpita","Nugegoda","Rajagiriya","Wellawatte"],
    "Galle":["Galle Fort","Hikkaduwa","Karapitiya","Unawatuna"],
    "Gampaha":["Gampaha Town","Ja-Ela","Kadawatha","Negombo","Ragama","Wattala"],
    "Hambantota":["Ambalantota","Hambantota Town","Tangalle"],
    "Jaffna":["Chunnakam","Jaffna Town","Kokuvil","Nallur"],
    "Kalutara":["Beruwala","Kalutara North","Panadura","Wadduwa"],
    "Kandy":["Gatambe","Kandy City","Katugastota","Peradeniya","Tennekumbura"],
    "Kegalle":["Kegalle Central"],
    "Kilinochchi":["Kilinochchi Central"],
    "Kurunegala":["Kurunegala Town","Melsiripura","Pannala","Polgahawela"],
    "Mannar":["Mannar Central"],
    "Matale":["Matale Central"],
    "Matara":["Akurugoda","Matara Town","Nupe","Weligama"],
    "Monaragala":["Monaragala Central"],
    "Mullaitivu":["Mullaitivu Central"],
    "Nuwara Eliya":["Nuwara Eliya Central"],
    "Polonnaruwa":["Polonnaruwa Central"],
    "Puttalam":["Puttalam Central"],
    "Ratnapura":["Kuruwita","Pelmadulla","Ratnapura Town"],
    "Trincomalee":["China Bay","Nilaveli","Uppuveli"],
    "Vavuniya":["Vavuniya Central"],
}
WATER  = ["Both","Pipe-borne","Well"]
ELEC   = ["Single phase","Three phase"]

def fmt_lkr(v):
    if v >= 1_000_000: return f"Rs. {v/1_000_000:.2f} M"
    if v >= 1_000:     return f"Rs. {v/1_000:.1f}K"
    return f"Rs. {v:.0f}"

def backend_ok():
    try: return requests.get(f"{API_BASE}/api/health", timeout=3).status_code == 200
    except: return False

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-inner">
    <div class="hero-icon">🏠</div>
    <div class="hero-text">
      <div class="hero-brand">Lanka<span>Estimate</span></div>
      <div class="hero-tagline">AI-powered property valuation for Sri Lanka's real estate market</div>
      <div class="hero-chips">
        <span class="hero-chip active">⚡ XGBoost ML</span>
        <span class="hero-chip">🧠 Explainable AI</span>
        <span class="hero-chip">📍 25 Districts</span>
        <span class="hero-chip">🏘️ 70+ Areas</span>
        <span class="hero-chip">📊 20K+ Data Points</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

ok = backend_ok()
if not ok:
    st.error("⚠️ Backend offline — run: `cd backend && .\\venv\\Scripts\\python -m uvicorn main:app --port 8000`")

# ─── Layout ───────────────────────────────────────────────────────────────────
L, R = st.columns([11, 13], gap="large")

# ════════════════════════════ LEFT — FORM ═════════════════════════════════════
with L:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-head">
      <div class="card-icon ci-blue">📋</div>
      <div>
        <div class="card-title">Property Details</div>
        <div class="card-sub">Fill in all fields to get an instant valuation</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Location
    st.markdown('<div class="sec-label">📍 Location</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        district = st.selectbox("District", DISTRICTS,
                                index=DISTRICTS.index("Colombo"), key="district")
    with c2:
        area = st.selectbox("Area", AREAS.get(district, []), key="area")

    st.markdown('<hr class="sep">', unsafe_allow_html=True)

    # Size & Structure
    st.markdown('<div class="sec-label">📐 Size & Structure</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        perch    = st.number_input("Land (Perches)", 1,  100, 10, key="perch")
        bedrooms = st.number_input("Bedrooms",       1,   10,  3, key="bed")
    with s2:
        kitchen  = st.number_input("Kitchen (sq ft)", 20, 300, 100, key="kit")
        bathrooms= st.number_input("Bathrooms",        1,  10,   2, key="bath")
    with s3:
        floors   = st.number_input("Floors",           1,   5,   1, key="floors")
        parking  = st.number_input("Parking Spots",    0,   5,   1, key="park")

    st.markdown('<hr class="sep">', unsafe_allow_html=True)

    # Amenities
    st.markdown('<div class="sec-label">⚡ Amenities & Utilities</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    with a1: has_garden  = st.checkbox("🌿 Garden", True,  key="garden")
    with a2: has_ac      = st.checkbox("❄️ AC",     False, key="ac")
    with a3: water_sup   = st.selectbox("💧 Water",        WATER, key="water")
    with a4: electricity = st.selectbox("⚡ Electricity",  ELEC,  key="elec")

    st.markdown('<hr class="sep">', unsafe_allow_html=True)

    # Year
    st.markdown('<div class="sec-label">📅 Construction</div>', unsafe_allow_html=True)
    year_built = st.number_input("Year Built", 1980, 2026, 2015, step=1, key="year")

    st.markdown("<br>", unsafe_allow_html=True)
    go = st.button("🔍  Get AI Valuation", use_container_width=True,
                   type="primary", disabled=not ok)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════ RIGHT — RESULTS ══════════════════════════════════
with R:

    # ── Trigger ──
    if go:
        payload = {
            "district": district, "area": area, "perch": perch,
            "bedrooms": bedrooms, "bathrooms": bathrooms,
            "kitchen_area_sqft": kitchen, "parking_spots": parking,
            "has_garden": has_garden, "has_ac": has_ac,
            "water_supply": water_sup, "electricity": electricity,
            "floors": floors, "year_built": year_built,
        }
        with st.spinner("Analysing property & computing AI explanation…"):
            try:
                r = requests.post(f"{API_BASE}/api/predict", json=payload, timeout=15)
                if r.status_code == 200:
                    st.session_state["res"]   = r.json()
                    st.session_state["pay"]   = payload
                    st.session_state.pop("err", None)
                else:
                    st.session_state["err"] = r.json().get("detail","Unknown error")
                    st.session_state.pop("res", None)
            except Exception as e:
                st.session_state["err"] = str(e)

    if "err" in st.session_state:
        st.error(f"❌ {st.session_state['err']}")

    if "res" in st.session_state:
        res = st.session_state["res"]
        pay = st.session_state["pay"]

        price  = res["predicted_price_lkr"]
        pfmt   = res["predicted_price_formatted"]
        pfull  = f"LKR {price:,.0f}"
        age    = 2025 - pay["year_built"]
        ppp    = price / pay["perch"]    if pay["perch"]    > 0 else 0
        ppb    = price / pay["bedrooms"] if pay["bedrooms"] > 0 else 0

        # ── Price Card ──
        parts = pfmt.split(" ")
        num   = parts[1] if len(parts) > 1 else pfmt
        unit  = " ".join(parts[2:]) if len(parts) > 2 else ""
        st.markdown(f"""
        <div class="price-band">
          <div class="pb-eyebrow">AI-Estimated Property Value</div>
          <div class="pb-price">{parts[0]} <span>{num}</span> {unit}</div>
          <div class="pb-sub">{pfull}</div>
          <div class="pb-badge">✓ Prediction Complete</div>
        </div>""", unsafe_allow_html=True)

        # ── KPI Strip ──
        st.markdown(f"""
        <div class="kpi-strip">
          <div class="kpi">
            <div class="kpi-val">{fmt_lkr(ppp)}</div>
            <div class="kpi-lbl">Per Perch</div>
          </div>
          <div class="kpi">
            <div class="kpi-val">{fmt_lkr(ppb)}</div>
            <div class="kpi-lbl">Per Bedroom</div>
          </div>
          <div class="kpi">
            <div class="kpi-val">{age} yrs</div>
            <div class="kpi-lbl">House Age</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Tabs ──
        t_sum, t_xai = st.tabs(["📋  Property Summary", "🧠  AI Explanation"])

        # ── Summary Tab ──
        with t_sum:
            st.markdown('<div class="card" style="margin-top:.6rem">', unsafe_allow_html=True)
            st.markdown("""
            <div class="card-head">
              <div class="card-icon ci-orange">🏡</div>
              <div>
                <div class="card-title">Input Summary</div>
                <div class="card-sub">Details used for this valuation</div>
              </div>
            </div>""", unsafe_allow_html=True)
            rows = [
                ("📍 District",    pay["district"]),
                ("🗺️ Area",        pay["area"]),
                ("📐 Land Size",   f"{pay['perch']} perches"),
                ("🛏️ Bedrooms",   str(pay["bedrooms"])),
                ("🚿 Bathrooms",   str(pay["bathrooms"])),
                ("🍳 Kitchen",     f"{pay['kitchen_area_sqft']} sq ft"),
                ("🚗 Parking",     f"{pay['parking_spots']} spots"),
                ("🏢 Floors",      str(pay["floors"])),
                ("📅 Year Built",  str(pay["year_built"])),
                ("⏳ House Age",   f"{age} years"),
                ("🌿 Garden",      "Yes ✅" if pay["has_garden"] else "No ❌"),
                ("❄️ AC",          "Yes ✅" if pay["has_ac"]     else "No ❌"),
                ("💧 Water",       pay["water_supply"]),
                ("⚡ Electricity", pay["electricity"]),
            ]
            html = '<div class="sum-grid">'
            for k, v in rows:
                html += f'<div class="sum-row"><span class="sum-key">{k}</span><span class="sum-val">{v}</span></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── XAI Tab ──
        with t_xai:
            st.markdown('<div class="card" style="margin-top:.6rem">', unsafe_allow_html=True)
            st.markdown("""
            <div class="card-head">
              <div class="card-icon ci-purple">🧠</div>
              <div>
                <div class="card-title">Why this price?</div>
                <div class="card-sub">Top factors that shaped the prediction</div>
              </div>
            </div>""", unsafe_allow_html=True)

            method = res.get("explainer_method", "Feature Importance")
            st.markdown(f"""
            <div class="xai-header">
              <div class="xai-icon">💡</div>
              <div class="xai-body">
                <div class="xai-title">Explainable AI Breakdown</div>
                <div class="xai-desc">
                  Each bar shows how much a feature contributed to moving the price
                  <b style="color:#12B76A">▲ up</b> or <b style="color:#F04438">▼ down</b>
                  relative to the average property. Wider bar = stronger influence.
                </div>
                <div class="xai-method">Method: {method}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            contribs = res.get("feature_contributions", [])
            if contribs:
                html = ""
                for c in contribs:
                    d   = c["direction"]
                    lbl = c["label"]
                    pct = c["percentage"]
                    if d == "increase":
                        arrow = '<span class="feat-arrow-up">▲</span>'
                        fill  = "feat-fill-up"
                        color = "#039855"
                    elif d == "decrease":
                        arrow = '<span class="feat-arrow-dn">▼</span>'
                        fill  = "feat-fill-dn"
                        color = "#D92D20"
                    else:
                        arrow = '<span class="feat-arrow-up" style="background:#EFF8FF;color:#1570EF">→</span>'
                        fill  = "feat-fill-neutral"
                        color = "#1570EF"

                    html += f"""
                    <div class="feat-item">
                      <div class="feat-row">
                        <span class="feat-name">{arrow}{lbl}</span>
                        <span class="feat-pct">{pct:.1f}%</span>
                      </div>
                      <div class="feat-track">
                        <div class="{fill}" style="width:{min(pct,100):.1f}%"></div>
                      </div>
                    </div>"""
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.info("No explanation data returned from the model.")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # ── Empty State ──
        st.markdown("""
        <div class="card">
          <div class="empty">
            <div class="empty-illo">🏠</div>
            <div class="empty-title">Ready to value your property</div>
            <div class="empty-desc">
              Complete the form on the left with your property details,<br>
              then click <b>Get AI Valuation</b> to instantly receive<br>
              a price estimate with a full AI explanation.
            </div>
            <br>
            <div>
              <span class="empty-step"><span class="step-num">1</span> Select district & area</span>
              <span class="empty-step"><span class="step-num">2</span> Enter size & features</span>
              <span class="empty-step"><span class="step-num">3</span> Click Get AI Valuation</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  LankaEstimate &nbsp;·&nbsp; Powered by XGBoost &nbsp;·&nbsp; Explainable AI &nbsp;·&nbsp;
  Sri Lanka Property Market &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)
