from typing import Any, List;
import paho.mqtt.client as mqtt
import os;
import commandlist as cmd

class File_Parser():
    @staticmethod
    def parse_file(file_name: str) -> List[Any]:
        current_path = os.path.dirname(__file__)
        lines = []
        try:
            with open(os.path.join(current_path, file_name), 'r') as file:
                for line in file:
                    lines.append(line.strip())  # Remove any leading or trailing whitespace
        except Exception as e:
            print(f"An error occurred: {e}")
        
        parsed_file = {}
        for line in lines:
            if line.startswith('#'):
                continue
            else:
                key, value = line.split(':')
                parsed_file[key] = value
        return parsed_file

class MQTT_handler():

    def __init__(self, pass_file='passes\\network.pw') -> None:
        self.mqtt_host = self._get_mqtt_host(pass_file=pass_file)
        self.topics = []
        # First only implement mqtt
    
    def _get_mqtt_host(self, pass_file):
        network_passes = File_Parser.parse_file(pass_file)
        #TODO: Add error handling
        return network_passes['MQTT_HOST']
        
    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
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
        

class Command_Handler():
    def __init__(self, mqtt_handler: MQTT_handler) -> None:
        self.mqtt_handler = mqtt_handler
        self.commands = []
    
    def invoke_temp_measurment(self, sensor_id):
        self.mqtt_handler.publish(f'sensor/{sensor_id}/cmd', cmd.GET_HUMIDITY_DATA)

    def invoke_set_low_(self, sensor_id):
        self.mqtt_handler.publish(f'sensor/{sensor_id}/cmd', cmd.GET_HUMIDITY_DATA)

    def add_command(self, command):
        self.commands.append(command)

    def remove_command(self, command):
        self.commands.remove(command)

    def handle_command(self, command):
        for cmd in self.commands:
            if cmd == command:
                cmd.execute()



if __name__ == '__main__':
    mqtt_handler = MQTT_handler()
    mqtt_handler.connect()
    mqtt_handler.subscribe('info')
    mqtt_handler.publish('esp32/frq', 'Hello World')



    mqtt_handler.loop_start()
    while True:
        pass