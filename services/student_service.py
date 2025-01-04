import sys
import os
import mysql.connector
from mysql.connector import Error

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DatabaseConfig

class StudentService:
    
    def create_connection(self):
        """Create a database connection and return it."""
        connection = DatabaseConfig.get_connection()
        return connection

    def add_student(self, name, age):
     connection = None
     cursor = None
     try:
         connection = self.create_connection()
         if connection:
            cursor = connection.cursor()

            # Insert student logic
            cursor.execute('''INSERT INTO students (name, age) VALUES (%s, %s)''', (name, age))
            connection.commit()

            # Get the student ID of the newly inserted student
            cursor.execute("SELECT LAST_INSERT_ID()")
            student_id = cursor.fetchone()[0]

            return student_id  # Return the student ID

     except mysql.connector.Error as e:
        print(f"Error while adding student: {e}")
     finally:
        # Ensure cursor and connection are closed properly
        if cursor:
            cursor.close()
        if connection:
            connection.close()



    def assign_subject(self, student_id, subject_name):
        """Assign a subject to the student."""
        connection = None
        cursor = None
        try:
            connection = self.create_connection()
            if connection:
                cursor = connection.cursor()

                # Get subject ID
                cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
                subject_id = cursor.fetchone()
                if not subject_id:
                    print(f"Subject '{subject_name}' not found.")
                    return None

                # Insert subject assignment logic (e.g., linking student and subject)
                cursor.execute("INSERT INTO student_subjects (student_id, subject_id) VALUES (%s, %s)", (student_id, subject_id[0]))
                connection.commit()
                print(f"Subject '{subject_name}' assigned to student with ID: {student_id}")
                return subject_name  # Return the subject name as confirmation
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def input_marks(self, student_id, subject_name, marks):
        """Input marks for a student."""
        connection = None
        cursor = None
        try:
            connection = self.create_connection()
            if connection:
                cursor = connection.cursor()

                # Get the subject ID
                cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
                subject_id = cursor.fetchone()
                if not subject_id:
                    print(f"Subject '{subject_name}' not found.")
                    return None

                # Insert marks into the marks table
                cursor.execute("INSERT INTO marks (student_id, subject_id, marks) VALUES (%s, %s, %s)",
                               (student_id, subject_id[0], marks))
                connection.commit()
                print(f"Marks for '{subject_name}' added successfully for student ID: {student_id}.")
                return True  # Marks were successfully added
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
            if connection:
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
