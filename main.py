"""
IoT-Data-Processing-System - Entry Point
Integrates device management, MQTT handling, and data analytics.
"""

import logging
from src.utils import setup_logging
from src.device import DeviceManager
from src.analytics import DataAnalyzer


def main():
    """Main execution function."""
    # Configure logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting IoT Data Processing System...")

    # Device management demo
    manager = DeviceManager()
    for device_id in ["sensor-temp-01", "sensor-hum-02", "sensor-press-03"]:
        manager.register_device(device_id)

    active = manager.get_active_devices()
    logger.info(f"Active devices: {active}")

    # Data analytics demo
    print("Running IoT Data Processing Analysis...")
    analyzer = DataAnalyzer()
    results = analyzer.analyze()

    print("Classification Report:")
    print(results["classification_report"])

    analyzer.visualize()
    print("Analysis completed successfully!")

    return analyzer


if __name__ == "__main__":
    main()
