import network
import time
import ujson as json
import urequests as requests
from machine import Pin, ADC
import dht

# Configuration
WIFI_SSID = 'your_wifi_ssid'
WIFI_PASSWORD = 'your_wifi_password'
API_ENDPOINT = 'https://your-api-endpoint.amazonaws.com/dev'
API_KEY = 'your_api_key'
DEVICE_ID = 'device-esp32-001'
SEND_INTERVAL = 5  # seconds

# Initialize Sensors
dht_sensor = dht.DHT22(Pin(4))
mq135_sensor = ADC(Pin(36))
mq135_sensor.atten(ADC.ATTN_11DB)  # Configure ADC range (0-3.6V)

# Connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network configuration:', wlan.ifconfig())

# Send data to API
def send_data(data):
    headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
    try:
        response = requests.post(API_ENDPOINT + '/sensor-data', data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print('Data sent:', data)
        else:
            print('Failed to send data:', response.text)
    except Exception as e:
        print('Error sending data:', e)

# Main loop
def main():
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    while True:
        try:
            # Read DHT22 sensor
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()

            # Read MQ135 sensor
            air_quality_value = mq135_sensor.read()

            # Prepare data payload
            data = {
                'device_id': DEVICE_ID,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'temperature': temperature,
                'humidity': humidity,
                'air_quality_index': air_quality_value,
            }

            send_data(data)
        except Exception as e:
            print('Error reading sensors:', e)

        time.sleep(SEND_INTERVAL)

if __name__ == '__main__':
    main()