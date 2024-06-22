
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import json
import sqlite3
from time import sleep
from typing import Any, List
from abc import ABC, abstractmethod
from threading import Thread


from modules.cmd_handler import MQTTCommandHandler as MQTTCommandHandler

# TODO: set database "humidity ground" stuff to moisture
# TODO: check all todos. They are separated
# TODO: Get rid of the global call or whatever it is. Of yet no idea how to invoke the measurment without it. Maybe a flag? maybe throgh database?
#       As of now the mqtt handler gets called somewhat global. Very confusing and bad design. Fix this! (Thank you Copilot)
# TODO: Make a more general callable interface to the database not this kind of container thingy. 
# Überfalle
# 


SENSOR_DATABASE_NAME = "projectX.db"
SENSOR_TABLE_NAME = "sensors"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TGApplication:
    def __init__(self) -> None:
        pass

    def run(self):
        try:
            telegram_token = json.load(open("modules\\passes\\network.pw"))['telegram_token']
        except Exception as e:
            print(f"An error occurred reading telegram token from json file: {e}")
            exit(1)
        application = ApplicationBuilder().token(telegram_token).build()
        
        start_handler = CommandHandler('start', TGApplication.start)
        temp_handler = CommandHandler('temp', TGApplication.temp)
        meas_handler = CommandHandler('meas', TGApplication.meas)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), TGApplication.echo)
        
        application.add_handler(start_handler)
        application.add_handler(temp_handler)
        application.add_handler(meas_handler)
        application.add_handler(echo_handler)

        application.run_polling()


    @abstractmethod
    def get_sensor_count():
        connection = sqlite3.connect(SENSOR_DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("""
    SELECT COUNT(*) FROM sensors;
        """)
        sensor_count = cursor.fetchone()[0]
        connection.close()
        return sensor_count
    
    @abstractmethod
    def get_humidity_sensor_IDs() -> list[str]:
        connection = sqlite3.connect(SENSOR_DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("""
    SELECT COUNT(*) FROM sensors;
        """)
        sensor_count = cursor.fetchone()[0]
        connection.close()
        return sensor_count
    
    @abstractmethod
    def pretty_print_humidity():
        # Get newest database entries for all connected sensors
        connection = sqlite3.connect(SENSOR_DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("""
    SELECT s.id AS sensorID, MAX(m.normedValue) AS normedValue, s.type, s.id, MAX(m.timestamp) AS timestamp
    FROM measurements AS m
    INNER JOIN sensors AS s ON m.sensorId = s.id
    GROUP BY s.id, s.type
    ORDER BY s.id ASC
    LIMIT 10;
        """)
        newest_entries = cursor.fetchall()
        connection.close()
        msg = "Last measurments:\n"
        for entry in newest_entries:
            msg += f"ID: {entry[0]} at {entry[4][:19]} Value: {str(entry[1]).ljust(8)} Type: {entry[2]}\n" # End entry 4 at 19 to cut off the milliseconds
            print(entry)
        return msg

    @abstractmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    @abstractmethod
    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        
    @abstractmethod
    async def temp(update: Update, context: ContextTypes.DEFAULT_TYPE):

        #print(newest_entries)
        msg = TGApplication.pretty_print_humidity()
        print(f"TG temp request handled. Sending:\n{msg}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    async def meas(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Get count of registered sensors
        # TODO: Get rid of the global variable. Of yet no idea how to invoke the measurment without setting a flag

        sensor_count = TGApplication.get_sensor_count()
        for sensor_id in range(sensor_count):
            mqtt_handler.invoke_humidity_measurment(str(sensor_id))
            print(f"Invoked humidity measurment for sensor {sensor_id}")   
            sleep(1)

        msg = f"Registered sensors: {sensor_count}. Sent measurement command to every one."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)



if __name__ == '__main__':
    mqtt_handler = MQTTCommandHandler()

    application = TGApplication()
    application.run()    


    while True:
        print("Main thread is doing other stuff")
        sleep(4)

    #application.start()


            


        
