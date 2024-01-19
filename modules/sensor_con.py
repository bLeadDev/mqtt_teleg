import sqlite3

SENSOR_DATABASE_NAME = "sensors.db"
SENSOR_TABLE_NAME = "sensors"

class SensorContainer:
    """SensorContainer class"""

    __sensor_list = None

    def __select_db(self):
        """Opens database and reads every sensor in the owned datastructure."""
        connection = sqlite3.connect(SENSOR_DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM """ + SENSOR_TABLE_NAME)
        self.__sensor_list = cursor.fetchall()
        connection.close()

    def create_db(self):
        """
        Create Database for Sensors following this structure:
            ID as INT PK,
            type as TEXT,
            lowCalibrationPoint as INT,
            highCalibrationPoint as INT,
            isCalibrated as INT
        """
        connection = sqlite3.connect(SENSOR_DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE " + SENSOR_TABLE_NAME + " (ID INT PRIMARY KEY, type TEXT, lowCalibrationPoint INT, highCalibrationPoint INT, isCalibrated INT)"
        )

        cursor.execute(
            "INSERT INTO " + SENSOR_TABLE_NAME + " VALUES (?, ?, ?, ?, ?)",
            (
                0,
                "ground_humidity",
                0,
                0,
                0
            ),
        )
        cursor.execute(
            "INSERT INTO " + SENSOR_TABLE_NAME + "  VALUES (?, ?, ?, ?, ?)",
            (
                1,
                "ground_humidity",
                0,
                0,
                0
            ),
        )
        cursor.execute(
            "INSERT INTO " + SENSOR_TABLE_NAME + " VALUES (?, ?, ?, ?, ?)",
            (
                2,
                "ground_humidity_and_temperature",
                0,
                48197,
                1
            ),
        )
        connection.commit()
        connection.close()

    def get_sensor(self, sensor_id):
        """returns the sensor with the given id as tuple"""
        if self.__sensor_list == None:
            self.__select_db()
        return self.__sensor_list[sensor_id]

    def get_sensors(self):
        """returns all sensors as list of tuples"""
        if self.__sensor_list == None:
            self.__select_db()
        return self.__sensor_list

    def set_sensor(
        self,
        sensor_id,
        sensor_type,
        sensor_low_calibration_point,
        sensor_high_calibration_point,
        sensor_is_calibrated,
    ):
        connection = sqlite3.connect(SENSOR_DATABASE_NAME)
        cursor = connection.cursor()
        if sensor_id < len(self.__sensor_list):
            cursor.execute(
                "UPDATE " + SENSOR_TABLE_NAME + " SET type=?, lowCalibrationPoint=?, highCalibrationPoint=?, isCalibrated=? WHERE id=?", 
                (
                    sensor_type,
                    sensor_low_calibration_point,
                    sensor_high_calibration_point,
                    sensor_is_calibrated,
                    sensor_id
                ),
            )
        else:
            cursor.execute(
                "INSERT INTO " + SENSOR_TABLE_NAME + " VALUES (?, ?, ?, ?, ?)",
                (
                    sensor_id,
                    sensor_type,
                    sensor_low_calibration_point,
                    sensor_high_calibration_point,
                    sensor_is_calibrated,
                ),
            )
        cursor.execute("""SELECT * FROM """ + SENSOR_TABLE_NAME)
        self.__sensor_list = cursor.fetchall()
        connection.commit()
        connection.close()

    def get_number_of_sensors(self):
        if self.__sensor_list == None:
            self.__select_db()
        return len(self.__sensor_list)


if __name__ == "__main__":

    sc = SensorContainer()

    print(sc.get_sensor(0))
    print(sc.get_sensors())
    print(sc.get_number_of_sensors())
    sc.set_sensor(1, "ground_humidity", 2, 352343, 4)
    print(sc.get_sensor(1))