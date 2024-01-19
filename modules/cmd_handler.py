import os
import json
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTT_ERR_SUCCESS, MQTT_ERR_NO_CONN
from modules.meas_logger import MeasurementContainer
from modules.sensor_container import SensorContainer
# from meas_logger import MeasurementContainer
# from sensor_container import SensorContainer    
import datetime

class MQTTCommandHandler(SensorContainer, MeasurementContainer):
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

    def handle_humidity(self, sensor, measurement_raw_value):
        # (ID INT PRIMARY KEY, type TEXT, lowCalibrationPoint INT, highCalibrationPoint INT, isCalibrated INT) is the sensor table/tuple
        sen_id = sensor[0]
        sen_type = sensor[1]
        sen_lowCalibrationPoint = sensor[2]
        sen_highCalibrationPoint = sensor[3]
        sen_isCalibrated = sensor[4]
        print("Handle temperature")
        print(f"Sensor {sen_id} is calibrated: {sen_isCalibrated}") 
        print(f"Sensor {sen_id} lowCalibrationPoint: {sen_lowCalibrationPoint}")    
        print(f"Sensor {sen_id} raw value: {measurement_raw_value}")

        if not sen_isCalibrated:
            measurement_percentage_value = None
        else:
            measurement_percentage_value = self.get_percentage_value(
                raw_value = int(measurement_raw_value), 
                lowCalibrationPoint = sen_lowCalibrationPoint, 
                highCalibrationPoint = sen_highCalibrationPoint
            )

        self.add_measurement(
            measurement_sensor_id=sen_id,
            measurement_type='temperature',
            measurement_raw_value=measurement_raw_value,
            measurement_percentage_value=measurement_percentage_value,
            measurement_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        pass

    def handle_temperature(self, sensor, measurement_raw_value):
        
        pass

    def _on_sensor_data(self, client, userdata, message):
        """
        Callback for when a sensor publishes data to the mqtt broker
        Reads sensors from database. If sensor is not registered in the database, it will be ignored
        Register function will be added later
        Calls the appropriate handler function for the measurement type"""
        print(f"received osd {message.topic} {str(message.payload)}")


        sensor_id = message.topic.split('/')[1]
        try:
            measurement_type = message.topic.split('/')[3]
        except IndexError:
            print(f"Invalid type: {message.topic}")
            return
        measurement_raw_value=message.payload.decode('utf-8')

        # Get the sensor object
        sensor = self.get_sensor(int(sensor_id))
        if sensor == None:
            print(f"Sensor with id {sensor_id} not found in database")
            return

        # Create a dictionary to map measurement types to functions
        # TODO: Make list of measurement types in a json. Read from json and create dictionary
        measurement_handlers = {
            "temp": self.handle_temperature,
            "hum": self.handle_humidity,
        }

        # Get the function for the current measurement type
        handler = measurement_handlers.get(measurement_type)

        # Call the function if it exists
        if handler is not None:
            handler(sensor, measurement_raw_value)
        else:
            print(f"Unknown measurement type: {measurement_type}")
 
        data = message.payload
        print(f"SensorID {sensor_id} type: {measurement_type} data: {data}")

    def get_percentage_value(self, raw_value, lowCalibrationPoint, highCalibrationPoint):
        return (raw_value - lowCalibrationPoint) / (highCalibrationPoint - lowCalibrationPoint)

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