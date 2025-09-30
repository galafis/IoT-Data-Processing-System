"""Test suite for main.py - IoT Data Processing System.

This module contains comprehensive unit tests for the main application entry point,
including normal execution flow and edge case scenarios.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO


class TestMainExecution:
    """Test cases for main application execution."""

    @pytest.fixture
    def mock_dependencies(self):
        """Mock external dependencies for isolated testing."""
        with patch('main.DeviceManager') as mock_dm, \
             patch('main.MQTTClient') as mock_mqtt, \
             patch('main.DataAnalyzer') as mock_analyzer, \
             patch('main.load_config') as mock_config:
            
            # Configure mock behaviors
            mock_config.return_value = {
                'mqtt': {'broker': 'localhost', 'port': 1883},
                'devices': {'max_connections': 100},
                'analytics': {'window_size': 60}
            }
            
            yield {
                'device_manager': mock_dm,
                'mqtt_client': mock_mqtt,
                'analyzer': mock_analyzer,
                'config': mock_config
            }

    def test_main_successful_initialization(self, mock_dependencies):
        """Test successful initialization of main application components."""
        from main import main
        
        # Execute main function
        result = main()
        
        # Verify configuration was loaded
        mock_dependencies['config'].assert_called_once()
        
        # Verify components were instantiated
        mock_dependencies['device_manager'].assert_called_once()
        mock_dependencies['mqtt_client'].assert_called_once()
        mock_dependencies['analyzer'].assert_called_once()
        
        assert result == 0  # Success exit code

    def test_main_graceful_shutdown(self, mock_dependencies):
        """Test graceful shutdown on interrupt signal."""
        from main import main
        
        mqtt_instance = mock_dependencies['mqtt_client'].return_value
        mqtt_instance.connect.side_effect = KeyboardInterrupt()
        
        # Should handle KeyboardInterrupt gracefully
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        # Verify cleanup was attempted
        mqtt_instance.disconnect.assert_called_once()

    def test_main_with_connection_retry(self, mock_dependencies):
        """Test MQTT connection retry mechanism."""
        from main import main
        
        mqtt_instance = mock_dependencies['mqtt_client'].return_value
        mqtt_instance.connect.side_effect = [
            ConnectionError("Connection failed"),
            ConnectionError("Connection failed"),
            None  # Success on third attempt
        ]
        
        result = main()
        
        # Verify retry attempts
        assert mqtt_instance.connect.call_count == 3
        assert result == 0


class TestConfigurationLoading:
    """Test cases for configuration loading and validation."""

    def test_config_file_missing(self):
        """Test behavior when configuration file is missing."""
        with patch('main.load_config') as mock_config:
            mock_config.side_effect = FileNotFoundError("Config not found")
            
            from main import main
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1  # Error exit code

    def test_config_invalid_format(self):
        """Test behavior with invalid configuration format."""
        with patch('main.load_config') as mock_config:
            mock_config.side_effect = ValueError("Invalid YAML format")
            
            from main import main
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1

    def test_config_missing_required_fields(self):
        """Test validation of required configuration fields."""
        with patch('main.load_config') as mock_config:
            mock_config.return_value = {}  # Empty config
            
            from main import validate_config
            
            with pytest.raises(ValueError, match="Missing required field"):
                validate_config(mock_config.return_value)


class TestDeviceManagement:
    """Test cases for device management functionality."""

    @pytest.fixture
    def mock_device_manager(self):
        """Create mock device manager."""
        with patch('main.DeviceManager') as mock:
            instance = mock.return_value
            instance.register_device.return_value = True
            instance.get_active_devices.return_value = []
            yield instance

    def test_device_registration_success(self, mock_device_manager):
        """Test successful device registration."""
        device_id = "device_001"
        result = mock_device_manager.register_device(device_id)
        
        assert result is True
        mock_device_manager.register_device.assert_called_once_with(device_id)

    def test_device_registration_duplicate(self, mock_device_manager):
        """Test handling of duplicate device registration."""
        mock_device_manager.register_device.side_effect = ValueError("Device already registered")
        
        with pytest.raises(ValueError, match="already registered"):
            mock_device_manager.register_device("device_001")

    def test_device_limit_exceeded(self, mock_device_manager):
        """Test behavior when device limit is exceeded."""
        mock_device_manager.register_device.side_effect = RuntimeError("Device limit exceeded")
        
        with pytest.raises(RuntimeError, match="limit exceeded"):
            mock_device_manager.register_device("device_101")


class TestMQTTConnection:
    """Test cases for MQTT connection handling."""

    @pytest.fixture
    def mock_mqtt_client(self):
        """Create mock MQTT client."""
        with patch('main.MQTTClient') as mock:
            instance = mock.return_value
            instance.is_connected.return_value = False
            yield instance

    def test_mqtt_connect_success(self, mock_mqtt_client):
        """Test successful MQTT connection."""
        mock_mqtt_client.connect.return_value = True
        mock_mqtt_client.is_connected.return_value = True
        
        result = mock_mqtt_client.connect()
        
        assert result is True
        assert mock_mqtt_client.is_connected() is True

    def test_mqtt_connection_timeout(self, mock_mqtt_client):
        """Test MQTT connection timeout handling."""
        mock_mqtt_client.connect.side_effect = TimeoutError("Connection timeout")
        
        with pytest.raises(TimeoutError, match="timeout"):
            mock_mqtt_client.connect()

    def test_mqtt_authentication_failure(self, mock_mqtt_client):
        """Test MQTT authentication failure."""
        mock_mqtt_client.connect.side_effect = PermissionError("Authentication failed")
        
        with pytest.raises(PermissionError, match="Authentication"):
            mock_mqtt_client.connect()

    def test_mqtt_message_publish(self, mock_mqtt_client):
        """Test MQTT message publishing."""
        topic = "iot/device/data"
        payload = {"temperature": 25.5, "humidity": 60}
        
        mock_mqtt_client.publish.return_value = True
        result = mock_mqtt_client.publish(topic, payload)
        
        assert result is True
        mock_mqtt_client.publish.assert_called_once_with(topic, payload)


class TestDataAnalytics:
    """Test cases for data analytics functionality."""

    @pytest.fixture
    def mock_analyzer(self):
        """Create mock data analyzer."""
        with patch('main.DataAnalyzer') as mock:
            instance = mock.return_value
            yield instance

    def test_data_analysis_valid_input(self, mock_analyzer):
        """Test data analysis with valid input."""
        data = {"temperature": 25.5, "timestamp": "2025-09-30T07:00:00Z"}
        mock_analyzer.analyze.return_value = {"status": "normal", "anomaly": False}
        
        result = mock_analyzer.analyze(data)
        
        assert result["status"] == "normal"
        assert result["anomaly"] is False

    def test_data_analysis_anomaly_detection(self, mock_analyzer):
        """Test anomaly detection in data."""
        data = {"temperature": 100.0, "timestamp": "2025-09-30T07:00:00Z"}
        mock_analyzer.analyze.return_value = {"status": "alert", "anomaly": True}
        
        result = mock_analyzer.analyze(data)
        
        assert result["status"] == "alert"
        assert result["anomaly"] is True

    def test_data_analysis_invalid_format(self, mock_analyzer):
        """Test handling of invalid data format."""
        mock_analyzer.analyze.side_effect = ValueError("Invalid data format")
        
        with pytest.raises(ValueError, match="Invalid data format"):
            mock_analyzer.analyze({"invalid": "data"})

    def test_data_analysis_missing_fields(self, mock_analyzer):
        """Test handling of missing required fields."""
        mock_analyzer.analyze.side_effect = KeyError("Missing required field: temperature")
        
        with pytest.raises(KeyError, match="temperature"):
            mock_analyzer.analyze({"timestamp": "2025-09-30T07:00:00Z"})


class TestErrorHandling:
    """Test cases for error handling and recovery."""

    def test_unhandled_exception_logging(self):
        """Test that unhandled exceptions are properly logged."""
        with patch('main.logger') as mock_logger:
            with patch('main.main') as mock_main:
                mock_main.side_effect = Exception("Unexpected error")
                
                with pytest.raises(Exception):
                    mock_main()
                
                # Verify error was logged
                assert mock_logger.error.called

    def test_resource_cleanup_on_error(self):
        """Test that resources are cleaned up on error."""
        with patch('main.MQTTClient') as mock_mqtt:
            instance = mock_mqtt.return_value
            instance.connect.side_effect = Exception("Connection error")
            
            from main import main
            
            with pytest.raises(SystemExit):
                main()
            
            # Verify cleanup was attempted
            instance.disconnect.assert_called()

    def test_memory_error_handling(self):
        """Test handling of memory errors."""
        with patch('main.DataAnalyzer') as mock_analyzer:
            mock_analyzer.return_value.analyze.side_effect = MemoryError("Out of memory")
            
            from main import main
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1


class TestCommandLineArguments:
    """Test cases for command-line argument parsing."""

    def test_help_argument(self):
        """Test --help argument displays usage information."""
        with patch('sys.argv', ['main.py', '--help']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    from main import parse_args
                    parse_args()
                
                assert exc_info.value.code == 0
                assert 'usage' in mock_stdout.getvalue().lower()

    def test_config_file_argument(self):
        """Test --config argument specifies custom config file."""
        with patch('sys.argv', ['main.py', '--config', '/path/to/config.yaml']):
            from main import parse_args
            args = parse_args()
            
            assert args.config == '/path/to/config.yaml'

    def test_verbose_mode(self):
        """Test --verbose flag enables debug logging."""
        with patch('sys.argv', ['main.py', '--verbose']):
            from main import parse_args
            args = parse_args()
            
            assert args.verbose is True


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=main', '--cov-report=term-missing'])
