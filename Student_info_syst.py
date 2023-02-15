import tkinter as tk
import sqlite3
from tkinter import messagebox

class Student:
    def __init__(self, name, grade, attendance, discipline):
        self.name = name
        self.grade = grade
        self.attendance = attendance
        self.discipline = discipline


class StudentInfoSystem:
    def __init__(self):
        self.students = []
        self.root = tk.Tk()
        self.root.title("Student Information System")
        self.db_conn = sqlite3.connect('students.db')
        self.create_tables()
        self.create_widgets()

    def create_tables(self):
        cursor = self.db_conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, grade INTEGER, attendance INTEGER, discipline INTEGER)')

    def create_widgets(self):
        # Create a grid system with 3 columns and multiple rows
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)

        tk.Label(self.root, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5, pady=5)

        tk.Label(self.root, text="Grade:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.grade_entry = tk.Entry(self.root)
        self.grade_entry.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=5)

        tk.Label(self.root, text="Attendance:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.attendance_entry = tk.Entry(self.root)
        self.attendance_entry.grid(row=2, column=1, columnspan=2, sticky='ew', padx=5, pady=5)

        tk.Label(self.root, text="Discipline:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.discipline_entry = tk.Entry(self.root)
        self.discipline_entry.grid(row=3, column=1, columnspan=2, sticky='ew', padx=5, pady=5)

        tk.Button(self.root, text="Add Student", command=self.add_student).grid(row=4, column=1, columnspan=2,
                                                                                sticky='ew', padx=5, pady=5)

        self.student_listbox = tk.Listbox(self.root)
        self.student_listbox.grid(row=5, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)

        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=6, column=1, columnspan=2, sticky='ew', padx=5, pady=5)

        self.load_data()

    def add_student(self):
        name = self.name_entry.get()
        grade = self.grade_entry.get()
        attendance = self.attendance_entry.get()
        discipline = self.discipline_entry.get()

        if not name or not grade or not attendance or not discipline:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            grade = int(grade)
            attendance = int(attendance)
            discipline = int(discipline)
        except ValueError:
            messagebox.showerror("Error", "Grade, attendance, and discipline must be integers.")
            return

        student = Student(name, grade, attendance, discipline)
        self.students.append(student)
        self.save_student_to_database(student)
        self.clear_form()
        self.load_data()

    def save_student_to_database(self, student):
        cursor = self.db_conn.cursor()
        cursor.execute('INSERT INTO students VALUES (?, ?, ?, ?)', (student.name, student.grade, student.attendance, student.discipline))
        self.db_conn.commit()

    def load_data(self):
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT * FROM students')

        self.students = []
        for row in cursor:
            student = Student(row[0], row[1], row[2], row[3])
            self.students.append(student)

        self.student_listbox.delete(0, tk.END)
        for student in self.students:
            self.student_listbox.insert(tk.END, f"{student.name} - Grade: {student.grade} - Attendance: {student.attendance}% - Discipline: {student.discipline}")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.attendance_entry.delete(0, tk.END)
        self.discipline_entry.delete(0, tk.END)

    def generate_report(self):
        total_students = len(self.students)
        total_grades = sum([student.grade for student in self.students])
        avg_grade = total_grades / total_students if total_students != 0 else 0

        total_attendance = sum([student.attendance for student in self.students])
        avg_attendance = total_attendance / total_students if total_students != 0 else 0

        total_discipline = sum([student.discipline for student in self.students])
        avg_discipline = total_discipline / total_students if total_students != 0 else 0

        report = f"Total students: {total_students}\n"
        report += f"Average grade: {avg_grade}\n"
        report += f"Average attendance: {avg_attendance}%\n"
        report += f"Average discipline score: {avg_discipline}\n"

        messagebox.showinfo("Report", report)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    student_info_system = StudentInfoSystem()
    student_info_system.run()
