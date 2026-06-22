import socket

with open("websites.txt", "r") as file:
    websites = file.read().splitlines()

website_ip_data = []

for website in websites:
    try:
        ip_addresses = socket.gethostbyname_ex(website)[2]

        for ip in ip_addresses:
            website_ip_data.append({
                "Website": website,
                "IP Address": ip
            })
            print(f"{website} → {ip}")

    except Exception as e:
        print(f"Could not resolve {website}: {e}")