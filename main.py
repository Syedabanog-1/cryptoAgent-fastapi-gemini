from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import os
import requests

# ✅ Load API key from .env
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file.")

# ✅ Setup external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Setup Gemini/OpenAI model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",  # gemini-2.0-flash does not exist in OpenAI models
    openai_client=external_client
)

# ✅ Setup run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# ✅ Function tool for getting crypto prices
@function_tool
def get_crypto_price(symbol: str) -> str:
    """
    Fetch the current price of a cryptocurrency from Binance.
    Example: BTCUSDT, ETHUSDT
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    response = requests.get(url)

    if response.status_code == 200:
        price = response.json()["price"]
        return f"The current price of {symbol.upper()} is ${price}"
    else:
        return "Invalid symbol or data fetch failed."

# ✅ Create the agent
crypto_agent = Agent(
    name="CryptoDataAgent",
    instructions="You provide real-time cryptocurrency prices using the Binance API.",
    tools=[get_crypto_price]
)

# ✅ Run the agent synchronously
response = Runner.run_sync(
    crypto_agent,
    input="What is the current price of BTCUSDT?",
    run_config=config
)

# ✅ Print the final output
print(response.final_output)