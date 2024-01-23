
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import json
import sqlite3
from time import sleep
from typing import Any, List

from modules.cmd_handler import MQTTCommandHandler as MQTTCommandHandler
invoke_humidity_measurment_for_all = False

if __name__ == '__main__':

    mqtt_handler = MQTTCommandHandler()

    # Start the telegram handler as thread
    

    # The main thread can continue doing other things
    while True:
        if invoke_humidity_measurment_for_all:
            invoke_humidity_measurment_for_all = False
            for sensor_id in range(mqtt_handler.get_number_of_sensors()):
                mqtt_handler.invoke_humidity_measurment(sensor_id)
                print(f"Invoked humidity measurment for sensor {sensor_id}")   
                sleep(1)
        # mqtt_handler.publish('sensor/01/status', timestamp())
        # mqtt_handler.publish('sensor/00/data/hum', str(42 + int(30 * random.random())))
        # mqtt_handler.publish('sensor/00/data/temp', str(42 + int(30 * random.random())))
        # mqtt_handler.publish('sensor/01/data/temp', str(40000 + int(60000 * random.random()))) 
        sleep(10)

    # If you want to wait for the MQTT thread to finish before exiting the main thread
    mqtt_thread.join()

