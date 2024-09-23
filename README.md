# IoT Sensor Data Collection & Analytics Platform

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Supported Devices](#supported-devices)
- [Use Cases](#use-cases)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Configure AWS Credentials](#configure-aws-credentials)
  - [Install Dependencies](#install-dependencies)
  - [Deploy Infrastructure](#deploy-infrastructure)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
  - [Running the Device Simulator](#running-the-device-simulator)
  - [Integrating Real IoT Devices](#integrating-real-iot-devices)
  - [Monitoring Data Processing](#monitoring-data-processing)
  - [Accessing Stored Data](#accessing-stored-data)
  - [Viewing Logs and Alerts](#viewing-logs-and-alerts)
- [Configuration](#configuration)
- [Data Schema](#data-schema)
- [Cleanup](#cleanup)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

The **IoT Sensor Data Collection & Analytics Platform** is a robust, scalable, and serverless solution designed to collect, process, and analyze real-time data from distributed IoT devices. This platform enables seamless integration of various sensors capturing a wide array of environmental and device metrics, such as temperature, humidity, air quality, light intensity, sound levels, GPS location, and more.

By leveraging the power of AWS services, this platform facilitates:

- **Real-time data ingestion and processing**
- **Event-driven alerts based on custom thresholds**
- **Scalable data storage and archiving**
- **Comprehensive monitoring and logging**

This project is ideal for applications in environmental monitoring, industrial IoT, smart cities, agriculture, and any domain that requires real-time insights from sensor data.

## Architecture Overview

The platform employs a microservices architecture using AWS serverless components, which ensures high availability, scalability, and cost-effectiveness.

- **IoT Devices**: Physical sensors or simulated devices that send sensor data via RESTful API calls.
- **AWS API Gateway**: Acts as a secure entry point for device data ingestion.
- **AWS Kinesis Data Streams**: Handles real-time streaming of high-throughput data.
- **AWS Lambda Functions**: Stateless compute services for processing data and executing business logic.
  - **Data Processor Function**: Validates and stores incoming data.
  - **Alert Handler Function**: Evaluates data against thresholds and triggers alerts.
- **AWS DynamoDB**: A NoSQL database for fast and flexible data storage of time-series sensor data.
- **AWS SNS (Simple Notification Service)**: Sends notifications and alerts to subscribed endpoints.
- **AWS S3 (Simple Storage Service)**: Stores configurations and archives data.
- **AWS CloudWatch**: Monitors the system by collecting logs and metrics.
- **AWS CloudFormation**: Automates the deployment and management of resources.

### Architecture Diagram

![Architecture Diagram](docs/architecture_diagram.png)

## Features

- **Comprehensive Data Collection**: Supports a wide range of sensor data, including environmental metrics, device health, and positional information.
- **Real-Time Data Processing**: Uses Kinesis and Lambda functions to process data as it arrives.
- **Event-Driven Alerts**: Configurable alerts via SNS based on custom thresholds.
- **Scalable Storage**: DynamoDB for immediate data access and S3 for long-term storage.
- **Extensible Design**: Easily add new sensors or data types with minimal changes.
- **High Availability**: Built on AWS's resilient infrastructure.
- **Security**: Employs AWS IAM roles and policies to secure resources.
- **Monitoring and Logging**: Detailed logs and metrics available through CloudWatch.
- **Infrastructure as Code**: Uses CloudFormation for repeatable and version-controlled deployments.

## Supported Devices

The platform is designed to work with a wide array of IoT devices, including but not limited to:

- **Environmental Sensors**:
  - Temperature and humidity sensors
  - Air quality monitors (e.g., CO₂, VOCs, particulate matter)
  - Light sensors (photodiodes, phototransistors)
  - Sound level meters
  - Barometric pressure sensors
  - UV index sensors
  - Anemometers (wind speed and direction)
  - Rain gauges
- **Device Health Sensors**:
  - Battery level monitors
  - Signal strength indicators
  - Motion detectors (accelerometers, gyroscopes)
  - GPS modules for location tracking
- **Industrial Sensors**:
  - Vibration sensors
  - Tilt sensors
  - Proximity sensors

**Note**: Devices must be capable of making HTTP requests to send data to the API Gateway. For devices that cannot natively make HTTP requests, consider using an intermediary gateway or edge computing device.

### Data Retrieval from Devices

To ensure seamless data collection from individual devices, the following technical processes are implemented:

#### Hardware Interfaces

- **I2C (Inter-Integrated Circuit)**: Utilized for connecting sensors requiring low-speed communication, such as temperature, humidity, and light sensors.
- **SPI (Serial Peripheral Interface)**: Employed for high-speed data transfer with sensors like barometric pressure and air quality monitors.
- **UART (Universal Asynchronous Receiver/Transmitter)**: Used for serial communication with GPS modules and motion detectors.

#### Microcontroller Programming

- **Firmware Development**: Implemented using C/C++ or MicroPython for microcontrollers like ESP32 or Arduino.
- **Sensor Drivers**: Configure and read data from various sensors using appropriate libraries.
- **Data Sampling**: Scheduled tasks to sample sensor data at regular intervals (e.g., every second).
- **Calibration**: Perform sensor calibration to maintain data accuracy over time.

#### Data Processing

- **Filtering**: Apply filters such as Kalman or moving average to smooth sensor data and eliminate noise.
- **Unit Conversion**: Convert raw sensor data to standardized units (e.g., Celsius for temperature, ppm for CO₂ levels).
- **Data Aggregation**: Aggregate data points if necessary before transmission to reduce payload size.

#### Data Formatting

- **JSON Payloads**: Structure data in JSON format adhering to the defined schema, including mandatory fields like `device_id` and `timestamp`.
- **Timestamping**: Use synchronized UTC timestamps to ensure data consistency across devices.

#### Communication Protocols

- **HTTP/HTTPS**: Devices communicate with the AWS API Gateway using secure RESTful API calls with POST requests.
- **Authentication**: Include API keys or tokens in headers for authenticated access (if enabled).
- **Payload Management**: Optimize JSON payloads to ensure efficient data transmission with minimal latency.

#### Network Connectivity

- **Wi-Fi Modules**: Configure devices with Wi-Fi capabilities to establish connections to local networks.
- **Cellular Modules**: Use cellular connectivity (e.g., LTE) for devices deployed in remote locations without Wi-Fi access.
- **Ethernet Connections**: For industrial applications requiring wired connectivity for reliability.

#### Power Management

- **Battery Monitoring**: Continuously monitor battery levels and report low power status.
- **Sleep Modes**: Implement deep sleep modes in microcontrollers to conserve energy during inactive periods.
- **Energy Harvesting**: Utilize solar panels or other energy harvesting methods to prolong device operational lifespan.

#### Edge Computing (Optional)

- **Data Aggregation Gateways**: Deploy edge devices like Raspberry Pi to aggregate and preprocess data from multiple sensors.
- **Local Storage**: Temporarily store data locally to handle intermittent network connectivity.
- **Protocol Translation**: Convert data from various sensor protocols to unified HTTP requests for cloud transmission.

#### Error Handling and Retries

- **Network Failures**: Implement retry logic with exponential backoff for failed transmissions to handle transient network issues.
- **Data Validation**: Validate data integrity before transmission, using checksums or CRC.
- **Exception Handling**: Ensure microcontrollers can recover from unexpected states or data anomalies by resetting or triggering watchdog timers.

## Use Cases

- **Environmental Monitoring**: Track air quality, noise pollution, and weather conditions in real time.
- **Smart Agriculture**: Monitor soil moisture, temperature, and humidity to optimize irrigation.
- **Asset Tracking**: Use GPS data to track the location of vehicles or equipment.
- **Industrial Automation**: Monitor machinery health by collecting vibration and pressure data.
- **Smart Cities**: Collect data from distributed sensors for traffic management and public safety.
- **Energy Management**: Monitor energy consumption and optimize usage patterns.

## Technologies Used

- **Programming Language**: Python 3.7+
- **Infrastructure as Code (IaC)**: AWS CloudFormation
- **Data Format**: JSON
- **AWS Services**:
  - **Compute**: Lambda
  - **Storage**: S3, DynamoDB
  - **Networking**: API Gateway, VPC (optional)
  - **Streaming**: Kinesis Data Streams
  - **Messaging**: SNS
  - **Monitoring**: CloudWatch
  - **Event Management**: EventBridge
- **Tools and Libraries**:
  - **AWS CLI**: Command-line interface for AWS services
  - **Boto3**: AWS SDK for Python
  - **Requests**: HTTP library for Python
  - **Python Dotenv**: For environment variable management

## Prerequisites

- **AWS Account**: Required for deploying AWS resources.
- **AWS CLI**: Installed and configured with appropriate permissions.
- **Python 3.7+**: Ensure Python is installed.
- **Git**: For cloning the repository.
- **IAM Permissions**: Ability to create IAM roles, Lambda functions, DynamoDB tables, and other AWS resources.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/yourusername/iot-sensor-platform.git
cd iot-sensor-platform
```

### Configure AWS Credentials

Ensure your AWS CLI is configured with credentials that have the necessary permissions.

```bash
aws configure
```

### Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### Deploy Infrastructure

Use the provided deployment script to set up AWS resources via CloudFormation.

```bash
cd scripts
./deploy.sh
```

**Note**: Ensure you have execution permissions for `deploy.sh` (`chmod +x deploy.sh`). The deployment process will:

- Package and upload Lambda functions to S3.
- Deploy CloudFormation stack to create AWS resources.
- Output the API Gateway endpoint URL.

## Directory Structure

```plaintext
iot-sensor-platform/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── api/
│   └── api_definition.yaml
├── config/
│   └── config.json
├── docs/
│   └── architecture_diagram.png
├── infrastructure/
│   ├── template.yaml
│   └── parameters.json
├── scripts/
│   ├── deploy.sh
│   └── cleanup.sh
├── src/
│   ├── device_simulator.py
│   └── lambda_functions/
│       ├── alert_handler.py
│       ├── data_processor.py
│       └── utils.py
├── .env.example
└── tests/
    └── test_functions.py
```

- **README.md**: Project documentation (this file).
- **LICENSE**: Project license (MIT).
- **.gitignore**: Specifies intentionally untracked files.
- **requirements.txt**: Python dependencies.
- **api/**: API Gateway definitions.
- **config/**: Configuration files for thresholds and settings.
- **docs/**: Documentation assets.
- **infrastructure/**: CloudFormation templates and parameters.
- **scripts/**: Deployment and cleanup scripts.
- **src/**: Source code.
  - **device_simulator.py**: Simulates IoT devices.
  - **lambda_functions/**: AWS Lambda function code.
  - **utils.py**: Utility functions and helpers.
- **.env.example**: Example environment variables file.
- **tests/**: Unit and integration tests.

## Usage

### Running the Device Simulator

The device simulator sends simulated sensor data to the API Gateway, mimicking real IoT devices.

1. **Copy the `.env.example` file to `.env`**

   ```bash
   cp .env.example .env
   ```

2. **Update the `.env` file**

   - Set the `API_ENDPOINT` variable to your API Gateway URL obtained from the deployment output.
   - Adjust `DEVICE_ID` and `SEND_INTERVAL` as needed.

3. **Run the simulator**

   ```bash
   cd src
   python device_simulator.py
   ```

### Integrating Real IoT Devices

To connect real devices:

1. **Configure Device Networking**

   - Ensure the device can make HTTPS requests.
   - Configure network settings for internet access.

2. **Set API Endpoint**

   - Program the device to send HTTP POST requests to the API Gateway endpoint `/sensor-data`.

3. **Format Data Payload**

   - Structure the JSON payload according to the updated data schema (see [Data Schema](#data-schema)).

4. **Handle Authentication (Optional)**

   - Implement API keys or other authentication mechanisms if enabled.

### Monitoring Data Processing

Use AWS CloudWatch to monitor the system:

- **Logs**:
  - Access logs for `data_processor` and `alert_handler` Lambda functions.
  - Analyze log streams for errors or performance issues.
- **Metrics**:
  - Monitor invocation counts, durations, and error rates.
  - Set up custom dashboards and alarms.

### Accessing Stored Data

Retrieve sensor data from DynamoDB:

- **AWS Console > DynamoDB > Tables**
  - Select the `IoTSensorPlatform-SensorDataTable`.
  - Use the **Explore Table** feature to query data.

- **Programmatic Access**:
  - Use Boto3 or AWS SDKs to query data in applications.

### Viewing Logs and Alerts

Monitor alerts via SNS and CloudWatch:

- **AWS Console > SNS > Topics**
  - Subscribe to the `SensorAlertTopic` via email, SMS, or other protocols.
- **AWS Console > CloudWatch > Alarms**
  - View and configure alarms based on metrics.

## Configuration

Adjust settings in `config/config.json` stored in S3:

```json
{
    "temperature_threshold": 30,
    "humidity_threshold": 70,
    "aqi_threshold": 100,
    "co2_threshold": 1000,
    "noise_level_threshold": 85,
    "battery_level_threshold": 20
}
```

- **temperature_threshold**: Threshold for temperature alerts.
- **humidity_threshold**: Threshold for humidity alerts.
- **aqi_threshold**: Threshold for Air Quality Index alerts.
- **co2_threshold**: Threshold for CO₂ level alerts.
- **noise_level_threshold**: Threshold for sound level alerts.
- **battery_level_threshold**: Threshold for low battery alerts.

**Updating Configurations**:

- Modify the `config.json` file locally.
- Upload it to the S3 bucket specified by the `CONFIG_BUCKET` environment variable.

## Data Schema

The platform expects data in a specific JSON format. Below is the updated schema reflecting all the data points collected:

`json
{
    "device_id": "string",
    "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
    "temperature": float,
    "humidity": float,
    "air_quality_index": float,
    "light_intensity": float,
    "sound_level": float,
    "pressure": float,
    "co2_level": float,
    "uv_index": float,
    "wind_speed": float,
    "wind_direction": "string",
    "battery_level": float,
    "signal_strength": float,
    "latitude": float,
    "longitude": float,
    "orientation": "string",
    "motion_detected": boolean
}
```

**Key Points**:

- **Mandatory Fields**: `device_id`, `timestamp`, `temperature`, `humidity`.
- **Optional Fields**: All other fields are optional but recommended where applicable.
- **Data Types**: Ensure data types match the schema (e.g., floats for numerical values).

## Cleanup

To delete AWS resources and avoid ongoing charges:

```bash
cd scripts
./cleanup.sh
```

**Note**: Ensure you have execution permissions for `cleanup.sh` (`chmod +x cleanup.sh`). The cleanup script will:

- Delete the CloudFormation stack.
- Remove the S3 buckets used for code and configuration.
- Confirm before deletion to prevent accidental loss.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**

   - Click the "Fork" button at the top right of the repository page.

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Make Changes**

   - Implement your feature or bug fix.
   - Write unit tests in the `tests/` directory.
   - Update documentation as needed.

4. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

5. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

6. **Open a Pull Request**

   - Go to your fork on GitHub.
   - Click the "New Pull Request" button.

## License

This project is licensed under the [MIT License](LICENSE), which permits reuse within proprietary software provided all copies of the licensed software include a copy of the MIT License terms and the copyright notice.

## Acknowledgments

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Serverless Architecture Patterns](https://docs.aws.amazon.com/lambda/latest/dg/lambda-design.html)
- [OpenAPI Specification](https://swagger.io/specification/)

---