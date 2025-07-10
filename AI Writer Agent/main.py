import streamlit as st
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check API Key
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please define it in your .env file.")

# Setup Gemini-compatible OpenAI client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

# Config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Writer Agent
writer = Agent(
    name='Writer Agent',
    instructions="""You are a writer agent. Generate poem,
    stories, essay, email etc."""
)

# Async call
async def run_agent(prompt: str):
    response = await Runner.run(
        writer,
        input=prompt,
        run_config=config
    )
    return response.final_output

# -----------------------------
# Streamlit UI Enhancements
# -----------------------------

# Page settings
st.set_page_config(
    page_title="AI Writer Agent",
    page_icon="✍️",
    layout="centered"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stTextArea textarea {
        border-radius: 10px;
        padding: 10px;
        font-size: 1rem;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3c7dcf;
    }
    </style>
""", unsafe_allow_html=True)

# Title & subtitle
st.markdown("<h1 style='text-align: center;'>🧠 AI Writer Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate poems, stories, essays, emails, and more using AI Agent</p>", unsafe_allow_html=True)

# Input
user_input = st.text_area("Enter your prompt below:", placeholder="e.g., Write a short story about AI saving the world.", height=180)

# Button
if st.button("✍️ Generate Content"):
    if user_input.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("🌀 Generating with Gemini..."):
            response = asyncio.run(run_agent(user_input))
        st.success("✅ Done!")
        st.markdown("### 📄 Generated Output:")
        with st.expander("Click to view output", expanded=True):
            st.markdown(response)
st.markdown("---")
st.markdown("🚀 Made with ❤️ by Sikandar Tahir")    