from time import sleep
import threading
from typing import Any, List
import sqlite3
import datetime
import random

from modules.cmd_handler import MQTTCommandHandler as MQTTCommandHandler

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
 

    mqtt_handler = MQTTCommandHandler()


    # The main thread can continue doing other things
    while True:
        mqtt_handler.invoke_humidity_measurment('1')
        mqtt_handler.publish('sensor/01/status', timestamp())
        mqtt_handler.publish('sensor/00/data/hum', str(42 + int(30 * random.random())))
        mqtt_handler.publish('sensor/00/data/temp', str(42 + int(30 * random.random())))
        mqtt_handler.publish('sensor/01/data/temp', str(40000 + int(60000 * random.random()))) 
        sleep(3)

    # If you want to wait for the MQTT thread to finish before exiting the main thread
    mqtt_thread.join()

