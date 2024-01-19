from time import sleep
import threading
from typing import Any, List
import sqlite3

from modules.mqtt_handler import MQTT_handler as MQTT_handler
from modules.cmd_handler import Command_Handler as Command_Handler
#from modules.sensor_container import SensorContainer as SensorContainer


if __name__ == '__main__':

    mqtt_handler = MQTT_handler()
    mqtt_handler.connect()
    mqtt_handler.subscribe('esp32/frq')
    mqtt_handler.subscribe('sensor/#')
    mqtt_handler.publish('esp32/frq', 'Hello World')

    mqtt_thread = threading.Thread(target=mqtt_handler.loop_start)
    mqtt_thread.start()

    command_handler = Command_Handler(mqtt_handler)
    
    # sc = SensorContainer()

    # print(sc.get_sensor(0))
    # print(sc.get_sensors())
    # print(sc.get_number_of_sensors())
    # sc.set_sensor(1, "ground_humidity", 2, 352343, 4)
    # print(sc.get_sensor(1))


    # The main thread can continue doing other things
    while True:
        command_handler.invoke_humidity_measurment('1')
        sleep(10)

    # If you want to wait for the MQTT thread to finish before exiting the main thread
    mqtt_thread.join()

