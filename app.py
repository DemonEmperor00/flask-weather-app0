from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "ae9d892d339e5d9da64b19b7a4254bc7"

def map_svg_icon(description):
    desc = description.lower()
    if "clear" in desc:
        return "clear-day.svg"
    elif "cloud" in desc:
        return "cloudy.svg"
    elif "rain" in desc:
        return "rainy-1.svg"
    elif "snow" in desc:
        return "snowy-1.svg"
    elif "thunder" in desc:
        return "thunder.svg"
    elif "mist" in desc or "fog" in desc or "haze" in desc:
        return "mist.svg"
    else:
        return "cloudy.svg"

def get_weather(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
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
            svg_icon = map_svg_icon(description)

            return {
                "city": data.get("name"),
                "temperature_celsius": temperature_celsius,
                "humidity": humidity,
                "description": description,
                "icon_code": icon_code,
                "svg_icon": svg_icon
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