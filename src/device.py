"""
IoT-Data-Processing-System - Módulo de Gerenciamento de Dispositivos
"""

class Device:
    def __init__(self, device_id: str, status: str = "offline"):
        self.device_id = device_id
        self.status = status

    def connect(self):
        self.status = "online"
        print(f"Dispositivo {self.device_id} conectado.")

    def disconnect(self):
        self.status = "offline"
        print(f"Dispositivo {self.device_id} desconectado.")

class DeviceManager:
    def __init__(self):
        self.devices = {}

    def register_device(self, device_id: str):
        if device_id not in self.devices:
            self.devices[device_id] = Device(device_id)
            print(f"Dispositivo {device_id} registrado.")
        else:
            print(f"Dispositivo {device_id} já registrado.")

    def get_active_devices(self):
        return [device.device_id for device in self.devices.values() if device.status == "online"]

