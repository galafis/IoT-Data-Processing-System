# Source Code Structure

This directory contains the main source code for the IoT Data Processing System.

## Package Architecture

The system follows a modular architecture pattern commonly used in production IoT applications:

### Core Modules

#### `device.py`
- **Purpose**: Device management and abstraction layer
- **Responsibilities**:
  - Device registration and lifecycle management
  - Device state tracking and validation
  - Hardware abstraction for different IoT device types
  - Device authentication and authorization
- **Key Classes**: `Device`, `DeviceManager`, `DeviceRegistry`

#### `mqtt_handler.py`
- **Purpose**: MQTT protocol communication layer
- **Responsibilities**:
  - MQTT broker connection management
  - Message publishing and subscription handling
  - QoS (Quality of Service) management
  - Connection retry and error handling
  - Message serialization/deserialization
- **Key Classes**: `MQTTClient`, `MQTTMessageHandler`, `MQTTConfig`

#### `analytics.py`
- **Purpose**: Real-time data analytics and processing
- **Responsibilities**:
  - Stream data processing
  - Statistical analysis and aggregation
  - Anomaly detection algorithms
  - Time-series data handling
  - Data quality validation
- **Key Classes**: `DataAnalyzer`, `StreamProcessor`, `AnomalyDetector`

#### `utils.py`
- **Purpose**: Shared utility functions and helpers
- **Responsibilities**:
  - Configuration management
  - Logging utilities
  - Data validation helpers
  - Common data transformations
  - Error handling utilities
- **Key Functions**: `load_config()`, `setup_logging()`, `validate_data()`, `format_timestamp()`

## Design Patterns Applied

- **Factory Pattern**: Used in device instantiation
- **Observer Pattern**: For event-driven MQTT message handling
- **Singleton Pattern**: For configuration and logging management
- **Strategy Pattern**: For different analytics algorithms

## Data Flow

```
IoT Devices → MQTT Handler → Device Manager → Analytics → Storage/Output
```

## Usage Example

```python
from src.device import DeviceManager
from src.mqtt_handler import MQTTClient
from src.analytics import DataAnalyzer
from src.utils import load_config

# Initialize configuration
config = load_config('config.yaml')

# Setup components
device_manager = DeviceManager(config)
mqtt_client = MQTTClient(config)
analyzer = DataAnalyzer(config)

# Connect and process
mqtt_client.connect()
mqtt_client.subscribe_to_devices(device_manager.get_active_devices())
```

## Best Practices

1. **Type Hints**: All modules use Python type hints for better code clarity
2. **Error Handling**: Comprehensive exception handling with custom exceptions
3. **Logging**: Structured logging throughout all modules
4. **Documentation**: Docstrings following Google style guide
5. **Testing**: Each module has corresponding unit tests in `tests/`

## Adding New Modules

When adding new functionality:
1. Create a new module with clear single responsibility
2. Add comprehensive docstrings
3. Include type hints
4. Write corresponding tests
5. Update this README

## Dependencies

See `requirements.txt` for external dependencies. Core modules rely on:
- `paho-mqtt`: MQTT client library
- `pandas`: Data analysis and manipulation
- `numpy`: Numerical computing
- `PyYAML`: Configuration file parsing
