from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_coordinates(address: str):
    geolocator = Nominatim(user_agent="geoguard_app")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        return None
    return None
