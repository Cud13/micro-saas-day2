from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/msaas-day2", methods=["GET", "POST"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }   
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code
    
    data = response.json()

    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


