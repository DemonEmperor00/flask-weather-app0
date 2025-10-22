from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def map_svg_icon(description, icon_code):
    desc = description.lower()
    is_night = icon_code.endswith('n')
    variant = "night" if is_night else "day"

    if "clear" in desc:
        return f"clear-{variant}.svg", f"clear-{variant}"
    elif "overcast" in desc:
        return f"overcast-{variant}.svg", f"overcast-{variant}"
    elif "cloud" in desc:
        return f"cloudy-{variant}.svg", f"cloudy-{variant}"
    elif "drizzle" in desc:
        return f"drizzle-{variant}.svg", f"drizzle-{variant}"
    elif "heavy intensity rain" in desc:
        return f"extreme-{variant}-rain.svg", f"extreme-{variant}-rain"
    elif "rain" in desc:
        return f"rain-{variant}.svg", f"rain-{variant}"
    elif "snow" in desc:
        return f"snow-{variant}.svg", f"snow-{variant}"
    elif "thunder" in desc:
        return f"thunderstorms-{variant}.svg", f"thunderstorms-{variant}"
    elif "fog" in desc:
        return f"fog-{variant}.svg", f"fog-{variant}"
    elif "haze" in desc:
        return f"haze-{variant}.svg", f"haze-{variant}"
    elif "mist" in desc:
        return f"mist-{variant}.svg", f"mist-{variant}"
    elif "wind" in desc:
        return f"wind-{variant}.svg", f"wind-{variant}"
    else:
        return f"cloudy-{variant}.svg", f"cloudy-{variant}"

def get_weather(city):
    GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    try:
        geo_params = {"q": city, "limit": 1, "appid": API_KEY}
        geo_response = requests.get(GEO_URL, params=geo_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return {"error": "City not found"}

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        forecast_params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
        forecast_response = requests.get(FORECAST_URL, params=forecast_params, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        current = forecast_data["list"][0]
        description = current["weather"][0]["description"].capitalize()
        icon_code = current["weather"][0]["icon"]
        temperature_celsius = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        svg_icon, background_class = map_svg_icon(description, icon_code)

        hourly_forecast = []
        for entry in forecast_data["list"][:8]:  # Next 24 hours (3-hour intervals)
            time = entry["dt_txt"][11:16]  # Extract HH:MM
            temp = entry["main"]["temp"]
            hourly_forecast.append({
                              "time": time,
                              "temp": temp,
                              "icon": entry["weather"][0]["icon"] + ".svg"  # or map to your custom SVG
                            })

        return {
            "city": geo_data[0]["name"],
            "temperature_celsius": temperature_celsius,
            "humidity": humidity,
            "description": description,
            "icon_code": icon_code,
            "svg_icon": svg_icon,
            "background_class": background_class,
            "hourly_forecast": hourly_forecast
        }

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