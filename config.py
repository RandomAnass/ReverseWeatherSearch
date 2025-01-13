import pandas as pd
APP_TITLE = "🌦️ Reverse Weather Search"
APP_DESCRIPTION = "Search for specific weather conditions across the globe with real data. Weather OSINT"

def replace_nan_with_emoji(value, emoji="❓"):
    return value if pd.notna(value) else emoji
