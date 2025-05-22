import os
import requests
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

openai.api_key = OPENAI_API_KEY

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=hr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_weather_response(weather_data, city):
    if not weather_data:
        return "Could not retrieve weather data."

    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    wind = weather_data['wind']['speed']

    prompt = f"Give me a weather report for today in the city {city}, but do not mention the weather just recommend what to wear."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    city = "Pula"
    weather = get_weather(city)
    odgovor = generate_weather_response(weather, city)
    print(odgovor)
