import logging

logger = logging.getLogger(__name__)

class TemperatureSensor:
    """
    Driver for the Temperature Sensor.
    """
    def __init__(self, i2c_address, i2c):
        """
        Initialize the TemperatureSensor.

        Parameters:
            i2c_address (int): I2C address of the temperature sensor.
            i2c (I2CInterface): Instance of I2CInterface for communication.
        """
        self.address = i2c_address
        self.i2c = i2c
        logger.info(f"TemperatureSensor initialized at I2C address {self.address}")

    def read_temperature(self):
        """
        Read temperature data from the sensor.

        Returns:
            float: Temperature in Celsius or None if reading fails.
        """
        try:
            raw_data = self.i2c.read_data(self.address, register=0x00, length=2)
            if raw_data and len(raw_data) == 2:
                # Convert raw data to temperature (example conversion)
                temperature = (raw_data[0] << 8 | raw_data[1]) * 0.0625
                logger.info(f"Temperature Read: {temperature}°C")
                return temperature
            else:
                logger.error("Invalid raw data received for temperature.")
                return None
        except Exception as e:
            logger.error(f"Error reading temperature: {e}")
            return None

class HumiditySensor:
    """
    Driver for the Humidity Sensor.
    """
    def __init__(self, i2c_address, i2c):
        """
        Initialize the HumiditySensor.

        Parameters:
            i2c_address (int): I2C address of the humidity sensor.
            i2c (I2CInterface): Instance of I2CInterface for communication.
        """
        self.address = i2c_address
        self.i2c = i2c
        logger.info(f"HumiditySensor initialized at I2C address {self.address}")

    def read_humidity(self):
        """
        Read humidity data from the sensor.

        Returns:
            float: Humidity percentage or None if reading fails.
        """
        try:
            raw_data = self.i2c.read_data(self.address, register=0x00, length=2)
            if raw_data and len(raw_data) == 2:
                # Convert raw data to humidity (example conversion)
                humidity = ((raw_data[0] << 8) | raw_data[1]) * 0.1
                logger.info(f"Humidity Read: {humidity}%")
                return humidity
            else:
                logger.error("Invalid raw data received for humidity.")
                return None
        except Exception as e:
            logger.error(f"Error reading humidity: {e}")
            return None