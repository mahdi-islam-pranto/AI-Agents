import requests

def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=fc2732c6b5257127c0aefbe5cf7ed68a&query={city}'
  
  response = requests.get(url)
  data = response.json()
  if "current" not in data:
    return "Weather data is not avaiable"
  current = data["current"]
  location = data.get("location", {})
  air_quality = current.get("air_quality", {})
  summary = (
        f"Weather in {location.get('name', city)}, {location.get('country', '')}:\n"
        f"- Temperature: {current.get('temperature', 'N/A')}°C\n"
        f"- Weather: {', '.join(current.get('weather_descriptions', []))}\n"
        f"- Wind: {current.get('wind_speed', 'N/A')} km/h from {current.get('wind_dir', 'N/A')}\n"
        f"- Humidity: {current.get('humidity', 'N/A')}%\n"
        f"- Cloud Cover: {current.get('cloudcover', 'N/A')}%\n"
        f"- Feels Like: {current.get('feelslike', 'N/A')}°C\n"
        f"- UV Index: {current.get('uv_index', 'N/A')}\n"
        f"- Visibility: {current.get('visibility', 'N/A')} km\n"
        f"- Air Quality (US EPA Index): {air_quality.get('us-epa-index', 'N/A')}\n"
    )
  return summary

data = get_weather_data('Dhaka')
print(data)