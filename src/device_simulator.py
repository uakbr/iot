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

def simulate_device():
    while True:
        data = {
            "device_id": DEVICE_ID,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "temperature": round(random.uniform(15.0, 40.0), 2),
            "humidity": round(random.uniform(30.0, 90.0), 2)
        }
        try:
            response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data)
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
                    response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data)
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
    else:
        simulate_device()