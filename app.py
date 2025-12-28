import streamlit as st
import joblib
import numpy as np

# ==================================================
# Page Config
# ==================================================
st.set_page_config(
    page_title="Mental Health Risk Detection",
    page_icon="🧠",
    layout="centered"
)

# ==================================================
# Emergency Resources (By Country)
# ==================================================
EMERGENCY_RESOURCES = {
    "India": {
        "number": "9152987821",
        "text": "AASRA – 24x7 Suicide Prevention Helpline",
        "url": "https://www.aasra.info/"
    },
    "United States": {
        "number": "988",
        "text": "988 Suicide & Crisis Lifeline",
        "url": "https://988lifeline.org/"
    },
    "United Kingdom": {
        "number": "116 123",
        "text": "Samaritans",
        "url": "https://www.samaritans.org/"
    },
    "Canada": {
        "number": "1-833-456-4566",
        "text": "Talk Suicide Canada",
        "url": "https://talksuicide.ca/"
    },
    "Australia": {
        "number": "13 11 14",
        "text": "Lifeline Australia",
        "url": "https://www.lifeline.org.au/"
    },
    "Other": {
        "number": "Local emergency number",
        "text": "Find local crisis support",
        "url": "https://findahelpline.com/"
    }
}

def show_emergency_resources(country):
    data = EMERGENCY_RESOURCES.get(country, EMERGENCY_RESOURCES["Other"])
    st.markdown(
        f"""
        <div style="padding:20px; background:#4b1f1f; border-radius:14px; color:white;">
        <h3>🚨 Immediate Support Available</h3>
        <p><b>{data['text']}</b></p>
        <p>📞 <b>{data['number']}</b></p>
        <p>🌐 <a href="{data['url']}" target="_blank" style="color:#ffd166;">
        Visit website</a></p>
        <p style="margin-top:10px;">
        If you are in immediate danger, please contact local emergency services.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# Load Model & Vectorizer
# ==================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load("risk_model.pkl")
    tfidf = joblib.load("tfidf_vectorizer.pkl")
    return model, tfidf

model, tfidf = load_artifacts()

# ==================================================
# Rule-based Phrase Lists
# ==================================================
CRITICAL_PHRASES = [
    "want to disappear", "end it all", "kill myself",
    "no reason to live", "better off dead",
    "suicide", "end my life", "give up on life", "depressed"
]

POSITIVE_PHRASES = [
    "happy", "excited", "confident", "optimistic",
    "grateful", "content", "peaceful", "calm"
]

def contains_critical_phrase(text):
    text = text.lower()
    return any(p in text for p in CRITICAL_PHRASES)

def contains_positive_phrase(text):
    text = text.lower()
    return any(p in text for p in POSITIVE_PHRASES)

# ==================================================
# UI Header
# ==================================================
st.title("🧠 Mental Health Risk Detection")
st.write(
    "Analyze text to assess **potential mental health risk levels**.\n\n"
    "_This tool is for educational purposes only._"
)

st.divider()

# ==================================================
# Country Selector
# ==================================================
country = st.selectbox(
    "🌍 Select your country (for emergency resources)",
    list(EMERGENCY_RESOURCES.keys()),
    index=0
)

# ==================================================
# Input
# ==================================================
st.subheader("✍️ Enter text")
user_text = st.text_area(
    "",
    height=160,
    placeholder="Example: I feel overwhelmed and anxious lately..."
)

# ==================================================
# Analyze Button
# ==================================================
if st.button("🔍 Analyze Risk"):

    if len(user_text.strip()) < 5:
        st.warning("Please enter a longer message for meaningful analysis.")
        st.stop()

    # --------------------------------------------------
    # CRITICAL OVERRIDE (Highest Priority)
    # --------------------------------------------------
    if contains_critical_phrase(user_text):
        st.error("🔴 **High Risk Detected**")
        st.progress(1.0)

        show_emergency_resources(country)

        st.caption(
            "⚠️ This tool does not provide medical advice. "
            "Please seek professional help if needed."
        )
        st.stop()

    # --------------------------------------------------
    # POSITIVE OVERRIDE
    # --------------------------------------------------
    if contains_positive_phrase(user_text):
        st.success("🟢 **Low Risk Detected**")
        st.progress(0.1)

        st.markdown(
            """
            <div style="padding:18px; background:#143d2b; border-radius:12px; color:white;">
            <h4>🌱 Positive emotional signals detected</h4>
            <p>Your message reflects generally positive or healthy emotions.</p>
            <b>Risk Probability:</b> Very Low<br>
            <b>Model Confidence:</b> Rule-based
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "⚠️ This tool does not provide medical advice."
        )
        st.stop()

    # --------------------------------------------------
    # ML MODEL DECISION
    # --------------------------------------------------
    X = tfidf.transform([user_text])
    proba_high = model.predict_proba(X)[0][0]

    if proba_high >= 0.60:
        st.error("🔴 **High Risk Detected**")
        st.progress(1.0)

        show_emergency_resources(country)

    elif proba_high >= 0.45:
        st.warning("🟠 **Moderate Risk Detected**")
        st.progress(proba_high)

        st.info(
            "💡 It might help to pause, reflect, or talk things out with someone you trust."
        )

    else:
        st.success("🟢 **Low / No Risk Detected**")
        st.progress(proba_high)

        st.markdown(
            "🌱 Your message does not show strong distress signals."
        )

    st.caption(
        "⚠️ This tool does **not** provide medical advice. "
        "If you or someone you know is struggling, please seek professional help."
    )
