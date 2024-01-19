import os
import json
from modules.mqtt_handler import MQTT_handler   

class Command_Handler():
    def __init__(self, mqtt_handler: MQTT_handler, command_list_filename="commandlist.json") -> None:
        self.mqtt_handler = mqtt_handler
        self.command_list_filename = command_list_filename
        self.current_path = os.path.dirname(__file__)
        self.commands = self._get_commands()

    def _get_commands(self):
        try:
            with open(os.path.join(self.current_path, self.command_list_filename), 'r') as file:
                commands = json.load(file)['commands']
        except Exception as e:
            print(f"An error occurred reading mqtt host from json file: {e}")
        return commands
    
    def invoke_humidity_measurment(self, sensor_id):
        self.mqtt_handler.publish(f'sensor/{sensor_id}/cmd', self.commands['CMD_GET_HUMIDITY_DATA'])

    def invoke_temperature_measurement(self, sensor_id):
        self.mqtt_handler.publish(f'sensor/{sensor_id}/cmd', self.commands['CMD_GET_TEMPERATURE_DATA'])