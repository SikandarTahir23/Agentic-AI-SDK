import streamlit as st
import os
from dotenv import load_dotenv

# --- Load API Key ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("❌ GEMINI_API_KEY environment variable is not set.")
    st.stop()

# --- Agentic SDK ---
from agents import (
    Runner,
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    function_tool
)

# --- External Gemini Client Setup ---
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

# --- Calculator Tool (No args in decorator) ---
@function_tool
def calculate(expression: str) -> str:
    """Solves basic math expressions like '5 * (2 + 3)'"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- Career Advisor Agent (No tools) ---
career_agent = Agent(
    name="CareerAdvisor",
    instructions="You're a career counselor. Guide users in choosing their career path.",
    tools=[],
    model=model,
)

# --- Main Agent (With calculator tool) ---
main_agent = Agent(
    name="MainAgent",
    instructions="You're an AI assistant. Use tools to solve math problems. For any career-related queries, reply politely but directly.",
    tools=[calculate],
    model=model,
)

# --- UI Setup ---
st.set_page_config(page_title="🎓 AI Career & Math Advisor", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    body { background-color: #111111; color: white; }
    .main {
        background: rgba(255,255,255,0.05);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 30px;
        box-shadow: 0 0 25px rgba(0,255,200,0.08);
    }
    .stTextArea textarea {
        background-color: #1c1c1c;
        color: white;
        border: 1px solid #444;
        border-radius: 8px;
    }
    .stButton button {
        background: linear-gradient(90deg, #00FFE0, #4A90E2);
        color: black;
        font-weight: bold;
        border-radius: 25px;
        padding: 10px 24px;
        box-shadow: 0px 0px 10px #00FFF7;
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 20px #00EFFF;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class='main'>
        <h1 style='text-align:center; color:#00FFF7;'>🎓 AI Career & Math Advisor</h1>
        <p style='text-align:center; color:#CCCCCC;'>Ask any math question or get career advice powered by Gemini + Agentic SDK.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Input ---
st.markdown("### 🤔 What's your question?")
query = st.text_area("Ask about a career or a math problem:", placeholder="e.g. What is (5 * 3) + 2? OR Suggest me a career in AI...")

# --- Action ---
if st.button("🚀 Get Answer") and query.strip():
    with st.spinner("Thinking with AI power..."):
        import asyncio

        # 🔁 Manual Handoff
        selected_agent = (
            career_agent if any(x in query.lower() for x in ["career", "job", "profession", "future"])
            else main_agent
        )

        result = asyncio.run(
            Runner.run(
                input=query,
                starting_agent=selected_agent,
                run_config=config
            )
        )

        # --- Output ---
        st.markdown("### ✅ AI Response")
        st.success(result.final_output)

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align:center;'>Made by <b>Sikandar Tahir</b> | Powered by <b>Gemini + Agentic SDK</b> 🤖</div>", unsafe_allow_html=True)
