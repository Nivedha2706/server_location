import pandas as pd
import folium

# Read the CSV file
df = pd.read_csv("server_locations.csv")

# Create map centered on the world
world_map = folium.Map(location=[20, 0], zoom_start=2)

# Add markers
for index, row in df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"{row['Website']} ({row['Country']})",
        tooltip=row["Website"]
    ).add_to(world_map)

# Save map
world_map.save("server_map.html")

print("Map created successfully!")