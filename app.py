from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os
app = Flask(__name__)

load_dotenv()
API_KEY = os.environ.get('WEATHER_API_KEY')

def map_svg_icon(description, icon_code):
    desc = description.lower()
    is_night = icon_code.endswith('n')
    variant = "night" if is_night else "day"
    
    if "clear" in desc:
        return "clear-" + variant + ".svg", f"clear-{variant}"
    elif "overcast cloud" in desc:
        return "overcast-" + variant + ".svg", f"overcast-{variant}"
    elif "cloud" in desc:
        return "cloudy-" + variant + ".svg", f"cloudy-{variant}"
    elif "drizzle" in desc:
        return "drizzle-" + variant + ".svg", f"drizzle-{variant}"
    elif "heavy intensity rain" in desc:
        return "extreme-" + variant + "-rain.svg", f"extreme-{variant}-rain"
    elif "rain" in desc:
        return "rain-" + variant + ".svg", f"rain-{variant}"
    elif "snow" in desc:
        return "snow-" + variant + ".svg", f"snow-{variant}"
    elif "thunder" in desc:
        return "thunderstorms-" + variant + ".svg", f"thunderstorms-{variant}"
    elif "fog" in desc:
        return "fog-" + variant + ".svg", f"fog-{variant}"
    elif "haze" in desc:
        return "haze-" + variant + ".svg", f"haze-{variant}"
    elif "mist" in desc:
        return "mist-" + variant + ".svg", f"mist-{variant}"
    elif "wind" in desc:
        return "wind-" + variant + ".svg", f"wind-{variant}"
    else:
        return "cloudy-" + variant + ".svg", f"cloudy-{variant}"

def get_weather(city):
    BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    params = {"q": city, "appid": API_KEY}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        cod = str(data.get("cod", ""))
        if cod != "404":
            main = data.get("main", {})
            weather = data.get("weather", [{}])[0]
            temperature_kelvin = main.get("temp")
            temperature_celsius = round(temperature_kelvin - 273.15, 2) if temperature_kelvin else None
            humidity = main.get("humidity")
            description = weather.get("description", "").capitalize()
            icon_code = weather.get("icon", "")
            svg_icon, background_class = map_svg_icon(description, icon_code)

            return {
                "city": data.get("name"),
                "temperature_celsius": temperature_celsius,
                "humidity": humidity,
                "description": description,
                "icon_code": icon_code,
                "svg_icon": svg_icon,
                "background_class": background_class
            }
        else:
            return {"error": "City not found"}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"error": "Network error occurred"}
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if not city:
            return render_template('index.html', error="Please enter a city name")
        weather_data = get_weather(city)
        return render_template('results.html', weather=weather_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)