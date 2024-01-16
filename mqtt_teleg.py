from typing import Any, List;
import os;


class MQTT_Telegram_handler:

    def __init__(self, mqtt_host, pw_file='passes\\network.pw') -> None:
        self.pw_file = pw_file
        self.network_passes = self._get_network_passes()
        # First only implement mqtt
        self.mqtt_host = mqtt_host  



    def _read_input(file_name):
        current_path = os.path.dirname(__file__)
        lines = []
        try:
            with open(os.path.join(current_path, file_name), 'r') as file:
                for line in file:
                    lines.append(line.strip())  # Remove any leading or trailing whitespace
        except Exception as e:
            print(f"An error occurred: {e}")
        return lines
    
    def _get_network_passes(self):
        network_passes = {}
        lines = self._read_input(self.pw_file)
        for line in lines:
            if line.startswith('#'):
                continue
            else:
                network, user, pw = line.split(':')
                network_passes[network] = (user, pw)
        return network_passes
        



lines = read_input('input1.txt')