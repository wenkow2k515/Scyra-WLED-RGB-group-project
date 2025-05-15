import requests
import json

wled_ip = input("Enter WLED IP address (e.g. 192.168.1.100): ").strip()

print("Enter your WLED JSON command:")
try:
    user_input = input("> ")
    payload = json.loads(user_input)  # ensures safety (only JSON)
except json.JSONDecodeError as e:
    print("Invalid JSON:", e)
    exit()

# Send the request
url = f"http://{wled_ip}/json/state"

try:
    res = requests.post(url, json=payload, timeout=5)
    if res.status_code == 200:
        print("Command sent successfully!")
        print("WLED response:", res.json())
    else:
        print(f"Error {res.status_code}: {res.text}")
except requests.exceptions.RequestException as e:
    print("Request failed:", e) 