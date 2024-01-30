# IoT Edge Connectivity Checker Module

## Description

The IoT Edge Connectivity Checker is an Azure IoT Edge module designed to assess network connectivity for specified IP addresses or URLs. It performs connectivity checks using ping or HTTP requests and logs the results. The module is particularly useful in IoT scenarios for monitoring network health and diagnosing connectivity issues in edge environments.

## Features

- **Connectivity Testing**: Supports both ping and HTTP requests to check network connectivity.
- **Azure Integration**: Seamlessly integrates with Azure IoT Edge and Azure Blob Storage for result storage.
- **Configurable**: Easily configured via environment variables or direct module inputs.

## Installation

This module is intended to be deployed as part of an Azure IoT Edge solution. Ensure you have Azure IoT Edge runtime installed on your target device.

### Deploying the Module

1. Clone this repository to your local machine or development environment.
2. Build the Docker image for the module and push it to your container registry.
3. Update your IoT Edge deployment manifest to include this module, referencing the Docker image.

### Dependencies

Install the required Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables in your IoT Edge module settings:

- `TASKS_JSON`: A JSON string representing the list of addresses and check types (ping or http). Example format:

  ```json
  [
    {"address": "192.168.1.1", "check_type": "ping", "endpoint_id": "Device1"},
    {"address": "http://example.com", "check_type": "http"}
  ]
  ```

- `AZURE_STORAGE_CONNECTION_STRING`: Your Azure Blob Storage account connection string.
- `AZURE_STORAGE_CONTAINER_NAME`: The name of the container in Azure Blob Storage where the CSV results will be saved.
- `SLEEP_TIME`: The amount of time between scanning

## Usage

Once deployed to an Azure IoT Edge device, the module will automatically start performing connectivity checks based on the provided configuration. Results will be logged and optionally sent to Azure Blob Storage if configured.

## Contributions

Contributions to this project are welcome. Please submit issues and pull requests with any enhancements or bug fixes.

## License

[MIT License](LICENSE)
