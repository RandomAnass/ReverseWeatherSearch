import folium
from streamlit_folium import folium_static

def render_map(map_data):
    """
    Render an interactive map with weather station data.

    Args:
        map_data (list): A list of dictionaries where each dictionary contains:
            - lat (float): Latitude of the weather station.
            - lon (float): Longitude of the weather station.
            - info (str): Information to display in the popup (e.g., station name, temperature, snow).

    Returns:
        None: The function renders the map directly using Streamlit's folium integration.
    """
    m = folium.Map(location=[map_data[0]['lat'], map_data[0]['lon']], zoom_start=3)
    for point in map_data:
        folium.Marker(
            location=[point['lat'], point['lon']],
            popup=folium.Popup(point['info'], max_width=300),
            icon=folium.Icon(icon="cloud", color="blue")
        ).add_to(m)
    folium_static(m)
