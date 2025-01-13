import streamlit as st
import pandas as pd
from helpers import search_weather_data_with_progress
from map_utils import render_map
from config import APP_TITLE, APP_DESCRIPTION
from pathlib import Path

def load_css():
    css_path = Path("templates/styles.css")
    if css_path.is_file():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title=APP_TITLE, page_icon="🌤", layout="wide")
load_css()
st.title(APP_TITLE)
st.write(APP_DESCRIPTION)
st.sidebar.header("🌎 Filters")
continent = st.sidebar.selectbox("Select Continent", ["All", "North America", "Europe", "Asia", "Australia", "Africa"], index=0)
country_filter = st.sidebar.text_input("Filter by Country (e.g., US)") # TODO: work on this filter
show_map = st.sidebar.checkbox("Show Weather Stations on Map", value=False)

st.header("Search for Weather Conditions")
col1, col2, col3 = st.columns(3)

with col1:
    temperature_range = st.slider("🌡 Temperature Range (°C)", -20, 50, (-5, 5), step=1)
with col2:
    date = st.date_input("📅 Date")
with col3:
    exact_time = st.selectbox("⏰ Time (Optional)", ["Any"] + [f"{i}:00" for i in range(0, 24)], index=0)

snow = st.radio("❄️ Snow", ["Any", "Yes", "No"], index=0)
wind_speed_range = st.slider("💨 Wind Speed Range (km/h)", 0, 50, (0, 20), step=1)


if st.button("Search"):
    st.write("🔍 Searching for weather data. This may take some time.")
    progress_bar = st.progress(0)  
    progress_status = st.empty()   # TODO: maybe change this

    def update_progress(progress, status):
        progress_bar.progress(progress)
        progress_status.text(status)

    with st.spinner("Fetching and processing data..."):
        results, map_data = search_weather_data_with_progress(
            temperature_range, date, exact_time, snow, wind_speed_range, continent, country_filter, update_progress
        )
        progress_bar.empty()
        progress_status.empty()
        if not results.empty:
            st.success("✅ Search completed! Displaying results:")
            st.dataframe(results, height=600, width=1200)

            if show_map:
                render_map(map_data)

            st.download_button("📥 Export Results to CSV", results.to_csv(index=False), "results.csv", "text/csv")
        else:
            st.warning("No matching weather data found. Please adjust your search criteria.")

else:
    st.info("Adjust the filters and click 'Search' to find results.")
