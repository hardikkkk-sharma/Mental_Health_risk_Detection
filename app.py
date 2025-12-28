
import streamlit as st

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="MindGuard AI",
    page_icon="🧠",
    layout="centered"
)

# =========================================================
# Rule-based Phrase Lists (DEFINE ONCE)
# =========================================================
CRITICAL_PHRASES = [
    "want to disappear",
    "kill myself",
    "end my life",
    "no reason to live",
    "better off dead",
    "suicidal",
    "can't go on",
    "give up on life"
]

POSITIVE_PHRASES = [
    "happy",
    "excited",
    "confident",
    "optimistic",
    "calm",
    "relaxed",
    "grateful",
    "content"
]

# =========================================================
# Analysis Logic
# =========================================================
def analyze_text(text: str):
    text = text.lower()

    if any(p in text for p in CRITICAL_PHRASES):
        return "High", 0.95, "High"

    if any(p in text for p in POSITIVE_PHRASES):
        return "Low", 0.05, "High"

    return "Moderate", 0.50, "Medium"

# =========================================================
# Emergency Resources
# =========================================================
def show_emergency_resources(country):
    resources = {
        "India": "📞 AASRA: 91-9820466726",
        "USA": "📞 988 Suicide & Crisis Lifeline",
        "UK": "📞 Samaritans: 116 123",
        "Australia": "📞 Lifeline: 13 11 14"
    }

    st.markdown(
        f"""
        <div style="padding:15px; background:#1f2937; border-radius:10px;">
        <b>Emergency Support ({country})</b><br>
        {resources.get(country, "Contact local emergency services")}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# UI
# =========================================================
st.title("🧠 MindGuard AI")
st.write("Analyze text to assess **potential mental health risk levels**.")
st.caption("This tool is for educational purposes only.")

user_text = st.text_area(
    "✍️ Enter text",
    height=160,
    placeholder="Example: I feel overwhelmed and anxious lately..."
)

country = st.selectbox(
    "🌍 Select your country (for emergency resources)",
    ["India", "USA", "UK", "Australia", "Other"]
)

if st.button("🔍 Analyze Risk"):
    if len(user_text.strip()) < 5:
        st.warning("Please enter a longer message.")
    else:
        risk, prob, confidence = analyze_text(user_text)

        st.progress(prob)

        if risk == "High":
            st.error("🔴 **High Risk Detected**")
            show_emergency_resources(country)

        elif risk == "Moderate":
            st.warning("🟠 **Moderate Risk Detected**")

        else:
            st.success("🟢 **Low Risk Detected**")

        st.markdown(
            f"""
            <div style="padding:20px; background:#facc15; border-radius:15px; text-align:center;">
            <h3>{risk} Risk</h3>
            <h2>Risk Probability: {prob:.2f}</h2>
            <p>Model Confidence: {confidence}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("💡 It might help to pause, reflect, or talk with someone you trust.")

st.caption(
    "⚠️ This tool does NOT provide medical advice. "
    "If you or someone you know is struggling, seek professional help."
)
