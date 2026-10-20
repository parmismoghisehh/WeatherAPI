from fastapi import FastAPI, Query


app = FastAPI()
#API that returns a hardcoded weather response. 
#Steps:
#1) checking cache
#2) cache response
#3) request WeatherAPI
#4) weatherAPI repsonse
#5) save cashed response
cache={}
@app.post("/weather")
def post_weather(
    city: str = Query(..., min_length=1),
    temperature: str = Query(...),
    condition: str = Query(..., min_length=1),
):
    weather = {
        "city": city,
        "temperature": temperature,
        "condition": condition,
    }
    cache[city] = weather
    return weather


@app.get("/weather")
def get_weather(city: str):
    if city in cache:
        return cache[city]

    weather = {
        "city": city,
        "temperature": "temperature",
        "condition": "condition",
    }
    cache[city] = weather
    print("Saving new weather")
    return weather

    


    


