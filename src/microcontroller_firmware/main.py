import time
import logging
import json
import os
from machine import I2C, Pin
from sensor_drivers import TemperatureSensor, HumiditySensor
from umqtt.simple import MQTTClient
import network

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
WIFI_SSID = os.getenv('WIFI_SSID')
WIFI_PASSWORD = os.getenv('WIFI_PASSWORD')

# Initialize Wi-Fi connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        logger.info('Connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    logger.info('Network configuration: %s', wlan.ifconfig())

# Initialize sensors
i2c_bus = I2C(scl=Pin(22), sda=Pin(21))
temp_sensor = TemperatureSensor(0x48, i2c_bus)  # Example I2C address
humidity_sensor = HumiditySensor(0x40, i2c_bus)

def send_data_mqtt(data):
    """
    Send data to AWS IoT Core via MQTT.

    Parameters:
        data (dict): The sensor data to send.
    """
    try:
        mqtt_client = MQTTClient(client_id=CLIENT_ID,
                                 server=IOT_ENDPOINT,
                                 ssl=True,
                                 ssl_params={
                                     'certfile': PATH_TO_CERT,
                                     'keyfile': PATH_TO_KEY,
                                     'ca_certs': PATH_TO_ROOT
                                 })
        mqtt_client.connect()
        mqtt_client.publish(TOPIC, json.dumps(data))
        mqtt_client.disconnect()
        logger.info(f"Data sent to AWS IoT Core: {data}")
    except Exception as e:
        logger.error(f"Failed to send data via MQTT: {e}")

def main():
    connect_wifi()

    while True:
        try:
            temperature = temp_sensor.read_temperature()
            humidity = humidity_sensor.read_humidity()
            data = {
                'device_id': DEVICE_ID,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'temperature': temperature,
                'humidity': humidity,
            }
            send_data_mqtt(data)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    main()