import urequests
import ujson

"""
This function gets the country location the ISS is flying over by first obtaining the ISS
longitude and latitude using the Open Notify API.

Reverse geocoding these coordinates with LocationIQ API returns the country the ISS is currently over, otherwise an error 
is returned with an explanation for the cause.
"""


def iss_location() -> str:

    # Get the current latitude and longitude of ISS
    response = urequests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])

    # Reverse geocode API key and url
    api_key = "add-your-own-API-key"
    reverse_geocode_url = f"https://us1.locationiq.com/v1/reverse?key={api_key}&lat={iss_lat}&lon={iss_long}&format=json"

    try:
        # Get the current location of ISS
        response = urequests.get(reverse_geocode_url)
        response.raise_for_status()
        data_dict = ujson.loads(response.text)
        country = data_dict["address"]["country"]
        print("\nThe International Space Station is currently over", country)
        return country

    except:
        if response.status_code == 400:
            print("Bad Request")
            return "ERROR"
        elif response.status_code == 401:
            print("Unauthorized")
            return "ERROR"
        elif response.status_code == 404:
            print("No location or places were found for the given input")
            return "ERROR"
        elif response.status_code == 429:
            print("Requests exceeded the rate-limits set on your account")
            return "ERROR"
        elif response.status_code == 500:
            print("Internal Server Error")
            return "ERROR"
        else:
            print("An error occured")
            return "ERROR"

