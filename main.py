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

def generate_weather_response(weather_data):
    if not weather_data:
        return "Ne mogu dohvatiti podatke o vremenu za taj grad."

    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']

    prompt = f"Daj mi jednostavan opis vremena za grad: Temperatura je {temp}°C, a trenutno je {description}."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    grad = "Pula"
    weather = get_weather(grad)
    odgovor = generate_weather_response(weather)
    print(odgovor)
