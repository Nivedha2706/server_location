import streamlit as st
import pandas as pd
import socket
import requests
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Server Location Visualizer",
    page_icon="🌍",
    layout="wide"
)

# ---------------- Session State ----------------
if "df" not in st.session_state:
    st.session_state.df = None

# ---------------- Sidebar ----------------
st.sidebar.title("🌍 Server Location Visualizer")

mode = st.sidebar.radio(
    "Input Mode",
    [
        "Single Website",
        "Multiple Websites",
        "Upload File"
    ]
)

st.sidebar.info(
    "Python + Networking + Data Visualization"
)

# ---------------- Inputs ----------------
websites = []

if mode == "Single Website":

    website = st.text_input(
        "Enter Website",
        "google.com"
    )

    if website:
        websites.append(website.strip())

elif mode == "Multiple Websites":

    text = st.text_area(
        "Enter websites (one per line)",
        "google.com\nyoutube.com\ngithub.com"
    )

    websites = [
        w.strip()
        for w in text.splitlines()
        if w.strip()
    ]

else:

    uploaded_file = st.file_uploader(
        "Upload txt file",
        type=["txt"]
    )

    if uploaded_file:
        websites = (
            uploaded_file
            .read()
            .decode()
            .splitlines()
        )
        # ---------------- Button ----------------
if st.button("Find Server Locations"):

    data = []

    with st.spinner("Fetching data..."):

        for website in websites:

            try:
                ip_address = socket.gethostbyname(website)

                response = requests.get(
                    f"http://ip-api.com/json/{ip_address}",
                    timeout=5
                )

                location = response.json()

                if location["status"] == "success":

                    data.append({
                        "Website": website,
                        "IP Address": ip_address,
                        "Country": location["country"],
                        "City": location["city"],
                        "Latitude": location["lat"],
                        "Longitude": location["lon"]
                    })

                else:
                    st.warning(
                        f"Could not process {website}"
                    )

            except Exception as e:
                st.error(
                    f"{website}: {e}"
                )

    if len(data) > 0:

        df = pd.DataFrame(data)

        # Save automatically
        df.to_csv(
            "server_locations.csv",
            index=False
        )

        # Save in session state
        st.session_state.df = df

# ---------------- Display Saved Data ----------------

if st.session_state.df is not None:

    df = st.session_state.df

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Websites",
        len(df)
    )

    col2.metric(
        "Countries",
        df["Country"].nunique()
    )

    col3.metric(
        "Servers",
        len(df)
    )

    st.divider()

    # Table
    st.subheader(
        "Server Information"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # Download CSV
    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False),
        file_name="server_locations.csv",
        mime="text/csv"
    )
   # ---------------- Interactive Map ----------------

if st.session_state.df is not None:

    df = st.session_state.df

    st.subheader("🌍 Interactive World Map")

    color_map = {
        "United States": "blue",
        "India": "green",
        "Singapore": "red",
        "Germany": "orange",
        "United Kingdom": "purple"
    }

    world_map = folium.Map(
        location=[20, 0],
        zoom_start=2
    )

    for _, row in df.iterrows():

        color = color_map.get(
            row["Country"],
            "cadetblue"
        )

        folium.Marker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            popup=f"""
            Website: {row['Website']}
            <br>
            IP: {row['IP Address']}
            <br>
            Country: {row['Country']}
            <br>
            City: {row['City']}
            """,
            tooltip=row["Website"],
            icon=folium.Icon(
                color=color,
                icon="cloud"
            )
        ).add_to(world_map)

    st_folium(
        world_map,
        width=1200,
        height=500
    )