"""
IoT-Data-Processing-System - Módulo de Manipulação MQTT
"""

import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker_address: str = "localhost", port: int = 1883, client_id: str = "IoTProcessor"):
        self.broker_address = broker_address
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT com sucesso!")
        else:
            print(f"Falha ao conectar, código de retorno: {rc}")

    def _on_message(self, client, userdata, msg):
        print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

    def connect(self):
        try:
            self.client.connect(self.broker_address, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Erro ao conectar ao broker MQTT: {e}")

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload)

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Desconectado do broker MQTT.")

