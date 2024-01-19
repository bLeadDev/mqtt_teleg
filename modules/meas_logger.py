import sqlite3
import datetime

MEAS_DATABASE_FILE_NAME = "projectX.db"
MEAS_TABLE_NAME = "measurements"

class MeasurementContainer:
    """MeasurementContainer class"""
    __measurement_list = None

    def __select_db(self):
        """Opens database and reads every measurement in the owned datastructure."""
        connection = sqlite3.connect(MEAS_DATABASE_FILE_NAME)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM """ + MEAS_TABLE_NAME)
        self.__measurement_list = cursor.fetchall()
        connection.close()

    def create_table(self):
        """
        Create Database for measurements following this structure:
            UUID as INT PK,
            sensorID as INT FK,
            type as TEXT,
            rawValue as INT,
            normedValue as REAL,
            timestamp as TEXT (YYYY-MM-DD HH:MM:SS.SSS)
        Every value is normed to its own type according to SI units.

        """
        connection = sqlite3.connect(MEAS_DATABASE_FILE_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE " + MEAS_TABLE_NAME + " (id INTEGER PRIMARY KEY AUTOINCREMENT, sensorID INT, type TEXT, rawValue INT, normedValue REAL, timestamp TEXT)"
        )

        self.add_measurement(1, "ground_humidity", 752343, 21.442)
        self.add_measurement(2, "ground_humidity", 152343, 51.442)
        self.add_measurement(0, "air_humidity", 35343, 72.3)
        connection.commit()
        connection.close()

    def get_measurements(self):
        """returns all measurements as list of tuples"""
        if self.__measurement_list == None:
            self.__select_db()
        return self.__measurement_list

    def add_measurement(
        self,
        measurement_sensor_id,
        measurement_type,
        measurement_raw_value,
        measurement_percentage_value,
        measurement_timestamp=None
    ):
        if measurement_timestamp == None:
            measurement_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
        connection = sqlite3.connect(MEAS_DATABASE_FILE_NAME)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO " + MEAS_TABLE_NAME + " (sensorID, type, rawValue, normedValue, timestamp) VALUES (?, ?, ?, ?, ?)",
            (
                measurement_sensor_id,
                measurement_type,
                measurement_raw_value,
                measurement_percentage_value,
                measurement_timestamp
            ),
        )
        cursor.execute("""SELECT * FROM """ + MEAS_TABLE_NAME)
        self.__measurement_list = cursor.fetchall()
        connection.commit()
        connection.close()

    def get_number_of_measurements(self):
        if self.__measurement_list == None:
            self.__select_db()
        return len(self.__measurement_list)


if __name__ == "__main__":

    from time import sleep
    sc = MeasurementContainer()
    # sc.create_table()

    print(sc.get_measurements())
    print(sc.get_number_of_measurements())

    sc.add_measurement(1, "ground_humidity", 352343, 71.442)
    sc.add_measurement(1, "sdd_humidity", 352343, 71.442)
    sleep(5)
    sc.add_measurement(3, "temp", 343, 21.223)
    sleep(5)
    sc.add_measurement(1, "has_slept", 443, 213.223)

    print(sc.get_measurements())
