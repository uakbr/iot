import time
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')
DEVICE_ID = os.getenv('DEVICE_ID', 'raspberrypi-001')
SEND_INTERVAL = int(os.getenv('SEND_INTERVAL', '5'))  # seconds

def read_sensors():
    # TODO: Implement actual sensor reading using GPIO
    temperature = 25.0  # Placeholder value
    humidity = 50.0     # Placeholder value
    return temperature, humidity

def send_data(data):
    try:
        response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data)
        response.raise_for_status()
        print(f"Data sent successfully: {data}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

def main():
    while True:
        temperature, humidity = read_sensors()
        data = {
            'device_id': DEVICE_ID,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'temperature': temperature,
            'humidity': humidity
        }
        send_data(data)
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    main()