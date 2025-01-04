import random

from modules.models import Student, ReportCard, Subject
class Student:
    def __init__(self, student_id, name, age):
        self.id = student_id
        self.name = name
        self.age = age



class StudentService:
    def __init__(self):
        self.students = []  # List to store student objects
        self.subjects = []  # List to store subject objects
        self.report_cards = {}  # Dictionary to store report cards by student ID

    def add_student(self, name, age):
        # Generate a unique student ID
        student_id = f"STU-{random.randint(1000, 9999)}"

        # Create a new student object
        student = Student(student_id, name, age)

        # Add the student to the list
        self.students.append(student)

        return student

    def assign_subject(self, student_id, subject_name):
        # Check if student exists
        student = next((s for s in self.students if s.id == student_id), None)
        if student:
            subject = Subject(subject_name)
            self.subjects.append(subject)
            return subject
        return None

    def input_marks(self, student_id, subject_name, marks):
        # Find the student by ID
        student = next((s for s in self.students if s.id == student_id), None)
        if student:
            report_card = self.report_cards.get(student_id, ReportCard(student))
            report_card.add_marks(subject_name, marks)
            self.report_cards[student_id] = report_card
            return report_card
        return None

    def generate_report(self, student_id):
        # Check if the report card exists for the student
        if student_id not in self.report_cards:
            print(f"Error: No report card found for student ID '{student_id}'.")
            return None

        # Get the report card for the student
        report_card = self.report_cards[student_id]

        # Format the report
        report = f"Student ID: {student_id}\n"
        total_marks = sum(report_card.marks.values())
        grade = self.calculate_grade(total_marks)
        report += f"Total Marks: {total_marks}\nGrade: {grade}\nMarks by Subject:\n"
        for subject, marks in report_card.marks.items():
            report += f"  {subject}: {marks}\n"

        return report

    def calculate_grade(self, total_marks):
        # Grade calculation logic based on total marks
        if total_marks >= 90:
            return 'A'
        elif total_marks >= 75:
            return 'B'
        elif total_marks >= 60:
            return 'C'
        else:
            return 'D'
