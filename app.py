from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
import os
import requests
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def get_crypto_price(symbol: str) -> str:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    response = requests.get(url)
    if response.status_code == 200:
        price = response.json()["price"]
        return f"The current price of {symbol.upper()} is ${price}"
    else:
        return "Invalid symbol or data fetch failed."

crypto_agent = Agent(
    name="CryptoDataAgent",
    instructions="You provide real-time cryptocurrency prices using the Binance API.",
    tools=[get_crypto_price]
)

app = FastAPI()

class CryptoQuery(BaseModel):
    query: str

@app.post("/get-price/")
async def get_price(data: CryptoQuery):
    try:
        result = await Runner.run(
            crypto_agent,
            input=data.query,
            run_config=config
        )
        return {"response": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
