import socket
import requests
import pandas as pd

# Read websites
with open("websites.txt", "r") as file:
    websites = file.read().splitlines()

data_list = []

for website in websites:
    try:
        ip_address = socket.gethostbyname(website)

        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        data = response.json()

        data_list.append({
            "Website": website,
            "IP Address": ip_address,
            "Country": data["country"],
            "City": data["city"],
            "Latitude": data["lat"],
            "Longitude": data["lon"]
        })

    except Exception as e:
        print(f"Error for {website}: {e}")

# Create DataFrame
df = pd.DataFrame(data_list)

# Save to CSV
df.to_csv("server_locations.csv", index=False)

print("CSV file created successfully!")