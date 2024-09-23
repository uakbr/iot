from .hardware_interface import I2CInterface, SPIInterface, UARTInterface
from .sensor_drivers import TemperatureSensor, HumiditySensor
from .data_sampler import DataSampler
from .calibration import calibrate_sensor