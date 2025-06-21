:

📘 Crypto Price Fetcher (FastAPI + Gemini Agent)

🎯 Objective:
Google Gemini API ke through ek agent banaya gaya hai.

Agent get_crypto_price(symbol) function use karta hai jo Binance API se real-time crypto price laata hai.

FastAPI endpoint /get-price/ par query bhejne par price return hota hai.

🧪 Example:
Request (POST /get-price/):

{ "query": "What is the price of BTCUSDT?" }

Response:

{ "response": "The current price of BTCUSDT is $63123.45" }


![IMG-20250621-WA0013](https://github.com/user-attachments/assets/4db32bde-5126-4494-97f2-ba86ca554907)
![IMG-20250621-WA0012](https://github.com/user-attachments/assets/c4e27f34-2c75-46ad-826c-14e902efb962)

