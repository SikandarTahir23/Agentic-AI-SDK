
import streamlit as st
import os
from dotenv import load_dotenv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# --- Load API Key ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("❌ GEMINI_API_KEY environment variable is not set.")
    st.stop()

# --- Agentic SDK Setup (Placeholder for Gemini API) ---
try:
    from agents import (
        Runner,
        Agent,
        AsyncOpenAI,
        OpenAIChatCompletionsModel,
        RunConfig,
    )
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
except ImportError:
    st.warning("Agentic SDK not available. Using dummy functions for demo.")

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="🚀 AI Startup Co-founder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS for Styling ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1a1a3d, #2a2a5e);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin: 2rem auto;
        max-width: 800px;
    }
    .stTextArea textarea {
        background: #2a2a5e;
        color: #e0e0ff;
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton button {
        background: linear-gradient(90deg, #00d4ff, #7b61ff);
        color: white;
        font-weight: 600;
        border-radius: 30px;
        padding: 12px 30px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
    }
    h1, h2, h3 {
        color: #00d4ff;
        font-family: 'Arial', sans-serif;
    }
    .stExpander {
        background: #2a2a5e;
        border-radius: 10px;
        border: 1px solid #00d4ff;
    }
    .stExpander div[role="button"] {
        color: #e0e0ff;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header UI ---
with st.container():
    st.markdown("""
    <div class='main'>
        <h1 style='text-align:center;'>🤖 AI Virtual Startup Co-founder</h1>
        <p style='text-align:center; color:#b0b0ff;'>Turn your startup idea into a professional business plan with AI!</p>
    </div>
    """, unsafe_allow_html=True)

# --- Input Section ---
st.markdown("### 💡 Share Your Startup Idea")
idea = st.text_area(
    "Describe your idea in detail:",
    placeholder="e.g., A wearable that tracks hydration levels and syncs with a mobile app...",
    height=150
)

# --- Gemini API Integration (Placeholder) ---
def call_gemini_api(idea, prompt):
    # Placeholder for actual API call
    try:
        # Example: Replace with actual Gemini API call
        response = model.generate_content(prompt + idea)  # Hypothetical method
        return response.text
    except:
        # Fallback to dummy response
        return f"AI-generated response for: {idea}"

# --- Improved Dummy Functions (to be replaced with Gemini API) ---
def idea_refiner(idea):
    # Replace with: return call_gemini_api(idea, "Refine this startup idea: ")
    return f"A refined solution: **{idea}** with AI-driven optimization."

def business_model(idea):
    # Replace with: return call_gemini_api(idea, "Generate a business model for: ")
    return f"""
    - **Problem**: Lack of efficient solutions for {idea.lower()}
    - **Solution**: AI-powered platform for {idea.lower()}
    - **Revenue**: Subscription-based + 5% transaction fee
    """

def target_audience(idea):
    # Replace with: return call_gemini_api(idea, "Identify target audience for: ")
    return f"""
    - Young professionals
    - Tech-savvy {idea.lower()} enthusiasts
    - Small businesses
    """

def pricing_strategy(idea):
    # Replace with: return call_gemini_api(idea, "Suggest pricing strategy for: ")
    return f"""
    - **Free Tier**: Basic features
    - **Pro Tier**: $15/month for advanced analytics
    - **Enterprise**: Custom pricing
    """

def pitch_deck_content(idea):
    # Replace with: return call_gemini_api(idea, "Create pitch deck content for: ")
    return f"""
    ### Pitch Deck Slides
    1. **Problem**: Inefficiencies in {idea.lower()}
    2. **Solution**: AI-driven {idea.lower()} platform
    3. **Market**: $5B+ global market
    4. **Revenue Model**: Subscription + Transaction fees
    5. **Go-to-Market**: Social media campaigns, partnerships
    6. **Funding Ask**: $100K for MVP development
    """

# --- Generate PDF Report ---
def generate_pdf_report(idea, refined, model, audience, pricing, deck):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.cyan)
    c.drawString(50, 750, "AI Startup Co-founder Report")
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    y = 720
    c.drawString(50, y, "Refined Idea:")
    y -= 20
    c.drawString(50, y, refined)
    
    y -= 40
    c.drawString(50, y, "Business Model:")
    for line in model.split("\n"):
        c.drawString(50, y, line.strip())
        y -= 20
    
    y -= 20
    c.drawString(50, y, "Target Audience:")
    for line in audience.split("\n"):
        c.drawString(50, y, line.strip())
        y -= 20
    
    y -= 20
    c.drawString(50, y, "Pricing Strategy:")
    for line in pricing.split("\n"):
        c.drawString(50, y, line.strip())
        y -= 20
    
    y -= 20
    c.drawString(50, y, "Pitch Deck Content:")
    for line in deck.split("\n")[:5]:  # Limit for brevity
        c.drawString(50, y, line.strip())
        y -= 20
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- Generate Button and Output ---
if st.button("🚀 Generate Startup Plan") and idea.strip():
    with st.spinner("⏳ Crafting your AI-powered business plan..."):
        # Generate outputs
        refined = idea_refiner(idea)
        model = business_model(idea)
        audience = target_audience(idea)
        pricing = pricing_strategy(idea)
        deck = pitch_deck_content(idea)

        # Display outputs in expanders
        with st.expander("✅ Refined Idea", expanded=True):
            st.markdown(f"<div style='background:#1a3c34;padding:16px;border-radius:10px;color:#e6ffec;'>{refined}</div>", unsafe_allow_html=True)

        with st.expander("🧱 Business Model Canvas"):
            st.markdown(f"<div style='background:#2a2a5e;padding:16px;border-radius:10px;color:#e0e0ff;'>{model}</div>", unsafe_allow_html=True)

        with st.expander("👥 Target Audience"):
            st.markdown(f"<div style='background:#2a2a5e;padding:16px;border-radius:10px;color:#e0e0ff;'>{audience}</div>", unsafe_allow_html=True)

        with st.expander("💰 Pricing Strategy"):
            st.markdown(f"<div style='background:#2a2a5e;padding:16px;border-radius:10px;color:#e0e0ff;'>{pricing}</div>", unsafe_allow_html=True)

        with st.expander("📊 Pitch Deck Content"):
            st.markdown(deck)

        # Downloadable PDF
        pdf_buffer = generate_pdf_report(idea, refined, model, audience, pricing, deck)
        st.download_button(
            label="📥 Download Business Plan PDF",
            data=pdf_buffer,
            file_name="startup_plan.pdf",
            mime="application/pdf"
        )

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#b0b0ff;'>Made by <b>Sikandar Tahir</b> | Powered by <b>Gemini + Agentic SDK</b> 💻</div>",
    unsafe_allow_html=True
)