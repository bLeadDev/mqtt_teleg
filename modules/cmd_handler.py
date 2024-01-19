import os
import json
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTT_ERR_SUCCESS, MQTT_ERR_NO_CONN

class MQTTCommandHandler():
    def __init__(self, command_list_filename="commandlist.json", passes_filename="passes\\network.pw") -> None:
        self.current_path = os.path.dirname(__file__)
        self.passes_filename = passes_filename  # File containing the mqtt host
        self.command_list_filename = command_list_filename
        self.commands = self._get_commands()

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        #self.client.message_callback_add("sensor/+/data", self._on_sensor_data)
        self.client.message_callback_add("sensor/+/data/#", self._on_sensor_data)
        self.mqtt_host = self._get_mqtt_host()
        self.client.connect(self.mqtt_host, 1883, 60)

        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()

    def _on_message(self, client, userdata, message):
        print(f"received {message.topic} {str(message.payload)}")


    def _on_sensor_data(self, client, userdata, message):
        
        sensor_id = message.topic.split('/')[1]
        data = message.payload
        print(f"Sensor {sensor_id} data: {data}")

    def _get_mqtt_host(self):
        try:
            with open(os.path.join(self.current_path, self.passes_filename), 'r') as file:
                mqtt_host = json.load(file)['mqtt_host']
        except Exception as e:
            print(f"An error occurred reading mqtt host from json file: {e}")
            return None
        return mqtt_host

    def _get_commands(self):
        try:
            with open(os.path.join(self.current_path, self.command_list_filename), 'r') as file:
                commands = json.load(file)['commands']
        except Exception as e:
            print(f"An error occurred reading command list from json file: {e}")
            return None
        return commands
    
    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to mqtt broker with result code {rc}")
        self.client.subscribe("sensor/#") 
        print("Subscribed to sensor/#")

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def invoke_humidity_measurment(self, sensor_id):
        self.client.publish(f'sensor/{sensor_id}/cmd', self.commands['CMD_GET_HUMIDITY_DATA'])

    def invoke_temperature_measurement(self, sensor_id):
        self.client.publish(f'sensor/{sensor_id}/cmd', self.commands['CMD_GET_TEMPERATURE_DATA'])

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()