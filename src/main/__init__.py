import sys
import os
import random
from tabulate import tabulate

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DatabaseConfig
from config.database import *
from services.student_service import StudentService
from helper import display_student_report

# Mocking an admin login
admin_credentials = {'admin': 'admin123'}

def admin_login():
    """Authenticate admin user."""
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if admin_credentials.get(username) == password:
        print("Admin logged in successfully!")
        return True
    else:
        print("Invalid admin credentials!")
        return False

def candidate_register(service):
    """Register a new candidate (student)."""
    username = input("Enter your username (Student ID or Email): ")
    password = input("Enter your password: ")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    student_id = service.add_student(name, age)
    # For simplicity, we simulate adding the student credentials to the database
    print(f"Candidate registered successfully with ID: {student_id}")
    return student_id, username, password

def candidate_login(candidates_db):
    """Log in an existing candidate."""
    username = input("Enter your username (Student ID or Email): ")
    password = input("Enter your password: ")
    if candidates_db.get(username) == password:
        print("Candidate logged in successfully!")
        return username
    else:
        print("Invalid credentials!")
        return None

def main():
    service = StudentService()
    candidates_db = {}  # This will simulate a database of registered candidates
    
    print("Welcome to the Student Report Card System!")
    
    while True:
        print("\nMenu:")
        print("1. Admin Login")
        print("2. Candidate Registration")
        print("3. Candidate Login")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            # Admin login
            if admin_login():
                while True:
                    print("\nAdmin Menu:")
                    print("1. Add a Student")
                    print("2. Add a Subject")
                    print("3. Input Marks")
                    print("4. Generate Report Card")
                    print("5. Exit Admin")

                    admin_choice = input("Enter your choice (1-5): ")

                    if admin_choice == "1":
                        # Add a new student
                        name = input("Enter student's name: ")
                        age = int(input("Enter student's age: "))
                        student_id = service.add_student(name, age)
                        print(f"Student added successfully with ID: {student_id}")

                    elif admin_choice == "2":
                        # Add a new subject
                        subject_name = input("Enter the subject name: ")
                        subject = service.add_subject(subject_name)
                        if subject:
                            print(f"Subject '{subject}' added successfully.")
                        else:
                            print(f"Error adding subject.")

                    elif admin_choice == "3":
                        # Input marks for a student
                        student_id = input("Enter student ID: ")
                        subject_name = input("Enter subject name: ")
                        marks = int(input("Enter marks: "))
                        success = service.input_marks(student_id, subject_name, marks)
                        if success:
                            print(f"Marks for '{subject_name}' updated for student ID: {student_id}")
                        else:
                            print("Marks not updated due to errors!")

                    elif admin_choice == "4":
                        # Generate report card for a student
                        student_id = input("Enter student ID: ")
                        report = service.generate_report(student_id)
                        if report:
                            print(report)
                        else:
                            print(f"Error: Report card not found for student ID '{student_id}'.")

                    elif admin_choice == "5":
                        # Exit Admin
                        print("Exiting admin panel.")
                        break

                    else:
                        print("Invalid choice. Please enter a number between 1 and 5.")
        
        elif choice == "2":
            # Candidate Registration
            student_id, username, password = candidate_register(service)
            candidates_db[username] = password  # Simulating saving to a database

        elif choice == "3":
            # Candidate Login
            logged_in_user = candidate_login(candidates_db)
            if logged_in_user:
                while True:
                    print("\nCandidate Menu:")
                    print("1. View Report Card")
                    print("2. Exit")

                    candidate_choice = input("Enter your choice (1-2): ")

                    if candidate_choice == "1":
                        # View report card for the logged-in student
                        report = service.generate_report(logged_in_user)
                        if report:
                            print(report)
                        else:
                            print(f"Error: Report card not found for student '{logged_in_user}'.")

                    elif candidate_choice == "2":
                        # Exit Candidate menu
                        print("Exiting candidate menu.")
                        break

                    else:
                        print("Invalid choice. Please enter a number between 1 and 2.")
        
        elif choice == "4":
            # Exit the program
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
