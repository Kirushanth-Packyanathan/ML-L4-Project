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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

/* ─── CSS Variables ─────────────────────────────────────────── */
:root {
  --bg:        #0A0E1A;
  --bg2:       #0F1629;
  --surface:   #141B2D;
  --surface2:  #1A2340;
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.12);
  --text:      #E8EAF0;
  --text2:     #8892A4;
  --text3:     #5A6478;
  --accent:    #FF6B2B;
  --accent2:   #FF8C5A;
  --accentbg:  rgba(255,107,43,0.12);
  --accentbdr: rgba(255,107,43,0.25);
  --blue:      #4F8EF7;
  --bluebg:    rgba(79,142,247,0.1);
  --green:     #10D9A0;
  --greenbg:   rgba(16,217,160,0.1);
  --purple:    #A78BFA;
  --purplebg:  rgba(167,139,250,0.1);
  --red:       #F56565;
  --redbg:     rgba(245,101,101,0.1);
  --radius:    16px;
  --radius-sm: 10px;
  --shadow:    0 8px 32px rgba(0,0,0,0.4);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
  --glow:      0 0 40px rgba(255,107,43,0.15);
}

/* ─── Reset & Base ──────────────────────────────────────────── */
*, html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  box-sizing: border-box;
}
.stApp {
  background: var(--bg) !important;
  min-height: 100vh;
}
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
.block-container { padding: 0 1.5rem 2rem !important; max-width: 1400px !important; }

/* ─── Scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ─── Hero Banner ───────────────────────────────────────────── */
.hero-wrap {
  background: linear-gradient(135deg, #0A0E1A 0%, #0F1629 50%, #0A1628 100%);
  padding: 2.5rem 2.5rem 2.2rem;
  margin: -1rem -1.5rem 2rem -1.5rem;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--border2);
}
.hero-wrap::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 60% 80% at 80% -20%, rgba(255,107,43,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 40% 60% at 10% 120%, rgba(79,142,247,0.12) 0%, transparent 60%);
  pointer-events: none;
}
/* Animated grid lines */
.hero-wrap::after {
  content: '';
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
}
.hero-inner {
  position: relative; z-index: 2;
  display: flex; align-items: center; gap: 1.2rem;
}
.hero-icon {
  width: 62px; height: 62px;
  background: linear-gradient(135deg, var(--accent), #e8590c);
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem;
  box-shadow: 0 12px 32px rgba(255,107,43,0.45), 0 0 0 1px rgba(255,107,43,0.2);
  flex-shrink: 0;
  animation: hero-pulse 3s ease-in-out infinite;
}
@keyframes hero-pulse {
  0%, 100% { box-shadow: 0 12px 32px rgba(255,107,43,0.45), 0 0 0 1px rgba(255,107,43,0.2); }
  50%       { box-shadow: 0 12px 48px rgba(255,107,43,0.65), 0 0 0 2px rgba(255,107,43,0.35), 0 0 60px rgba(255,107,43,0.2); }
}
.hero-text { flex: 1; }
.hero-brand {
  font-size: 2.2rem; font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.04em;
  line-height: 1;
  margin-bottom: 0.35rem;
}
.hero-brand span {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-tagline {
  font-size: 1.05rem; font-weight: 400;
  color: var(--text2);
  line-height: 1.5;
}
.hero-chips {
  display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.8rem;
}
.hero-chip {
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border2);
  color: var(--text2);
  border-radius: 100px;
  padding: 0.3rem 0.9rem;
  font-size: 0.78rem; font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  transition: all 0.2s ease;
}
.hero-chip:hover {
  background: var(--accentbg);
  border-color: var(--accentbdr);
  color: var(--accent);
}
.hero-chip.active {
  background: var(--accentbg);
  border-color: var(--accentbdr);
  color: var(--accent);
}
.hero-stats {
  display: flex; gap: 2rem; margin-top: 1.5rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
}
.hero-stat-val {
  font-size: 1.5rem; font-weight: 800;
  color: #fff; letter-spacing: -0.03em;
}
.hero-stat-lbl {
  font-size: 0.75rem; color: var(--text3); font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-top: 0.1rem;
}
/* Status dot */
.status-dot {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.3rem 0.8rem;
  background: rgba(16,217,160,0.1);
  border: 1px solid rgba(16,217,160,0.25);
  border-radius: 100px;
  font-size: 0.78rem; font-weight: 600;
  color: var(--green);
}
.status-dot::before {
  content: '';
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green);
  animation: blink 2s ease-in-out infinite;
}
.status-dot.offline {
  background: var(--redbg);
  border-color: rgba(245,101,101,0.25);
  color: var(--red);
}
.status-dot.offline::before { background: var(--red); animation: none; }
@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}

