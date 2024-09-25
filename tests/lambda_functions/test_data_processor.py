import unittest
from lambda_functions import data_processor

class TestDataProcessor(unittest.TestCase):

    def test_valid_payload(self):
        event = {
            'body': '{"device_id": "device-001", "timestamp": "2023-10-15T14:30:00Z", "temperature": 25.5}'
        }
        response = data_processor.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)

    def test_invalid_payload(self):
        event = {
            'body': '{"device_id": "device-001", "temperature": "invalid"}'
        }
        response = data_processor.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_missing_required_fields(self):
        event = {
            'body': '{"timestamp": "2023-10-15T14:30:00Z"}'
        }
        response = data_processor.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_extra_unexpected_fields(self):
        event = {
            'body': '{"device_id": "device-001", "timestamp": "2023-10-15T14:30:00Z", "unexpected_field": 123}'
        }
        response = data_processor.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()