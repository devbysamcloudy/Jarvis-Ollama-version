import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if data['cod'] == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"{city}: {temp}°C, {desc}"
        else:
            return f"City '{city}' not found"
    except:
        return "Weather service error"