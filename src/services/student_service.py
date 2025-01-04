import sys
import os
import mysql.connector
from mysql.connector import Error
from random import random
from random import randint


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DatabaseConfig


class StudentService:
    def create_connection(self):
        """Create a database connection and return it."""
        connection = DatabaseConfig.get_connection()
        return connection

    def add_student(self, name, age):
        """Add a new student to the database."""
        connection = None
        cursor = None
        try:
            connection = self.create_connection()
            cursor = connection.cursor()

            # Generate a new student ID
            student_id = f"S{randint(1000, 9999)}"

            # Insert student record
            cursor.execute('''INSERT INTO students (student_id, name, age) VALUES (%s, %s, %s)''',
                           (student_id, name, age))
            connection.commit()
            return student_id  # Return the generated student ID
        except Error as e:
            print(f"Error while adding student: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def add_subject(self, subject_name):
        """Add a new subject to the database."""
        connection = None
        cursor = None
        try:
            connection = self.create_connection()
            cursor = connection.cursor()

            # Check if the subject already exists
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
            subject = cursor.fetchone()
            if subject:
                print(f"Subject '{subject_name}' already exists in the database.")
                return subject_name

            # Insert subject into the subjects table
            cursor.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subject_name,))
            connection.commit()
            print(f"Subject '{subject_name}' added successfully.")
            return subject_name
        except Error as e:
            print(f"Error while adding subject: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # def assign_subject(self, student_id, subject_name):
    #     """Assign a subject to the student."""
    #     connection = None
    #     cursor = None
    #     try:
    #         connection = self.create_connection()
    #         cursor = connection.cursor()

    #         # Get subject ID
    #         cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
    #         subject_id = cursor.fetchone()
    #         if not subject_id:
    #             print(f"Subject '{subject_name}' not found.")
    #             return None

    #         # Insert subject assignment
    #         cursor.execute("INSERT INTO student_subjects (student_id, subject_id) VALUES (%s, %s)",
    #                        (student_id, subject_id[0]))
    #         connection.commit()
    #         return subject_name  # Return the subject name as confirmation
    #     except Error as e:
    #         print(f"Error: {e}")
    #     finally:
    #         if cursor:
    #             cursor.close()
    #         if connection:
    #             connection.close()

    def input_marks(self, student_id, subject_name, marks):
        """Input marks for a student."""
        connection = None
        cursor = None
        try:
            connection = self.create_connection()
            cursor = connection.cursor()

            # Get subject ID
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
            subject_id = cursor.fetchone()
            if not subject_id:
                print(f"Subject '{subject_name}' not found.")
                return False

            # Insert marks into the marks table
            cursor.execute("INSERT INTO marks (student_id, subject_id, marks) VALUES (%s, %s, %s)",
                           (student_id, subject_id[0], marks))
            connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def generate_report(self, student_id):
        """Generate a report for a student."""
        connection = None
        cursor = None
        try:
            connection = self.create_connection()
            cursor = connection.cursor()

            # Fetch marks and subjects for the student
            query = """
            SELECT subjects.subject_name, marks.marks
            FROM marks
            JOIN subjects ON marks.subject_id = subjects.subject_id
            WHERE marks.student_id = %s
            """
            cursor.execute(query, (student_id,))
            results = cursor.fetchall()

            if not results:
                print(f"No records found for student ID: {student_id}")
                return None

            # Generate the report
            total_marks = sum(row[1] for row in results)
            grade = self.calculate_grade(total_marks)
            report = f"Student ID: {student_id}\n"
            report += f"Total Marks: {total_marks}\nGrade: {grade}\nMarks by Subject:\n"
            for subject, marks in results:
                report += f"  {subject}: {marks}\n"

            # Optionally, insert the report card into the database
            cursor.execute('''INSERT INTO report_cards (student_id, total_marks, grade) VALUES (%s, %s, %s)''',
                           (student_id, total_marks, grade))
            connection.commit()

            return report
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def calculate_grade(self, total_marks):
        """Calculate the grade based on total marks."""
        if total_marks >= 90:
            return 'A'
        elif total_marks >= 75:
            return 'B'
        elif total_marks >= 60:
            return 'C'
        else:
            return 'D'
