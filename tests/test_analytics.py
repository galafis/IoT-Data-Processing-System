import unittest
import os
import logging
import pandas as pd
from src.analytics import DataAnalyzer
from src.device import DeviceManager, Device
from src.utils import setup_logging


class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DataAnalyzer()
        self.sample_data = pd.DataFrame({
            'feature1': [1.0, 2.0, 3.0, 4.0, 5.0],
            'feature2': [5.0, 4.0, 3.0, 2.0, 1.0],
            'feature3': [1.0, 1.0, 0.0, 0.0, 1.0],
            'target': [0, 1, 0, 1, 0]
        })
        self.analyzer.load_data(self.sample_data)

    def test_load_data(self):
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(self.analyzer.data.shape, (5, 4))

    def test_load_data_generates_default(self):
        analyzer = DataAnalyzer()
        analyzer.load_data()
        self.assertEqual(analyzer.data.shape, (1000, 4))

    def test_analyze(self):
        results = self.analyzer.analyze()
        self.assertIn('statistics', results)
        self.assertIn('classification_report', results)
        self.assertIsNotNone(self.analyzer.model)

    def test_visualize(self):
        self.analyzer.analyze()
        self.analyzer.visualize(repo_name="test_repo")
        self.assertTrue(os.path.exists("test_repo_analysis.png"))
        os.remove("test_repo_analysis.png")


class TestDeviceManager(unittest.TestCase):

    def setUp(self):
        self.manager = DeviceManager()

    def test_register_device(self):
        self.manager.register_device("sensor-01")
        self.assertIn("sensor-01", self.manager.devices)

    def test_register_duplicate_device(self):
        self.manager.register_device("sensor-01")
        self.manager.register_device("sensor-01")
        self.assertEqual(len(self.manager.devices), 1)

    def test_get_active_devices_empty(self):
        self.manager.register_device("sensor-01")
        self.assertEqual(self.manager.get_active_devices(), [])

    def test_get_active_devices_after_connect(self):
        self.manager.register_device("sensor-01")
        self.manager.devices["sensor-01"].connect()
        self.assertEqual(self.manager.get_active_devices(), ["sensor-01"])


class TestDevice(unittest.TestCase):

    def test_device_default_status(self):
        device = Device("d1")
        self.assertEqual(device.status, "offline")

    def test_device_connect(self):
        device = Device("d1")
        device.connect()
        self.assertEqual(device.status, "online")

    def test_device_disconnect(self):
        device = Device("d1")
        device.connect()
        device.disconnect()
        self.assertEqual(device.status, "offline")


class TestUtils(unittest.TestCase):

    def test_setup_logging(self):
        log_file = "test_app.log"
        setup_logging(log_file=log_file)
        logger = logging.getLogger("test_utils")
        logger.info("test message")
        self.assertTrue(os.path.exists(log_file))
        os.remove(log_file)


if __name__ == '__main__':
    unittest.main()
