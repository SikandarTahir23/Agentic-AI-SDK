from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from openai import AsyncOpenAI  
from dotenv import load_dotenv
import os
import requests

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=gemini_api_key
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

set_tracing_disabled(disabled=True)  # Open AI Tracing == Disable

@function_tool
def get_weather(city:str)->str:
    """
    Get the current weather for a given city.
    """
    result=requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    data=result.json()
    return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."

@function_tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert a given amount from one currency to another.
    """
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}")
    data = response.json()
    rate = data['rates'].get(to_currency.upper())

    if rate:
        converted = amount * rate
        return f"{amount} {from_currency.upper()} is equal to {converted:.2f} {to_currency.upper()}."
    else:
        return f"Currency {to_currency.upper()} is not supported."

agent: Agent = Agent(   
    name="Weather Agent",
    instructions="You are a weather agent. You can provide weather information and forecasts.",
    model=model,
    tools=[get_weather, convert_currency]
)
result = Runner.run_sync(agent, "convert 100 pakistani rupees to euros")
print(result.final_output)