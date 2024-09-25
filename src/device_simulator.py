import os
import time
import json
import requests
import random
from dotenv import load_dotenv
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ENDPOINT = os.getenv('API_ENDPOINT')
DEVICE_ID = os.getenv('DEVICE_ID', 'device-001')
SEND_INTERVAL = int(os.getenv('SEND_INTERVAL', '5'))  # seconds
API_KEY = os.getenv('API_KEY')  # New environment variable for API Key

def simulate_device():
    while True:
        data = {
            "device_id": DEVICE_ID,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "temperature": round(random.uniform(15.0, 40.0), 2),
            "humidity": round(random.uniform(30.0, 90.0), 2),
            # New simulated data
            "air_quality_index": round(random.uniform(0, 500), 2),
            "light_intensity": round(random.uniform(0, 10000), 2),  # in lumens
            "sound_level": round(random.uniform(30, 130), 2),  # in decibels
            "pressure": round(random.uniform(950, 1050), 2),  # in hPa
            "co2_level": round(random.uniform(400, 5000), 2),  # in ppm
            "uv_index": round(random.uniform(0, 11), 2),
            "wind_speed": round(random.uniform(0, 100), 2),  # in km/h
            "wind_direction": random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            "battery_level": round(random.uniform(0, 100), 2),  # in percentage
            "signal_strength": round(random.uniform(-120, 0), 2),  # in dBm
            "latitude": round(random.uniform(-90.0, 90.0), 6),
            "longitude": round(random.uniform(-180.0, 180.0), 6),
            "orientation": random.choice(['Upright', 'Upside Down', 'Sideways']),
            "motion_detected": random.choice([True, False]),
        }
        headers = {'x-api-key': API_KEY}
        try:
            # Ensure API_ENDPOINT includes the full URL
            response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data, headers=headers)
            response.raise_for_status()
            logger.info(f"Data sent: {data}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send data: {e}")
            # Implement exponential backoff
            for retry in range(1, 4):
                sleep_time = 2 ** retry
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
                try:
                    response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data, headers=headers)
                    response.raise_for_status()
                    logger.info(f"Data sent on retry {retry}: {data}")
                    break
                except requests.exceptions.RequestException as e:
                    logger.error(f"Retry {retry} failed: {e}")
            else:
                logger.error("Failed to send data after retries.")
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    if not API_ENDPOINT:
        logger.error("API_ENDPOINT is not set in the environment variables.")
        exit(1)
    else:
        # Make sure API_ENDPOINT ends with '/sensor-data'
        if not API_ENDPOINT.endswith('/sensor-data'):
            API_ENDPOINT = API_ENDPOINT.rstrip('/') + '/sensor-data'
        simulate_device()