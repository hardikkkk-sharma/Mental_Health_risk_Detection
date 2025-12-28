import streamlit as st
import joblib
import os

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="Mental Health Risk Detection",
    page_icon="🧠",
    layout="centered"
)

# =========================================================
# Title & Description
# =========================================================
st.markdown(
    """
    <h1 style="text-align:center;">🧠 Mental Health Risk Detection</h1>
    <p style="text-align:center; color:#9ca3af;">
    Analyze text to assess potential mental health risk levels.
    </p>
    <p style="text-align:center; font-style:italic; color:#6b7280;">
    This tool is for educational purposes only.
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# =========================================================
# Emergency Resources
# =========================================================
def show_emergency_resources(country):
    resources = {
        "India": {
            "name": "AASRA",
            "phone": "+91 9820466726",
            "url": "https://www.aasra.info"
        },
        "USA": {
            "name": "988 Suicide & Crisis Lifeline",
            "phone": "988",
            "url": "https://988lifeline.org"
        },
        "UK": {
            "name": "Samaritans",
            "phone": "116 123",
            "url": "https://www.samaritans.org"
        },
        "Australia": {
            "name": "Lifeline",
            "phone": "13 11 14",
            "url": "https://www.lifeline.org.au"
        }
    }

    data = resources.get(country)

    if data:
        st.markdown(
            f"""
            <div style="
                padding:18px;
                background:#1f2937;
                border-radius:12px;
                border-left:6px solid #ef4444;
            ">
            <h4>🚨 Emergency Support – {country}</h4>
            <p><b>{data['name']}</b></p>
            <p>📞 <b>{data['phone']}</b></p>
            <p>🌐 <a href="{data['url']}" target="_blank" style="color:#60a5fa;">
                Visit Official Website
            </a></p>
            <p style="margin-top:10px;">
            If you are in immediate danger, please contact local emergency services.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(
            "🚨 Please contact your local emergency services or a trusted mental health professional."
        )

# =========================================================
# Rule-Based Phrase Lists
# =========================================================
CRITICAL_PHRASES = [
    "want to disappear", "kill myself", "end my life",
    "suicide", "better off dead", "can't go on",
    "give up on life", "no reason to live", "depressed", "die", "kill"
]

POSITIVE_PHRASES = [
    "happy", "excited", "confident", "optimistic",
    "calm", "relaxed", "grateful", "content", "motivated"
]

# =========================================================
# Load ML Model (Optional)
# =========================================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load("risk_model.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
        return model, vectorizer
    except:
        return None, None

model, vectorizer = load_model()

# =========================================================
# Text Analysis Logic
# =========================================================
def analyze_text(text):
    text = text.lower()

    # 1️⃣ Critical rule-based override
    if any(p in text for p in CRITICAL_PHRASES):
        return "High", 0.95, "High"

    # 2️⃣ Positive override
    if any(p in text for p in POSITIVE_PHRASES):
        return "Low", 0.05, "High"

    # 3️⃣ ML fallback (if available)
    if model and vectorizer:
        X = vectorizer.transform([text])
        proba = model.predict_proba(X)[0][0]

        if proba >= 0.60:
            return "High", proba, "Medium"
        elif proba >= 0.45:
            return "Moderate", proba, "Medium"
        else:
            return "Low", proba, "Low"

    # 4️⃣ Safe default
    return "Moderate", 0.50, "Low"

# =========================================================
# User Input
# =========================================================
st.markdown("### ✍️ Enter text")
user_text = st.text_area(
    "",
    height=160,
    placeholder="Example: I feel overwhelmed and anxious lately..."
)

country = st.selectbox(
    "🌍 Select your country (for emergency resources)",
    ["India", "USA", "UK", "Australia"]
)

# =========================================================
# Analyze Button
# =========================================================
if st.button("🔍 Analyze Risk"):
    if len(user_text.strip()) < 5:
        st.warning("Please enter a longer message for better analysis.")
    else:
        risk, probability, confidence = analyze_text(user_text)

        # Progress bar
        st.progress(probability)

        # =================================================
        # Output UI
        # =================================================
        if risk == "High":
            st.markdown(
                f"""
                <div style="
                    background:linear-gradient(135deg,#7f1d1d,#ef4444);
                    padding:25px;
                    border-radius:16px;
                    color:white;
                    text-align:center;
                ">
                <h2>🔴 High Risk Detected</h2>
                <h3>Risk Probability: {probability:.2f}</h3>
                <p>Model Confidence: {confidence}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            show_emergency_resources(country)

        elif risk == "Moderate":
            st.markdown(
                f"""
                <div style="
                    background:linear-gradient(135deg,#92400e,#facc15);
                    padding:25px;
                    border-radius:16px;
                    color:black;
                    text-align:center;
                ">
                <h2>🟠 Moderate Risk Detected</h2>
                <h3>Risk Probability: {probability:.2f}</h3>
                <p>Model Confidence: {confidence}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info("💡 It may help to pause, reflect, or talk with someone you trust.")

        else:
            st.markdown(
                f"""
                <div style="
                    background:linear-gradient(135deg,#065f46,#10b981);
                    padding:25px;
                    border-radius:16px;
                    color:white;
                    text-align:center;
                ">
                <h2>🟢 Low / No Risk Detected</h2>
                <h3>Risk Probability: {probability:.2f}</h3>
                <p>Model Confidence: {confidence}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success("🌱 You’re expressing positive emotional signals.")

# =========================================================
# Footer Disclaimer
# =========================================================
st.markdown(
    """
    <hr>
    <p style="color:#9ca3af; font-size:0.9em;">
    ⚠️ This tool does <b>not</b> provide medical advice.
    If you or someone you know is struggling, please seek professional help.
    </p>
    """,
    unsafe_allow_html=True
)
