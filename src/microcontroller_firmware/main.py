import time
import logging
import json
import os
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables or configuration if needed
IOT_ENDPOINT = os.getenv('IOT_ENDPOINT')
CLIENT_ID = os.getenv('CLIENT_ID', 'device-001')
PATH_TO_CERT = os.getenv('PATH_TO_CERT', 'certs/device.pem.crt')
PATH_TO_KEY = os.getenv('PATH_TO_KEY', 'certs/private.pem.key')
PATH_TO_ROOT = os.getenv('PATH_TO_ROOT', 'certs/AmazonRootCA1.pem')
TOPIC = os.getenv('TOPIC', 'sensor/data')
DEVICE_ID = os.getenv('DEVICE_ID', 'device-001')
SEND_INTERVAL = int(os.getenv('SEND_INTERVAL', '5'))  # seconds

def send_data_mqtt(data):
    """
    Send data to AWS IoT Core via MQTT.

    Parameters:
        data (dict): The sensor data to send.
    """
    mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
    mqtt_client.configureEndpoint(IOT_ENDPOINT, 8883)
    mqtt_client.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
    mqtt_client.connect()
    mqtt_client.publish(TOPIC, json.dumps(data), 1)
    mqtt_client.disconnect()
    logger.info(f"Data sent to AWS IoT Core: {data}")

def main():
    # Initialize data sampler (assuming it's defined elsewhere)
    sampler = DataSampler()
    
    logger.info("Starting data sampling...")
    while True:
        data = sampler.sample()
        # Add device-specific information
        data['device_id'] = DEVICE_ID
        data['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        send_data_mqtt(data)
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    main()