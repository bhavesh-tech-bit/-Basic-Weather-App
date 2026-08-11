import requests

API_KEY = "Your API Key"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def get_weather(location):

    if location.isdigit():
        params = {
            "zip": f"{location},in", 
            "appid": API_KEY,
            "units": "metric"
        }
    else:
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric"
        }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 401:
            print("\n❌ Invalid API Key.")
            return

        
        if response.status_code == 404:
            data = response.json()
            print(f"\n❌ {data.get('message', 'City or ZIP code not found.').title()}")
            return


        response.raise_for_status()

 
        data = response.json()

        temperature_c = data["main"]["temp"]
        temperature_f = celsius_to_fahrenheit(temperature_c)
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]

        print("\n========== Weather Report ==========")
        print(f"Location           : {data['name']}")
        print(f"Temperature (°C)   : {temperature_c:.2f} °C")
        print(f"Temperature (°F)   : {temperature_f:.2f} °F")
        print(f"Humidity           : {humidity}%")
        print(f"Weather            : {description}")
        print(f"Wind Speed         : {wind_speed} m/s")
        print("====================================")

    except requests.exceptions.Timeout:
        print("\n❌ Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        print("\n❌ No internet connection.")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request Error: {e}")

    except KeyError as e:
        print(f"\n❌ Unexpected API response. Missing key: {e}")


def main():
    print("========== Weather Application ==========")

    while True:
        location = input("\nEnter City Name or ZIP Code: ").strip()

        # Input validation
        if not location:
            print("❌ Input cannot be empty.")
            continue

        get_weather(location)

        choice = input("\nSearch another location? (y/n): ").strip().lower()

        if choice != "y":
            print("\nThank you for using the Weather Application!")
            break


if __name__ == "__main__":
    main()