import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Gemini Agent dependencies
from agents import (
    Runner,
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    function_tool
)

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("GEMINI_API_KEY environment variable is not set.")
    st.stop()

# Gemini-compatible model setup
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

# Streamlit App Title
st.set_page_config(page_title="Crypto Agent", page_icon="💸")
st.title("💸 Crypto Price Agent")
st.markdown("""
Get **real-time cryptocurrency prices** powered by **Binance API** and a Gemini-based AI assistant.

---
""")

# Tool: Show top 10 crypto prices
def show_top_prices_raw() -> str:
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        top_10 = data[:10]
        result = "📊 *Top 10 Cryptocurrency Prices*:\n\n"
        for coin in top_10:
            result += f"- {coin['symbol']}: *${coin['price']}*\n"
        return result
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {str(e)}"

# Tool: Show specific coin price
def show_specific_coin_price_raw(symbol: str) -> str:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"🔎 Current price of {symbol.upper()} is *${data['price']}*"
        else:
            return f"❌ {symbol.upper()} not found. Try a correct trading pair like BTCUSDT."
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {str(e)}"

# Decorated tool functions (not used directly in UI)
@function_tool
def show_top_prices(dummy: str = "") -> str:
    return show_top_prices_raw()

@function_tool
def show_specific_coin_price(symbol: str) -> str:
    return show_specific_coin_price_raw(symbol)

# Define agent
crypto_agent = Agent(
    name="💸 Crypto Agent",
    instructions="""
You are a smart crypto expert. Help users:
- View top 10 coin prices
- Get prices of coins like BTCUSDT or ETHUSDT
Respond simply and clearly. Use tools when needed.
""",
    tools=[show_top_prices, show_specific_coin_price]
)

# Main UI
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Show Top 10 Coins"):
        st.markdown(show_top_prices_raw())

with col2:
    coin = st.text_input("🔎 Enter trading pair (e.g. BTCUSDT, ETHUSDT)")
    if st.button("Get Price") and coin:
        st.markdown(show_specific_coin_price_raw(coin))

# Footer
st.markdown("---")
st.markdown("Created by **Sikandar Tahir** | Powered by Binance API and Gemini")