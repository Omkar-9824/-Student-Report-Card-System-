# Configuration settings can be defined here, such as database or file paths.
APP_NAME = "Student Report Card System"
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='student_report_card',
                user='root',
                password='1982'
            )
            return connection
            
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return None


db=DatabaseConfig()
db.get_connection()


