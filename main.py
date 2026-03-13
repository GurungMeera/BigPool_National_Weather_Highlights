from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

API_KEY = "cdc38a132c5afd324c6eb6da1e75875b"
BASE_URL = "https://api.weather.gov/alerts/active"

@app.get("/national-weather")
def get_national_weather():

    response = requests.get(BASE_URL)

    if response.status_code != 200:
        return {"error": "Unable to retrieve weather alerts"}

    data = response.json()

    major_events = []

    for event in data["features"]:
        properties = event["properties"]

        alert = {
            "event": properties.get("event"),
            "area": properties.get("areaDesc"),
            "severity": properties.get("severity"),
            "headline": properties.get("headline")
        }

        # Only include major alerts
        if properties.get("severity") in ["Severe", "Extreme"]:
            major_events.append(alert)

    return {
        "total_events": len(major_events),
        "major_weather_events": major_events
    }

