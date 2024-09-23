import logging
from sensor_drivers import TemperatureSensor, HumiditySensor

logger = logging.getLogger(__name__)

def calibrate_sensor(sensor, offset=0.0, scale=1.0):
    """
    Calibrate the sensor by applying an offset and scale factor.
    
    Parameters:
        sensor: Instance of a sensor class (e.g., TemperatureSensor, HumiditySensor).
        offset (float): The offset to be added to the raw sensor reading.
        scale (float): The scale factor to multiply with the raw sensor reading.
    
    Returns:
        The calibrated sensor instance or None if calibration fails.
    """
    try:
        if isinstance(sensor, TemperatureSensor):
            original_read = sensor.read_temperature()
        elif isinstance(sensor, HumiditySensor):
            original_read = sensor.read_humidity()
        else:
            logger.error(f"Unsupported sensor type: {type(sensor)}")
            return None

        if original_read is not None:
            calibrated_value = (original_read + offset) * scale
            logger.info(f"Calibrated {sensor.__class__.__name__}: {calibrated_value}")
            # Depending on the sensor implementation, you might need to store the calibration values
            sensor.calibrated_value = calibrated_value
            return sensor
        else:
            logger.error(f"Calibration failed for {sensor.__class__.__name__}")
            return None
    except Exception as e:
        logger.error(f"Error during calibration of {sensor.__class__.__name__}: {e}")
        return None