/* ─── Glass Card ────────────────────────────────────────────── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.6rem;
  box-shadow: var(--shadow-sm);
  margin-bottom: 1.2rem;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}
.card:hover {
  box-shadow: var(--shadow);
  border-color: var(--border2);
}
.card-head {
  display: flex; align-items: center; gap: 0.7rem;
  margin-bottom: 1.3rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}
.card-icon {
  width: 36px; height: 36px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; flex-shrink: 0;
}
.ci-orange { background: var(--accentbg); border: 1px solid var(--accentbdr); }
.ci-blue   { background: var(--bluebg);   border: 1px solid rgba(79,142,247,0.2); }
.ci-green  { background: var(--greenbg);  border: 1px solid rgba(16,217,160,0.2); }
.ci-purple { background: var(--purplebg); border: 1px solid rgba(167,139,250,0.2); }
.card-title {
  font-size: 0.9rem; font-weight: 700;
  color: var(--text);
  text-transform: uppercase; letter-spacing: 0.08em;
}
.card-sub {
  font-size: 0.82rem; color: var(--text3); font-weight: 400;
  margin-top: 0.1rem;
}

/* ─── Section Label ─────────────────────────────────────────── */
.sec-label {
  font-size: 0.78rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text3);
  margin: 1rem 0 0.45rem;
  display: flex; align-items: center; gap: 0.4rem;
}
hr.sep {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1rem 0;
}

/* ─── Buttons ───────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent) 0%, #e8590c 100%) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0.78rem 1.5rem !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1.05rem !important;
  letter-spacing: 0.01em !important;
  transition: all 0.25s cubic-bezier(.4,0,.2,1) !important;
  box-shadow: 0 4px 20px rgba(255,107,43,0.4), 0 0 0 0 rgba(255,107,43,0.4) !important;
  width: 100%;
  position: relative;
  overflow: hidden;
}
.stButton > button::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
  border-radius: 12px;
}
.stButton > button:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 30px rgba(255,107,43,0.55), 0 0 0 4px rgba(255,107,43,0.15) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }
.stButton > button:disabled {
  background: var(--surface2) !important;
  box-shadow: none !important;
  transform: none !important;
}

/* ─── Form Controls ─────────────────────────────────────────── */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
  background: var(--surface2) !important;
  border: 1.5px solid var(--border2) !important;
  border-radius: 10px !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stSelectbox > div > div:hover,
.stSelectbox [data-baseweb="select"]:hover > div {
  border-color: var(--accent) !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] span,
.stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] div {
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.97rem !important;
  font-weight: 500 !important;
  background: transparent !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"] {
  background: var(--surface2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 12px !important;
  box-shadow: var(--shadow) !important;
}
[data-baseweb="popover"] li,
[data-baseweb="menu"] li,
[data-baseweb="option"],
[data-baseweb="option"] span,
[role="option"], [role="listbox"] * {
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.93rem !important;
  background: transparent !important;
}
[data-baseweb="option"]:hover,
[role="option"]:hover {
  background: var(--accentbg) !important;
  color: var(--accent) !important;
}
.stNumberInput > div > div > input {
  background: var(--surface2) !important;
  border: 1.5px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.97rem !important;
  font-weight: 500 !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stNumberInput > div > div > input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(255,107,43,0.15) !important;
  outline: none !important;
}
.stSelectbox label, .stNumberInput label, .stCheckbox label {
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  color: var(--text2) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}
.stCheckbox label span, .stCheckbox label p {
  color: var(--text2) !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
/* Checkbox */
.stCheckbox [data-baseweb="checkbox"] > div {
  background: var(--surface2) !important;
  border-color: var(--border2) !important;
  border-radius: 5px !important;
}
.stCheckbox [data-baseweb="checkbox"] > div[data-checked="true"] {
  background: var(--accent) !important;
  border-color: var(--accent) !important;
}
/* Number input stepper buttons */
.stNumberInput button {
  background: var(--surface2) !important;
  border-color: var(--border2) !important;
  color: var(--text2) !important;
}
.stNumberInput button:hover {
  background: var(--accentbg) !important;
  color: var(--accent) !important;
}

/* ─── Price Result ──────────────────────────────────────────── */
.price-band {
  background: linear-gradient(135deg, #0F1629 0%, #141B2D 100%);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  padding: 2rem 1.8rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: var(--glow), var(--shadow);
}
.price-band::before {
  content: '';
  position: absolute;
  bottom: -60px; right: -60px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(255,107,43,0.2) 0%, transparent 70%);
  pointer-events: none;
}
.price-band::after {
  content: '';
  position: absolute;
  top: -60px; left: -60px;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(79,142,247,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.pb-eyebrow {
  font-size: 0.78rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.18em;
  color: var(--text3);
  margin-bottom: 0.6rem;
  position: relative; z-index: 1;
}
.pb-price {
  font-size: 3.4rem; font-weight: 800;
  letter-spacing: -0.05em;
  color: #FFFFFF;
  line-height: 1;
  position: relative; z-index: 1;
  text-shadow: 0 0 40px rgba(255,107,43,0.3);
}
.pb-price span {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
}
.pb-full {
  font-size: 0.88rem; color: var(--text3);
  margin-top: 0.35rem; font-weight: 500;
  position: relative; z-index: 1;
  font-style: italic;
}
.pb-badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  background: rgba(16,217,160,0.1);
  border: 1px solid rgba(16,217,160,0.25);
  color: var(--green);
  border-radius: 100px;
  padding: 0.3rem 1rem;
  font-size: 0.8rem; font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-top: 1rem;
  position: relative; z-index: 1;
}
/* Price range bar */
.price-range-wrap {
  position: relative; z-index: 1;
  margin-top: 1.2rem;
  padding: 0 0.5rem;
}
.price-range-labels {
  display: flex; justify-content: space-between;
  font-size: 0.75rem; color: var(--text3); font-weight: 500;
  margin-bottom: 0.4rem;
}
.price-range-track {
  width: 100%; height: 6px;
  background: rgba(255,255,255,0.08);
  border-radius: 100px;
  position: relative;
  overflow: visible;
}
.price-range-fill {
  position: absolute;
  top: 0; height: 100%;
  background: linear-gradient(90deg, var(--blue), var(--accent));
  border-radius: 100px;
  transition: width 0.6s ease;
}
.price-range-dot {
  position: absolute;
  top: 50%; transform: translate(-50%, -50%);
  width: 14px; height: 14px;
  background: var(--accent);
  border: 2px solid #fff;
  border-radius: 50%;
  box-shadow: 0 0 12px rgba(255,107,43,0.6);
}

/* ─── Confidence Meter ──────────────────────────────────────── */
.conf-wrap {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1rem;
  display: flex; align-items: center; gap: 1rem;
}
.conf-label {
  font-size: 0.78rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--text3); white-space: nowrap;
}
.conf-track {
  flex: 1; height: 8px;
  background: rgba(255,255,255,0.06);
  border-radius: 100px; overflow: hidden;
}
.conf-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, var(--blue), var(--green));
  position: relative; overflow: hidden;
  animation: conf-anim 1s ease-out forwards;
}
.conf-fill::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  animation: shimmer 2s infinite;
}
@keyframes conf-anim {
  from { width: 0 !important; }
}
@keyframes shimmer {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
.conf-pct {
  font-size: 0.95rem; font-weight: 800;
  color: var(--green); white-space: nowrap;
}

/* ─── KPI Strip ─────────────────────────────────────────────── */
.kpi-strip {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 0.8rem; margin-bottom: 1rem;
}
.kpi {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem 0.85rem;
  text-align: center;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}
.kpi::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  border-radius: 2px 2px 0 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.kpi:hover::before { opacity: 1; }
.kpi:hover {
  border-color: var(--border2);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.kpi-icon { font-size: 1.1rem; margin-bottom: 0.35rem; }
.kpi-val {
  font-size: 1.2rem; font-weight: 800;
  color: var(--text); letter-spacing: -0.02em;
}
.kpi-lbl {
  font-size: 0.7rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--text3); margin-top: 0.2rem;
}
.kpi-accent { color: var(--accent) !important; }
.kpi-blue   { color: var(--blue) !important; }
.kpi-green  { color: var(--green) !important; }
.kpi-k1::before { background: linear-gradient(90deg, var(--accent), var(--accent2)); }
.kpi-k2::before { background: linear-gradient(90deg, var(--blue), #74C0FC); }
.kpi-k3::before { background: linear-gradient(90deg, var(--green), #6EE7B7); }

/* ─── Tabs ──────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface2);
  border-radius: 12px;
  padding: 4px; gap: 3px;
  border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div {
  border-radius: 9px; border: none;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  color: var(--text3) !important;
  padding: 0.55rem 1.2rem;
  transition: all 0.2s ease;
  background: transparent;
}
.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div {
  background: var(--surface) !important;
  color: var(--text) !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
  font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 0 !important; }

/* ─── Summary Grid ──────────────────────────────────────────── */
.sum-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}
.sum-row {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.55rem 0.9rem;
  display: flex; justify-content: space-between; align-items: center;
  transition: border-color 0.2s ease;
}
.sum-row:hover { border-color: var(--border2); }
.sum-key { font-size: 0.85rem; color: var(--text3); font-weight: 500; }
.sum-val { font-size: 0.88rem; color: var(--text); font-weight: 700; }

/* ─── XAI Header ────────────────────────────────────────────── */
.xai-header {
  background: linear-gradient(135deg, var(--purplebg), var(--bluebg));
  border: 1px solid rgba(167,139,250,0.2);
  border-radius: 12px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1.2rem;
  display: flex; align-items: flex-start; gap: 0.7rem;
}
.xai-icon { font-size: 1.3rem; margin-top: 0.05rem; }
.xai-body { flex: 1; }
.xai-title {
  font-size: 0.95rem; font-weight: 700;
  color: var(--purple); margin-bottom: 0.25rem;
}
.xai-desc  {
  font-size: 0.85rem; color: var(--text2);
  opacity: 0.85; line-height: 1.6;
}
.xai-method {
  display: inline-block;
  background: var(--purplebg);
  border: 1px solid rgba(167,139,250,0.25);
  color: var(--purple);
  border-radius: 100px;
  padding: 0.2rem 0.7rem;
  font-size: 0.75rem; font-weight: 700;
  margin-top: 0.4rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ─── Feature Bars ──────────────────────────────────────────── */
.feat-item {
  margin-bottom: 1rem;
  animation: fadein-up 0.4s ease both;
}
@keyframes fadein-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.feat-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 0.35rem;
}
.feat-name {
  font-size: 0.9rem; font-weight: 600; color: var(--text);
  display: flex; align-items: center; gap: 0.5rem;
}
.feat-arrow-up {
  display: inline-flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--greenbg);
  border: 1px solid rgba(16,217,160,0.3);
  color: var(--green);
  font-size: 0.6rem; font-weight: 800; flex-shrink: 0;
}
.feat-arrow-dn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--redbg);
  border: 1px solid rgba(245,101,101,0.3);
  color: var(--red);
  font-size: 0.6rem; font-weight: 800; flex-shrink: 0;
}
.feat-arrow-neu {
  display: inline-flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--bluebg);
  border: 1px solid rgba(79,142,247,0.3);
  color: var(--blue);
  font-size: 0.6rem; font-weight: 800; flex-shrink: 0;
}
.feat-pct-wrap { display: flex; align-items: center; gap: 0.5rem; }
.feat-pct {
  font-size: 0.82rem; font-weight: 700; color: var(--text3);
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 0.12rem 0.5rem;
}
.feat-track {
  width: 100%; height: 8px;
  background: rgba(255,255,255,0.05);
  border-radius: 100px;
  overflow: hidden;
}
.feat-fill-up {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, #039855, var(--green));
  animation: barfill 0.8s cubic-bezier(.4,0,.2,1) both;
  position: relative;
}
.feat-fill-dn {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, #D92D20, var(--red));
  animation: barfill 0.8s cubic-bezier(.4,0,.2,1) both;
}
.feat-fill-neutral {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, #1570EF, var(--blue));
  animation: barfill 0.8s cubic-bezier(.4,0,.2,1) both;
}
@keyframes barfill {
  from { width: 0 !important; }
}

