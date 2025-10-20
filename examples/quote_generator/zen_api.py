import httpx
import random

api_url = "https://zenquotes.io/api/quotes"

async def quote_generator():

    async with httpx.AsyncClient() as client:
        
        response = await client.get(api_url)
        data = response.json()
        
        random_quote = random.choice(data)["q"]
        return random_quote
