import random



class Student:
    def __init__(self, name, age):
        self.id = f"STU-{random.randint(1000, 9999)}"
        self.name = name
        self.age = age
        self.subjects = []

    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.age})"


class Subject:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Subject({self.name})"


class ReportCard:
    def __init__(self, student_id):
        self.id = f"RC-{random.randint(1000, 9999)}"
        self.student_id = student_id
        self.marks = {}


    def __init__(self, student):
                self.student = student
                self.marks = {}  # Dictionary to store marks by subject

    def add_marks(self, subject_name, marks):
                self.marks[subject_name] = marks
                print(f"Added marks for subject '{subject_name}': {marks}")

    def calculate_total_and_grade(self):
        total_marks = sum(self.marks.values())
        grade = self.get_grade(total_marks)
        return total_marks, grade

    @staticmethod
    def get_grade(total_marks):
        if total_marks >= 90:
            return 'A'
        elif total_marks >= 75:
            return 'B'
        elif total_marks >= 50:
            return 'C'
        else:
            return 'D'
