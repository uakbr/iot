# IoT Sensor Data Collection & Analytics Platform

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [Features](#features)
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
  - [Monitoring Data Processing](#monitoring-data-processing)
  - [Accessing Stored Data](#accessing-stored-data)
  - [Viewing Logs and Alerts](#viewing-logs-and-alerts)
- [Configuration](#configuration)
- [Cleanup](#cleanup)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

The **IoT Sensor Data Collection & Analytics Platform** is a scalable, serverless solution for real-time data collection and analytics from distributed IoT devices. It processes sensor data such as temperature and humidity, triggers alerts based on predefined conditions, and stores data for analysis.

## Architecture Overview

The platform leverages AWS services to create a robust, scalable, and cost-effective solution.

- **IoT Devices**: Devices (simulated or real) send sensor data via REST API.
- **AWS API Gateway**: Serves as the entry point for data ingestion.
- **AWS Kinesis Data Streams**: Handles real-time data streaming.
- **AWS Lambda**: Processes data and applies business logic.
- **AWS DynamoDB**: Stores time-series data for quick retrieval.
- **AWS S3**: Archives older data for long-term storage.
- **AWS EventBridge**: Manages alerts and event-driven actions.
- **AWS CloudWatch**: Monitors logs, metrics, and triggers alerts.

![Architecture Diagram](docs/architecture_diagram.png)

## Features

- **Real-time Data Ingestion**
- **Serverless Data Processing**
- **Time-Series Data Storage**
- **Event-Driven Alerts**
- **Data Archival**
- **Comprehensive Monitoring and Logging**

## Technologies Used

- **Programming Language**: Python 3.7+
- **Infrastructure as Code (IaC)**: AWS CloudFormation
- **Data Format**: JSON
- **AWS Services**: Kinesis, Lambda, DynamoDB, S3, EventBridge, CloudWatch, API Gateway
- **Tools and Libraries**: AWS CLI, Boto3, Requests

## Prerequisites

- **AWS Account**: Required for deploying AWS resources.
- **AWS CLI**: Installed and configured.
- **Python 3.7+**: Ensure Python is installed.
- **Git**: For cloning the repository.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/yourusername/iot-sensor-platform.git
cd iot-sensor-platform
```

### Configure AWS Credentials

Configure your AWS CLI with the necessary permissions.

```bash
aws configure
```

### Install Dependencies

Install the required Python packages.

```bash
pip install -r requirements.txt
```

### Deploy Infrastructure

Use the provided deployment script to set up AWS resources.

```bash
cd scripts
./deploy.sh
```

**Note**: Ensure you have execution permissions for `deploy.sh` (`chmod +x deploy.sh`).

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
└── .env.example
```

- **README.md**: Project documentation.
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
- **.env.example**: Example environment variables file.

## Usage

### Running the Device Simulator

The device simulator sends simulated sensor data to the API Gateway.

1. **Copy the `.env.example` file to `.env`**

   ```bash
   cp .env.example .env
   ```

2. **Update the `.env` file**

   - Set the `API_ENDPOINT` variable to your API Gateway URL.

3. **Run the simulator**

   ```bash
   cd src
   python device_simulator.py
   ```

### Monitoring Data Processing

Check CloudWatch Logs for Lambda functions.

- **AWS Console > CloudWatch > Logs**
  - View logs for `data_processor` and `alert_handler` Lambda functions.

### Accessing Stored Data

View data stored in DynamoDB.

- **AWS Console > DynamoDB > Tables**
  - Select `IoTSensorData` table.
  - Use the **Explore Table** feature.

### Viewing Logs and Alerts

Monitor alerts via EventBridge and CloudWatch.

- **AWS Console > CloudWatch > Alarms**
  - Configure notifications as needed.

## Configuration

Adjust settings in `config/config.json`.

```json
{
    "temperature_threshold": 30,
    "humidity_threshold": 70
}
```

- **temperature_threshold**: Threshold for temperature alerts.
- **humidity_threshold**: Threshold for humidity alerts.

## Cleanup

To delete AWS resources and avoid charges:

```bash
cd scripts
./cleanup.sh
```

**Note**: Ensure you have execution permissions for `cleanup.sh` (`chmod +x cleanup.sh`).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

# Repository File Details

Here is a detailed explanation of each file:

- **README.md**: Comprehensive guide and documentation for the project.
- **LICENSE**: Specifies the open-source license.
- **.gitignore**: Lists files and directories to be ignored by Git.
- **requirements.txt**: Contains Python package dependencies.
- **api/api_definition.yaml**: Defines the API Gateway configuration.
- **config/config.json**: Holds configurable parameters like thresholds.
- **docs/architecture_diagram.png**: Visual representation of the system architecture.
- **infrastructure/template.yaml**: CloudFormation template to deploy AWS resources.
- **infrastructure/parameters.json**: Parameters for the CloudFormation template.
- **scripts/deploy.sh**: Automates the deployment process.
- **scripts/cleanup.sh**: Automates the cleanup process.
- **src/device_simulator.py**: Simulates IoT devices sending data.
- **src/lambda_functions/alert_handler.py**: Handles alerts based on conditions.
- **src/lambda_functions/data_processor.py**: Processes incoming data.
- **src/lambda_functions/utils.py**: Utility functions for Lambda code.
- **.env.example**: Sample environment variables file.

# Additional Improvements

- **Error Handling**: Enhanced error handling in scripts and Lambda functions.
- **Logging**: Improved logging for better traceability.
- **Security**: Instructions for setting up IAM roles and permissions securely.
- **Scalability**: Notes on how to adjust resources for scaling.
- **Performance Testing**: Guidelines for load testing the system.