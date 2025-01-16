import pandas as pd
from datetime import datetime, timedelta  
from helpers import search_weather_data_with_progress

def mock_progress_callback(progress, status):
    pass

def test_search_weather_data_with_progress():
    # Parameters for the test
    avg_temp_range = (-2, 2)       
    min_temp_range = (-10, -5)     
    max_temp_range = (0, 5)        
    date = datetime.now() - timedelta(days=1)
    exact_time = "Any"               
    snow = "Any"                     
    wind_speed_range = (0, 30)       
    continent = "North America"      
    country_filter = "CA"            

    # Run the function
    results, _ = search_weather_data_with_progress(
        avg_temp_range, min_temp_range, max_temp_range, date, exact_time,
        snow, wind_speed_range, continent, country_filter, mock_progress_callback
    )

    # Assertions
    assert not results.empty, "Expected results, but got an empty DataFrame."
    assert all(-2 <= temp <= 2 for temp in results["Temperature (°C)"]), "Temperature range mismatch."

    # Logs
    # Log the length of data
    num_rows = len(results)
    print(f"Number of rows in results: {num_rows}")
    nan_percentage = results.isna().mean() * 100
    print("Percentage of NaN values per column:")
    print(nan_percentage)
    overall_nan_percentage = results.isna().mean().mean() * 100
    print(f"Overall NaN percentage in the dataset: {overall_nan_percentage:.2f}%")