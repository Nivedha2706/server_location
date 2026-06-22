import socket
import requests

# Read websites from file
with open("websites.txt", "r") as file:
    websites = file.read().splitlines()

for website in websites:
    try:
        # Get IP address
        ip_address = socket.gethostbyname(website)

        # Get location information
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        data = response.json()

        print("\n-------------------------")
        print("Website :", website)
        print("IP Address :", ip_address)
        print("Country :", data['country'])
        print("City :", data['city'])
        print("Latitude :", data['lat'])
        print("Longitude :", data['lon'])

    except Exception as e:
        print(f"Error for {website}: {e}")