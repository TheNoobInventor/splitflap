import urequests
import ujson

"""
This function gets the country location the ISS is flying over by first obtaining the ISS
longitude and latitude using the Open Notify API.

Reverse geocoding these coordinates returns the country the ISS is currently over. Otherwise if the reverse
geocoding API returns an error response with statuc code 404, the ISS is over a water body. If any other error 
is encountered, that will also be printed out with an accompanying message for the error code. 
"""


def iss_location() -> str:

    # Get current latitude and longitude of ISS
    try:
        response = urequests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        data = response.json()
        iss_lat = float(data["iss_position"]["latitude"])
        iss_long = float(data["iss_position"]["longitude"])
        print("\nISS latitude:", iss_lat, "\n", "   longitude:", iss_long)

    except Exception as e:
        print(f"Error getting ISS position: {e}")
        return "ERROR"

    # Reverse geocode API key and url
    api_key = "add-your-own-API-key"
    reverse_geocode_url = f"https://us1.locationiq.com/v1/reverse?key={api_key}&lat={iss_lat}&lon={iss_long}&format=json"

    # Get current location of ISS
    try:
        response = urequests.get(reverse_geocode_url, timeout=10)
        data_dict = ujson.loads(response.text)
        response.close()

        country = data_dict["address"]["country"]
        print("\nThe International Space Station is currently over", country)
        return country

    except Exception as e:
        if response.status_code == 404:
            print("\nNo location found - ISS is over an ocean")
        else:
            print(f"API Error: {response.status_code}")
        return "ERROR"
