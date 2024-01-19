import os
from typing import Any, List
import paho.mqtt.client as mqtt
import json

class MQTT_handler():
    def __init__(self, pass_file='passes\\network.pw') -> None:
        # get absolute path
        self.current_path = os.path.dirname(__file__)
        self.pass_file = pass_file
        self.mqtt_host = self._get_mqtt_host()

        self.topics = []
        # First only implement mqtt
    
    def _get_mqtt_host(self):
        """
        Reads the mqtt host from a file and returns its ip address
        """
        try:
            with open(os.path.join(self.current_path, self.pass_file), 'r') as file:
                mqtt_host = json.load(file)['mqtt_host']
        except Exception as e:
            print(f"An error occurred reading mqtt host from json file: {e}")
        
        return mqtt_host

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to mqtt broker with result code {rc}")
        for topic in self.topics:
            self.client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        print(f"{msg.topic} {str(msg.payload)}")

    def connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.client.connect(self.mqtt_host, 1883, 60)

    def subscribe(self, topic):
        self.topics.append(topic)
        self.client.subscribe(topic)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()