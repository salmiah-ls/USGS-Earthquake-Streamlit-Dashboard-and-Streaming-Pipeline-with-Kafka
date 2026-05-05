import streamlit as st
import pandas as pd
import requests
import time
import pydeck as pdk

st.set_page_config(page_title="Earthquake Map", layout="wide")

st.title("🌍 Real-Time Earthquake Map")

# 🔄 Auto refresh every 60 seconds
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 60:
    st.session_state.last_refresh = time.time()
    st.rerun()

# 🌐 Fetch USGS data
@st.cache_data(ttl=60)
def load_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    return requests.get(url).json()

data = load_data()

records = []
for f in data["features"]:
    props = f["properties"]
    coords = f["geometry"]["coordinates"]

    records.append({
        "magnitude": props["mag"],
        "place": props["place"],
        "lat": coords[1],
        "lon": coords[0]
    })

df = pd.DataFrame(records).dropna()

# 🗺️ Map
#st.map(df)
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=50000,
    get_fill_color='[255, 0, 0, 160]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=1,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    #map_style="mapbox://styles/mapbox/light-v9",
    tooltip={
        "html": "<b>Location:</b> {place}<br/><b>Magnitude:</b> {magnitude}",
        "style": {"color": "white"}
    }
))

# 📋 Show latest data
st.dataframe(df.head(), hide_index=True)