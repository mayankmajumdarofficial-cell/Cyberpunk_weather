from django.shortcuts import render
import requests

def index(request):
    weather_data = None
    error_msg = None

    if request.method == "POST":
        region = request.POST.get("region", "").strip()
        if region:
            # Using Open-Meteo geocoding + weather api (Free, no keys required, highly reliable)
            try:
                # 1. Coordinate lookup
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={region}&count=1&language=en&format=json"
                geo_res = requests.get(geo_url).json()
                
                if geo_res.get("results"):
                    loc = geo_res["results"][0]
                    lat, lon = loc["latitude"], loc["longitude"]
                    name = f"{loc['name']}, {loc.get('country', 'Unknown Sector')}"
                    
                    # 2. Fetch atmospheric data
                    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code"
                    w_res = requests.get(weather_url).json()
                    current = w_res.get("current", {})
                    
                    # Cyberpunk interpretation of standard WMO weather codes
                    code = current.get("weather_code", 0)
                    if code == 0: atmosphere = "CRYSTAL SILICONE SKY / NO PARTICULATES"
                    elif code in [1, 2, 3]: atmosphere = "HAZY RAD-SHIELD COMPROMISE"
                    elif code in [45, 48]: atmosphere = "SULPHUR FOG / OXIDIZING VISIBILITY LOW"
                    elif code in [51, 53, 55, 61, 63, 65]: atmosphere = "CORROSIVE ACID DRIZZLE DETECTED"
                    elif code in [71, 73, 75, 77, 85, 86]: atmosphere = "ASHFALL / CRYOGENIC PRECIPITATION"
                    elif code in [95, 96, 99]: atmosphere = "IONIC STORM / ELECTROMAGNETIC RUPTURE WARNING"
                    else: atmosphere = "UNKNOWN ATMOSPHERIC ANOMALY"

                    weather_data = {
                        "region": name.upper(),
                        "temp": current.get("temperature_2m"),
                        "feels_like": current.get("apparent_temperature"),
                        "humidity": current.get("relative_humidity_2m"),
                        "wind": current.get("wind_speed_10m"),
                        "status": atmosphere
                    }
                else:
                    error_msg = "GEOLOCATION ERROR: Sector coordinates unregistered in Imperial Archives."
            except Exception:
                error_msg = "DECK ERROR: Uplink timed out. Satellite connection severed."
        else:
            error_msg = "INPUT REQUIRED: Insert Sector ID/Region Name."

    return render(request, "weather/index.html", {"weather": weather_data, "error": error_msg})