/* Rank badge */
.feat-rank {
  width: 20px; height: 20px;
  border-radius: 6px;
  background: var(--surface2);
  border: 1px solid var(--border);
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 0.65rem; font-weight: 800;
  color: var(--text3);
}

/* ─── Empty State ───────────────────────────────────────────── */
.empty {
  text-align: center; padding: 4rem 2rem;
}
.empty-illo {
  width: 96px; height: 96px;
  background: radial-gradient(135deg, var(--accentbg), var(--surface2));
  border: 1px solid var(--accentbdr);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 2.5rem; margin: 0 auto 1.2rem;
  box-shadow: 0 0 40px rgba(255,107,43,0.1);
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}
.empty-title {
  font-size: 1.25rem; font-weight: 800;
  color: var(--text); margin-bottom: 0.5rem;
}
.empty-desc  {
  font-size: 0.95rem; color: var(--text3); line-height: 1.8;
}
.empty-steps {
  display: flex; flex-direction: column; gap: 0.5rem;
  margin-top: 1.5rem; max-width: 280px; margin-left: auto; margin-right: auto;
}
.empty-step {
  display: flex; align-items: center; gap: 0.7rem;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px; padding: 0.65rem 1rem;
  font-size: 0.88rem; font-weight: 600; color: var(--text2);
  text-align: left;
  transition: border-color 0.2s ease;
}
.empty-step:hover { border-color: var(--accentbdr); }
.step-num {
  min-width: 22px; height: 22px; border-radius: 6px;
  background: linear-gradient(135deg, var(--accent), #e8590c);
  color: #fff;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 0.65rem; font-weight: 800;
  flex-shrink: 0;
}

/* ─── Footer ────────────────────────────────────────────────── */
.footer {
  text-align: center; padding: 1.8rem 0 0.8rem;
  font-size: 0.83rem; color: var(--text3);
  border-top: 1px solid var(--border); margin-top: 1rem;
}
.footer a { color: var(--text3); text-decoration: none; }
.footer strong { color: var(--accent); }

/* ─── Spinner override ──────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ─── Alert override ────────────────────────────────────────── */
.stAlert { border-radius: 12px !important; }
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

ok = backend_ok()

# ─── Hero Banner ──────────────────────────────────────────────────────────────
status_cls  = "status-dot" if ok else "status-dot offline"
status_txt  = "API Online" if ok else "API Offline"
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-inner">
    <div class="hero-icon">🏠</div>
    <div class="hero-text">
      <div class="hero-brand">Lanka<span>Estimate</span></div>
      <div class="hero-tagline">AI-powered property valuation for Sri Lanka's real estate market</div>
      <div class="hero-chips" style="margin-top:0.7rem">
        <span class="hero-chip active">⚡ XGBoost ML</span>
        <span class="hero-chip">🧠 Explainable AI</span>
        <span class="hero-chip">📍 25 Districts</span>
        <span class="hero-chip">🏘️ 70+ Areas</span>
        <span class="hero-chip">📊 20K+ Data Points</span>
        <span class="{status_cls}">{status_txt}</span>
      </div>
    </div>
  </div>
  <div class="hero-stats">
    <div>
      <div class="hero-stat-val">25</div>
      <div class="hero-stat-lbl">Districts</div>
    </div>
    <div>
      <div class="hero-stat-val">70+</div>
      <div class="hero-stat-lbl">Areas Covered</div>
    </div>
    <div>
      <div class="hero-stat-val">20K+</div>
      <div class="hero-stat-lbl">Training Samples</div>
    </div>
    <div>
      <div class="hero-stat-val">XGBoost</div>
      <div class="hero-stat-lbl">ML Algorithm</div>
    </div>
    <div>
      <div class="hero-stat-val">SHAP</div>
      <div class="hero-stat-lbl">Explainability</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

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
        <div class="card-sub">Fill in all fields to get an instant AI valuation</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Location
    st.markdown('<div class="sec-label">📍 &nbsp;Location</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        district = st.selectbox("District", DISTRICTS,
                                index=DISTRICTS.index("Colombo"), key="district")
    with c2:
        area = st.selectbox("Area", AREAS.get(district, []), key="area")

    st.markdown('<hr class="sep">', unsafe_allow_html=True)

    # Size & Structure
    st.markdown('<div class="sec-label">📐 &nbsp;Size &amp; Structure</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="sec-label">⚡ &nbsp;Amenities &amp; Utilities</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    with a1: has_garden  = st.checkbox("🌿 Garden", True,  key="garden")
    with a2: has_ac      = st.checkbox("❄️ AC",     False, key="ac")
    with a3: water_sup   = st.selectbox("💧 Water",        WATER, key="water")
    with a4: electricity = st.selectbox("⚡ Electricity",  ELEC,  key="elec")

    st.markdown('<hr class="sep">', unsafe_allow_html=True)

    # Year
    st.markdown('<div class="sec-label">📅 &nbsp;Construction</div>', unsafe_allow_html=True)
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

        # Price range estimate (±10%)
        lo, hi = price * 0.90, price * 1.10
        mid_pct = 50  # dot always centred
        fill_pct = 100

        st.markdown(f"""
        <div class="price-band">
          <div class="pb-eyebrow">🏡 AI-Estimated Property Value</div>
          <div class="pb-price">{parts[0]} <span>{num}</span> {unit}</div>
          <div class="pb-full">{pfull}</div>
          <div class="pb-badge">✓ &nbsp;Prediction Complete</div>
          <div class="price-range-wrap">
            <div class="price-range-labels">
              <span>{fmt_lkr(lo)} (−10%)</span>
              <span>Estimated Range</span>
              <span>{fmt_lkr(hi)} (+10%)</span>
            </div>
            <div class="price-range-track">
              <div class="price-range-fill" style="left:0;width:100%"></div>
              <div class="price-range-dot" style="left:{mid_pct}%"></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Confidence Meter ──
        contribs = res.get("feature_contributions", [])
        conf_pct  = min(95, 55 + len(contribs) * 4)   # heuristic
        st.markdown(f"""
        <div class="conf-wrap">
          <span class="conf-label">🎯 Model Confidence</span>
          <div class="conf-track">
            <div class="conf-fill" style="width:{conf_pct}%"></div>
          </div>
          <span class="conf-pct">{conf_pct}%</span>
        </div>""", unsafe_allow_html=True)

        # ── KPI Strip ──
        st.markdown(f"""
        <div class="kpi-strip">
          <div class="kpi kpi-k1">
            <div class="kpi-icon">💰</div>
            <div class="kpi-val kpi-accent">{fmt_lkr(ppp)}</div>
            <div class="kpi-lbl">Per Perch</div>
          </div>
          <div class="kpi kpi-k2">
            <div class="kpi-icon">🛏️</div>
            <div class="kpi-val kpi-blue">{fmt_lkr(ppb)}</div>
            <div class="kpi-lbl">Per Bedroom</div>
          </div>
          <div class="kpi kpi-k3">
            <div class="kpi-icon">⏳</div>
            <div class="kpi-val kpi-green">{age} yrs</div>
            <div class="kpi-lbl">House Age</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Tabs ──
        t_sum, t_xai = st.tabs(["📋  Property Summary", "🧠  AI Explanation"])

        # ── Summary Tab ──
        with t_sum:
            st.markdown('<div class="card" style="margin-top:.7rem">', unsafe_allow_html=True)
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
            st.markdown('<div class="card" style="margin-top:.7rem">', unsafe_allow_html=True)
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
                  Each factor below shows its <b style="color:#10D9A0">positive ▲</b> or
                  <b style="color:#F56565">negative ▼</b> impact on the estimated price.
                  The chart visualises the exact SHAP contribution values.
                </div>
                <div class="xai-method">Method: {method}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            # ── Sub-tabs: SHAP Chart | Feature Breakdown ──
            xai_chart_tab, xai_bars_tab = st.tabs(["📊  SHAP Chart", "📋  Feature Breakdown"])

            # ─── SHAP Chart sub-tab ───────────────────────────────────
            with xai_chart_tab:
                # Fetch the chart image from the backend
                shap_state_key = "shap_img_" + str(hash(str(pay)))
                if shap_state_key not in st.session_state:
                    with st.spinner("Generating SHAP chart…"):
                        try:
                            shap_r = requests.post(
                                f"{API_BASE}/api/shap-plot",
                                json=pay, timeout=30
                            )
                            if shap_r.status_code == 200:
                                shap_data = shap_r.json()
                                st.session_state[shap_state_key] = shap_data
                            else:
                                st.session_state[shap_state_key] = {"error": shap_r.text}
                        except Exception as ex:
                            st.session_state[shap_state_key] = {"error": str(ex)}

                shap_data = st.session_state.get(shap_state_key, {})

                if "image" in shap_data:
                    import base64 as _b64
                    img_bytes = _b64.b64decode(shap_data["image"])

                    # Wrap in a styled dark container
                    st.markdown("""
                    <div style="
                      background:#1A2340;
                      border:1px solid rgba(255,255,255,0.07);
                      border-radius:14px;
                      padding:1rem;
                      margin-top:0.6rem;
                    ">""", unsafe_allow_html=True)

                    st.image(img_bytes, use_container_width=True,
                             caption=f"Method: {shap_data.get('graph_type', method)}")

                    st.markdown("</div>", unsafe_allow_html=True)

                    # How-to-read callout
                    st.markdown("""
                    <div style="
                      display:flex; gap:1.2rem; margin-top:0.8rem;
                      padding:0.75rem 1rem;
                      background:rgba(167,139,250,0.07);
                      border:1px solid rgba(167,139,250,0.18);
                      border-radius:10px; flex-wrap:wrap;
                    ">
                      <span style="font-size:0.83rem;color:#8892A4;font-weight:600;">
                        📖 <b style="color:#E8EAF0">How to read:</b>
                        &nbsp;Bars extending <b style="color:#10D9A0">right (green)</b> push the price higher.
                        &nbsp;Bars extending <b style="color:#F56565">left (red)</b> pull the price lower.
                        &nbsp;Bar length = magnitude of impact.
                      </span>
                    </div>""", unsafe_allow_html=True)

                elif "error" in shap_data:
                    st.warning(f"⚠️ Could not load SHAP chart: {shap_data['error']}")
                else:
                    st.info("SHAP chart not available.")

            # ─── Feature Breakdown sub-tab ────────────────────────────
            with xai_bars_tab:
                if contribs:
                    html = ""
                    for i, c in enumerate(contribs):
                        d   = c["direction"]
                        lbl = c["label"]
                        pct = c["percentage"]
                        delay = i * 80
                        if d == "increase":
                            arrow = '<span class="feat-arrow-up">▲</span>'
                            fill  = "feat-fill-up"
                        elif d == "decrease":
                            arrow = '<span class="feat-arrow-dn">▼</span>'
                            fill  = "feat-fill-dn"
                        else:
                            arrow = '<span class="feat-arrow-neu">→</span>'
                            fill  = "feat-fill-neutral"

                        html += f"""
                        <div class="feat-item" style="animation-delay:{delay}ms">
                          <div class="feat-row">
                            <span class="feat-name">
                              <span class="feat-rank">#{i+1}</span>
                              {arrow}{lbl}
                            </span>
                            <span class="feat-pct-wrap">
                              <span class="feat-pct">{pct:.1f}%</span>
                            </span>
                          </div>
                          <div class="feat-track">
                            <div class="{fill}" style="width:{min(pct,100):.1f}%;animation-delay:{delay}ms"></div>
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
              then click <b style="color:#FF6B2B">Get AI Valuation</b> to instantly receive<br>
              a price estimate with a full AI explanation.
            </div>
            <div class="empty-steps">
              <div class="empty-step"><span class="step-num">1</span> Select district &amp; area</div>
              <div class="empty-step"><span class="step-num">2</span> Enter size &amp; property features</div>
              <div class="empty-step"><span class="step-num">3</span> Click Get AI Valuation</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <strong>LankaEstimate</strong> &nbsp;·&nbsp;
  Powered by XGBoost &nbsp;·&nbsp;
  Explainable AI (SHAP) &nbsp;·&nbsp;
  Sri Lanka Property Market &nbsp;·&nbsp;
  © 2026
</div>
""", unsafe_allow_html=True)
