import streamlit as st
import pandas as pd
import joblib

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Titanic Survival Predictor",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

/* ── App background ── */
.stApp {
    background: #0d1b2a;
    color: #e8dcc8;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 960px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0a141f 0%, #112233 50%, #0d1b2a 100%);
    border: 1px solid rgba(180,140,80,0.3);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(180,140,80,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #c8a96e;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1.05rem;
    color: #9fb3c8;
    margin: 0;
    line-height: 1.6;
    font-weight: 300;
}
.hero .badge {
    display: inline-block;
    background: rgba(180,140,80,0.15);
    border: 1px solid rgba(180,140,80,0.4);
    color: #c8a96e;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* ── Section cards ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #c8a96e;
    margin: 0 0 1.2rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    color: #9fb3c8 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e8dcc8 !important;
    border-radius: 8px !important;
}
div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(180,140,80,0.5) !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c8a96e, #a07840) !important;
    color: #0d1b2a !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
}

/* ── Result boxes ── */
.result-survived {
    background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(16,185,129,0.08));
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    text-align: center;
    animation: fadeIn 0.5s ease;
}
.result-perished {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(185,28,28,0.08));
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    text-align: center;
    animation: fadeIn 0.5s ease;
}
.result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
}
.result-sub { font-size: 0.9rem; color: #9fb3c8; margin: 0; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Info stat boxes ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-bottom: 1.4rem;
}
.stat-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #c8a96e;
    font-weight: 700;
}
.stat-label { font-size: 0.75rem; color: #6b8299; text-transform: uppercase; letter-spacing: 0.8px; }

/* ── Divider ── */
.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(180,140,80,0.4), transparent);
    margin: 1.5rem 0;
}

