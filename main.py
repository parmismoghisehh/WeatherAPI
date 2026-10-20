import os
from urllib.parse import quote

import requests  # pyright: ignore[reportMissingModuleSource]
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY") or os.getenv("VISUAL_CROSSING_API_KEY")
# API that returns a hardcoded weather response.
# Steps:
# 1) checking cache
# 2) cache response
# 3) request WeatherAPI
# 4) weatherAPI response
# 5) save cached response
cache = {}


@app.get("/weather")
def get_weather(city: str = Query(..., min_length=1)):
    city = city.strip().lower()
    if not city:
        raise HTTPException(status_code=400, detail="Enter a city")
    if city in cache:
        return cache[city]
    if not api_key:
        raise HTTPException(status_code=500, detail="Weather API key is missing")

    url = (
        "https://weather.visualcrossing.com/"
        "VisualCrossingWebServices/rest/services/timeline/"
        f"{quote(city, safe='')}"
    )
    try:
        response = requests.get(
            url,
            params={
                "key": api_key,
                "unitGroup": "metric",
                "include": "current",
                "contentType": "json",
            },
            timeout=10,
        )
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Could not connect to service")

    if response.status_code == 400:
        raise HTTPException(status_code=400, detail="Check the city name")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Could not find weather service")

    data = response.json()
    current_data = data["currentConditions"]
    weather = {
        "city": data.get("resolvedAddress", city),
        "temperature": current_data["temp"],
        "condition": current_data["conditions"],
    }
    cache[city] = weather

    return weather

   


    


    


