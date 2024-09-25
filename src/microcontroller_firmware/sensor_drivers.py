import logging
from machine import I2C

logger = logging.getLogger(__name__)

class TemperatureSensor:
    """
    Driver for the Temperature Sensor (e.g., TMP102).
    """
    def __init__(self, i2c_address, i2c_bus):
        """
        Initialize the TemperatureSensor.

        Parameters:
            i2c_address (int): I2C address of the temperature sensor.
            i2c_bus (I2C): Instance of I2C bus for communication.
        """
        self.address = i2c_address
        self.i2c = i2c_bus
        logger.info(f"TemperatureSensor initialized at I2C address {self.address}")

    def read_temperature(self):
        """
        Read temperature data from the sensor.

        Returns:
            float: Temperature in Celsius or None if reading fails.
        """
        try:
            raw_data = self.i2c.readfrom_mem(self.address, 0x00, 2)
            if len(raw_data) == 2:
                raw_temp = (raw_data[0] << 8) | raw_data[1]
                temperature = raw_temp * 0.0078125  # Convert to Celsius
                logger.info(f"Temperature Read: {temperature:.2f}°C")
                return temperature
            else:
                logger.error("Invalid raw data received for temperature.")
                return None
        except Exception as e:
            logger.error(f"Error reading temperature: {e}")
            return None

class HumiditySensor:
    """
    Driver for the Humidity Sensor (e.g., HDC1080).
    """
    def __init__(self, i2c_address, i2c_bus):
        """
        Initialize the HumiditySensor.

        Parameters:
            i2c_address (int): I2C address of the humidity sensor.
            i2c_bus (I2C): Instance of I2C bus for communication.
        """
        self.address = i2c_address
        self.i2c = i2c_bus
        logger.info(f"HumiditySensor initialized at I2C address {self.address}")

    def read_humidity(self):
        """
        Read humidity data from the sensor.

        Returns:
            float: Humidity percentage or None if reading fails.
        """
        try:
            raw_data = self.i2c.readfrom_mem(self.address, 0x01, 2)
            if len(raw_data) == 2:
                raw_humidity = (raw_data[0] << 8) | raw_data[1]
                humidity = (raw_humidity / 65536.0) * 100.0  # Convert to %
                logger.info(f"Humidity Read: {humidity:.2f}%")
                return humidity
            else:
                logger.error("Invalid raw data received for humidity.")
                return None
        except Exception as e:
            logger.error(f"Error reading humidity: {e}")
            return None

# Add additional sensor classes similar to the above