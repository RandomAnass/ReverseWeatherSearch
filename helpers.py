import pandas as pd
from meteostat import Stations, Daily
from config import replace_nan_with_emoji

def search_weather_data_with_progress(
    temperature_range, date, exact_time, snow, wind_speed_range, continent, country_filter, progress_callback
):
    """
    Fetch weather data and process it based on user inputs.

    Args:
        temperature_range (tuple): A tuple containing the minimum and maximum temperature (°C).
        date (datetime): The date for the weather data.
        exact_time (str): The exact hour for the weather data (e.g., "15:00") or "Any".
        snow (str): Snow condition, either "Yes", "No", or "Any".
        wind_speed_range (tuple): A tuple containing the minimum and maximum wind speed (km/h).
        continent (str): Continent filter (e.g., "North America") or "All".
        country_filter (str): Specific country filter (e.g., "US").

    Returns:
        tuple: A tuple containing:
            - DataFrame: Matched weather data with columns such as temperature, precipitation, and wind speed.
            - list: A list of dictionaries for map data, each containing latitude, longitude, and hoverable info.
    """
    start_date = pd.to_datetime(date)
    end_date = start_date + pd.Timedelta(days=1)

    # global
    stations = Stations()
    stations = stations.fetch()
    stations['id'] = stations.index

    # TODO: add other continents approximations; or use countries/continents lists
    if continent == "North America":
        stations = stations[(stations['latitude'] >= 30) & (stations['latitude'] <= 50) &
                            (stations['longitude'] >= -130) & (stations['longitude'] <= -50)]
    # TODO: get unique country codes (US, DE ...)
    if country_filter:
        stations = stations[stations['country'] == country_filter.upper()]

    total_stations = stations.shape[0]
    matched_data = []
    map_data = []
    # TODO: rework this to be faster
    for idx, (_, station) in enumerate(stations.iterrows()):
        #  progress bar (work on long waiting time)
        progress_callback((idx + 1) / total_stations, f"Processing station {idx + 1}/{total_stations}...")

        data = Daily(station['id'], start=start_date, end=end_date)
        data = data.fetch()

        if not data.empty:
            data['time'] = pd.to_datetime(data.index)
            data['hour'] = data['time'].dt.hour

            if exact_time != "Any":
                hour = int(exact_time.split(":")[0])
                data = data[data['hour'] == hour]

            data = data[
                ((data['tmin'] >= temperature_range[0]) & (data['tmax'] <= temperature_range[1]))
                | (data['tavg'] >= temperature_range[0]) & (data['tavg'] <= temperature_range[1])
            ]

            if snow == "Yes":
                data = data[data['snow'] > 0]
            elif snow == "No":
                data = data[data['snow'] == 0]

            if wind_speed_range:
                data = data[(data['wspd'] >= wind_speed_range[0]) & (data['wspd'] <= wind_speed_range[1])]

            for _, record in data.iterrows():
                result = {
                    "City": station['name'],
                    "Country": station['country'],
                    "Station": station['id'],
                    "Temperature (°C)": record['tavg'],
                    "Min Temp (°C)": record['tmin'],
                    "Max Temp (°C)": record['tmax'],
                    "Precipitation (mm)": replace_nan_with_emoji(record['prcp'], "🌧️"),
                    "Snow (cm)": replace_nan_with_emoji(record['snow'], "❄️"),
                    "Wind Direction (°)": replace_nan_with_emoji(record['wdir'], "🧭"),
                    "Wind Speed (km/h)": replace_nan_with_emoji(record['wspd'], "💨"),
                    "Pressure (hPa)": replace_nan_with_emoji(record['pres'], "🧪"),
                    "Date": record['time'],
                    "Hour": record['hour']
                }
                matched_data.append(result)

                map_data.append({
                    "lat": station['latitude'],
                    "lon": station['longitude'],
                    "info": f"{station['name']} ({station['country']})<br>"
                            f"Temp: {record['tavg']} °C, Snow: {result['Snow (cm)']}"
                })

    return pd.DataFrame(matched_data), map_data
