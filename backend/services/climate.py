import requests
from datetime import datetime, timedelta

def get_elevation(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if "elevation" in data and len(data["elevation"]) > 0:
            return data["elevation"][0]
    except Exception as e:
        print(f"Error fetching elevation: {e}")
    return None

def get_historical_climate(lat: float, lon: float):
    end_date = datetime.now() - timedelta(days=365)
    start_date = end_date - timedelta(days=365)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_str}&end_date={end_str}&daily=temperature_2m_max,precipitation_sum&timezone=auto"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if "daily" in data:
            max_temps = data["daily"].get("temperature_2m_max", [])
            precips = data["daily"].get("precipitation_sum", [])
            
            max_temps = [t for t in max_temps if t is not None]
            precips = [p for p in precips if p is not None]

            if not max_temps or not precips:
                return None
            avg_rainfall = sum(precips)
            max_t = max(max_temps)
            
            return {
                "avg_yearly_rainfall": round(avg_rainfall, 2),
                "max_temp": round(max_t, 2)
            }
    except Exception as e:
        print(f"Error fetching climate: {e}")
    
    return None
