import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from services.student_service import StudentService
from helper import display_student_report


def main():
    service = StudentService()
    print(dir(service))
    print("Welcome to the Student Report Card System!")

    while True:
        print("\nMenu:")
        print("1. Add a Student")
        print("2. Assign Subject to a Student")
        print("3. Input Marks")
        print("4. Generate Report Card")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            # Add a new student
            name = input("Enter student's name: ")
            age = int(input("Enter student's age: "))
            student = service.add_student(name, age)
            print(f"Student added successfully with ID: {student.id}")

        elif choice == "2":
            # Assign a subject to a student
            student_id = input("Enter student ID: ")
            subject_name = input("Enter subject name: ")
            subject = service.assign_subject(student_id, subject_name)
            if subject:
                print(f"Subject '{subject.name}' assigned to student with ID: {student_id}")
            else:
                print("Student ID not found!")

        elif choice == "3":
            # Input marks for a student
            student_id = input("Enter student ID: ")
            subject_name = input("Enter subject name: ")
            marks = int(input("Enter marks: "))
            report_card = service.input_marks(student_id, subject_name, marks)
            if report_card:
                print(f"Marks for '{subject_name}' updated for student ID: {student_id}")
            else:
                print("Report Card not found for this student ID!")

        elif choice == "4":
            # Generate report card for a student
            student_id = input("Enter student ID: ")
            report = service.generate_report(student_id)
            if report:
                display_student_report(report)
            else:
                print(f"Error: Report card not found for student ID '{student_id}'.")

        elif choice == "5":
            # Exit the program
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