/* ── Class badge colors ── */
.cls-1 { color: #ffd700; }
.cls-2 { color: #c0c0c0; }
.cls-3 { color: #cd7f32; }

/* ── Feature guide & model info text ── */
.fg-label { color: #c8a96e; font-weight: 700; }
.fg-text  { color: #9fb3c8; font-size: 0.85rem; line-height: 1.6; }
.fg-row   { margin-bottom: 0.85rem; }
.mi-label { color: #e8dcc8; font-weight: 600; }
.mi-text  { color: #9fb3c8; }
</style>
""", unsafe_allow_html=True)

# ── Load model ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model  = joblib.load("titanic_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

model, scaler = load_artifacts()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">🚢 Machine Learning Project</div>
    <h1>Titanic Survival Predictor</h1>
    <p>Enter a passenger's profile below to predict their likelihood of surviving<br>
    the RMS Titanic disaster of April 15, 1912, based on historical data.</p>
</div>
""", unsafe_allow_html=True)

# ── Dataset overview ─────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-grid">
    <div class="stat-box">
        <div class="stat-value">891</div>
        <div class="stat-label">Training Samples</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">38.4%</div>
        <div class="stat-label">Survival Rate</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">7</div>
        <div class="stat-label">Input Features</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: two columns ───────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="card"><div class="card-title">👤 Passenger Profile</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        pclass = st.selectbox("Passenger Class", [1, 2, 3],
                              format_func=lambda x: f"Class {x} — {'First' if x==1 else 'Second' if x==2 else 'Third'}")
        age    = st.number_input("Age (years)", min_value=0, max_value=120, value=30)
        sibsp  = st.number_input("Siblings / Spouse aboard", min_value=0, max_value=10, value=0)

    with c2:
        sex      = st.selectbox("Sex", ["Male", "Female"])
        fare     = st.number_input("Fare paid (£)", min_value=0.0, max_value=600.0, value=32.0, step=0.5)
        parch    = st.number_input("Parents / Children aboard", min_value=0, max_value=10, value=0)

    embarked = st.selectbox("Port of Embarkation", ["S", "C", "Q"])

    st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button("⚓  Predict Survival", use_container_width=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 Feature Guide</div>
        <hr class="gold-divider">
        <div class="fg-row fg-text">
            <span class="fg-label">Passenger Class</span><br>
            <span class="cls-1">■</span> 1st — Upper &nbsp;|&nbsp;
            <span class="cls-2">■</span> 2nd — Middle &nbsp;|&nbsp;
            <span class="cls-3">■</span> 3rd — Lower
        </div>
        <div class="fg-row fg-text">
            <span class="fg-label">Fare</span><br>
            Ticket price in British pounds. Higher fares linked to 1st class cabins nearer lifeboats.
        </div>
        <div class="fg-row fg-text">
            <span class="fg-label">SibSp</span><br>
            Siblings or spouses travelling aboard together.
        </div>
        <div class="fg-row fg-text">
            <span class="fg-label">Parch</span><br>
            Parents or children travelling aboard together.
        </div>
        <div class="fg-row fg-text" style="margin-bottom:0">
            <span class="fg-label">Embarked</span><br>
            S — Southampton &nbsp;|&nbsp; C — Cherbourg &nbsp;|&nbsp; Q — Queenstown
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">🤖 Model Info</div>
        <hr class="gold-divider">
        <table style="width:100%;border-collapse:collapse;font-size:0.85rem">
            <tr><td style="padding:5px 0;color:#6b8299;width:45%">Algorithm</td>
                <td style="padding:5px 0;color:#e8dcc8">Scikit-learn classifier</td></tr>
            <tr><td style="padding:5px 0;color:#6b8299">Preprocessing</td>
                <td style="padding:5px 0;color:#e8dcc8">StandardScaler</td></tr>
            <tr><td style="padding:5px 0;color:#6b8299">Dataset</td>
                <td style="padding:5px 0;color:#e8dcc8">Kaggle Titanic</td></tr>
            <tr><td style="padding:5px 0;color:#6b8299">Task</td>
                <td style="padding:5px 0;color:#e8dcc8">Binary Classification</td></tr>
            <tr><td style="padding:5px 0;color:#6b8299">Output</td>
                <td style="padding:5px 0;color:#e8dcc8">Survived / Not Survived</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ── Prediction logic ──────────────────────────────────────────────────────────
if predict_btn:
    sex_enc      = 0 if sex == "Male" else 1
    embarked_enc = {"S": 0, "C": 1, "Q": 2}[embarked]

    input_df = pd.DataFrame(
        [[pclass, sex_enc, age, fare, sibsp, parch, embarked_enc]],
        columns=["Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
    )
    input_scaled = scaler.transform(input_df)
    prediction   = model.predict(input_scaled)[0]

    st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)

    if prediction == 1:
        st.markdown("""
        <div class="result-survived">
            <div class="result-icon">🟢</div>
            <div class="result-title" style="color:#4ade80">Survived</div>
            <p class="result-sub">Based on the provided profile, this passenger<br>
            is predicted to have <b>survived</b> the Titanic disaster.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-perished">
            <div class="result-icon">🔴</div>
            <div class="result-title" style="color:#f87171">Did Not Survive</div>
            <p class="result-sub">Based on the provided profile, this passenger<br>
            is predicted to have <b>perished</b> in the Titanic disaster.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Input summary table ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 View Input Summary"):
        summary = pd.DataFrame({
            "Feature": ["Passenger Class", "Sex", "Age", "Fare (£)", "Siblings/Spouse", "Parents/Children", "Embarked"],
            "Value":   [f"Class {pclass}", sex, age, f"£{fare:.2f}", sibsp, parch,
                        {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}[embarked]]
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr class="gold-divider">
<p style="text-align:center;font-size:0.78rem;color:#3d5166;margin-top:1rem">
    Built for ML study &nbsp;·&nbsp; Titanic dataset via Kaggle &nbsp;·&nbsp;
    Powered by Scikit-learn &nbsp;&amp;&nbsp; Streamlit
</p>
""", unsafe_allow_html=True)
