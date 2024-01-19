from time import sleep
import threading
from typing import Any, List
import sqlite3
import datetime

from modules.cmd_handler import MQTTCommandHandler as MQTTCommandHandler
from modules.sensor_container import SensorContainer as SensorContainer
from modules.meas_logger import MeasurementContainer as MeasurementContainer

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':

    mqtt_handler = MQTTCommandHandler()

    mqtt_handler.publish('sensor/01/data/temp', '42.533')
    mqtt_handler.publish('sensor/02/data/temp', '42.533')
    mqtt_handler.publish('sensor/03/cmd', 'get_hum_data')
    mqtt_handler.publish('sensor/03/status', 'critical_error')
    mqtt_handler.publish('sensor/04/data/hum', '42.533')

    mc = MeasurementContainer()
    sc = SensorContainer()

    sc.set_sensor(1, 'temp', 42.533)

    # The main thread can continue doing other things
    while True:
        mqtt_handler.invoke_humidity_measurment('1')
        mqtt_handler.publish('sensor/03/status', timestamp())
        mqtt_handler.publish('sensor/04/data/hum', 'critical_error')
        print(sc.get_sensor(1))
        sleep(3)

    # If you want to wait for the MQTT thread to finish before exiting the main thread
    mqtt_thread.join()

