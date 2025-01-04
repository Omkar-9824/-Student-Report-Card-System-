import sys
import os
import mysql.connector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DatabaseConfig

def create_tables():
    connection = None
    cursor = None
    try:
        connection = DatabaseConfig.get_connection()
        if connection:
            cursor = connection.cursor()

            # Create students table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(255) PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
            ''')

            # Create subjects table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                subject_name TEXT
            )
            ''')

            # Create marks table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                mark_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                student_id VARCHAR(255),
                subject_id INTEGER,
                marks INTEGER,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
            )
            ''')

            # Create report cards table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS report_cards (
                report_card_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                student_id VARCHAR(255),
                total_marks INTEGER,
                grade TEXT,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            ''')
            
            # Create admin credentials table
            cursor.execute('''CREATE TABLE IF NOT EXISTS admin_credentials (
                username VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )''')

            # Hardcode admin username and password for authentication
            cursor.execute('''SELECT * FROM admin_credentials WHERE username = %s''', ('admin',))
            if cursor.fetchone() is None:
                cursor.execute('''INSERT INTO admin_credentials (username, password) VALUES (%s, %s)''',
                               ('admin', 'admin123'))  # Hardcoded username and password
                connection.commit()

            connection.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

create_tables()  # Call this function once to create the tables