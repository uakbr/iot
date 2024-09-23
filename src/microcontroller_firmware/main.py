import time
import logging
from data_sampler import DataSampler  # Updated import
from calibration import calibrate_sensor
import json
import requests
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables or configuration if needed
API_ENDPOINT = os.getenv('API_ENDPOINT', 'http://localhost:5000')
DEVICE_ID = os.getenv('DEVICE_ID', 'device-001')
SEND_INTERVAL = int(os.getenv('SEND_INTERVAL', '5'))  # seconds

def send_data(data):
    """
    Send sampled data to the API endpoint.

    Parameters:
        data (dict): The sensor data to send.
    """
    try:
        response = requests.post(f"{API_ENDPOINT}/sensor-data", json=data)
        response.raise_for_status()
        logger.info(f"Data sent successfully: {data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send data: {e}")
        # Implement exponential backoff for retries
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

def main():
    """
    Main function to initialize sensors, calibrate them, and start data sampling.
    """
    try:
        # Initialize hardware interfaces
        i2c = I2CInterface(bus_number=1)
        spi = SPIInterface(bus=0, device=0)
        uart = UARTInterface(port='/dev/ttyUSB0', baudrate=115200)

        # Initialize sensors
        temperature_sensor = TemperatureSensor(i2c_address=0x48, i2c=i2c)
        humidity_sensor = HumiditySensor(i2c_address=0x40, i2c=i2c)

        # Calibrate sensors
        temperature_sensor = calibrate_sensor(temperature_sensor, offset=0.5, scale=1.02)
        humidity_sensor = calibrate_sensor(humidity_sensor, offset=-1.0, scale=0.98)

        # Initialize data sampler
        sampler = DataSampler(interval=SEND_INTERVAL)
        sampler.add_sensor(temperature_sensor)
        sampler.add_sensor(humidity_sensor)

        logger.info("Starting data sampling...")
        while True:
            data = sampler.sample()
            # Add device-specific information
            data['device_id'] = DEVICE_ID
            data['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            send_data(data)
            time.sleep(sampler.interval)
    except KeyboardInterrupt:
        logger.info("Data sampling stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()