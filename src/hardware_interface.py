import smbus
import spidev
import serial
import logging

logger = logging.getLogger(__name__)

class I2CInterface:
    def __init__(self, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        logger.info(f"I2C bus {bus_number} initialized.")

    def read_data(self, device_address, register, length=1):
        try:
            data = self.bus.read_i2c_block_data(device_address, register, length)
            logger.info(f"I2C Read from {device_address} register {register}: {data}")
            return data
        except Exception as e:
            logger.error(f"I2C Read Error: {e}")
            return None

    def write_data(self, device_address, register, data):
        try:
            self.bus.write_i2c_block_data(device_address, register, data)
            logger.info(f"I2C Write to {device_address} register {register}: {data}")
        except Exception as e:
            logger.error(f"I2C Write Error: {e}")

class SPIInterface:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 50000
        logger.info(f"SPI bus {bus} device {device} initialized.")

    def transfer(self, data):
        try:
            response = self.spi.xfer2(data)
            logger.info(f"SPI Transfer: Sent {data}, Received {response}")
            return response
        except Exception as e:
            logger.error(f"SPI Transfer Error: {e}")
            return None

class UARTInterface:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=1):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        logger.info(f"UART port {port} initialized with baudrate {baudrate}.")

    def read_data(self, size=1):
        try:
            data = self.serial.read(size)
            logger.info(f"UART Read: {data}")
            return data
        except Exception as e:
            logger.error(f"UART Read Error: {e}")
            return None

    def write_data(self, data):
        try:
            self.serial.write(data)
            logger.info(f"UART Write: {data}")
        except Exception as e:
            logger.error(f"UART Write Error: {e}")