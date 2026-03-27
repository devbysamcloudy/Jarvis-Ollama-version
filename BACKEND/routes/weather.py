from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
import os
from dotenv import load_dotenv

load_dotenv()

weather_bp = Blueprint("weather", __name__)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@weather_bp.route("/", methods=["GET"])
@jwt_required()
def get_weather():
    city = request.args.get("city", "Nairobi")

    if not API_KEY:
        return jsonify({"error": "Weather API key not configured"}), 500

    try:
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }, timeout=5)

        data = response.json()

        if data.get("cod") == 200:
            return jsonify({
                "city":        data["name"],
                "temp":        round(data["main"]["temp"], 1),
                "feels_like":  round(data["main"]["feels_like"], 1),
                "humidity":    data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize(),
                "wind":        data["wind"]["speed"],
                "country":     data["sys"]["country"],
            }), 200
        else:
            return jsonify({"error": f"City '{city}' not found"}), 404

    except requests.exceptions.Timeout:
        return jsonify({"error": "Weather service timed out"}), 503
    except Exception as e:
        return jsonify({"error": f"Weather service error: {str(e)}"}), 500