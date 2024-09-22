import os
import time
import json
import requests
import random
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')

def simulate_device():
    while True:
        data = {
            "device_id": "device-001",
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "temperature": round(random.uniform(15.0, 40.0), 2),
            "humidity": round(random.uniform(30.0, 90.0), 2)
        }
        try:
            response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data)
            response.raise_for_status()
            print(f"Data sent: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send data: {e}")
        time.sleep(5)

if __name__ == "__main__":
    if not API_ENDPOINT:
        print("API_ENDPOINT is not set in the environment variables.")
    else:
        simulate_device()