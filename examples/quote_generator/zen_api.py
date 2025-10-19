import requests
import random

api_url = "https://zenquotes.io/api/quotes/"
def quote_generator():

    response = requests.get(api_url)
    data = response.json()

    random_quote = random.choice(data)["q"]
    return random_quote
