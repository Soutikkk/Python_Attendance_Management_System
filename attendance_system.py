"""
Attendance Management System
A simple, terminal-based, object-oriented application for tracking student attendance.
Uses CSV files to persist data.
"""

import csv
import datetime
import os


class Student:
    """Represents a student in the system."""

    def __init__(self, student_id: str, name: str, class_section: str):
        self.student_id = student_id.strip()
        self.name = name.strip()
        self.class_section = class_section.strip()

    def to_dict(self) -> dict:
        """Serializes student details to a dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_section": self.class_section,
        }

    def __str__(self) -> str:
        return f"ID: {self.student_id} | Name: {self.name} | Class/Section: {self.class_section}"


class AttendanceManager:
    """Manages students and attendance records, including file persistence."""

    def __init__(self, students_csv: str = "students.csv", attendance_csv: str = "attendance.csv"):
        self.students_csv = students_csv
        self.attendance_csv = attendance_csv
        self.students = {}  # student_id -> Student object
        self.attendance = []  # List of dicts: {"date": str, "student_id": str, "status": str}
        self.load_data()

    def load_data(self):
        """Loads students and attendance records from CSV files."""
        # Load students
        if os.path.exists(self.students_csv):
            try:
                with open(self.students_csv, mode="r", encoding="utf-8", newline="") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Ensure columns exist before parsing
                        if "student_id" in row and "name" in row and "class_section" in row:
                            student = Student(
                                student_id=row["student_id"],
                                name=row["name"],
                                class_section=row["class_section"]
                            )
                            self.students[student.student_id] = student
            except Exception as e:
                print(f"[Error] Failed to load student data: {e}")

        # Load attendance records
        if os.path.exists(self.attendance_csv):
            try:
                with open(self.attendance_csv, mode="r", encoding="utf-8", newline="") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if "date" in row and "student_id" in row and "status" in row:
                            self.attendance.append({
                                "date": row["date"].strip(),
                                "student_id": row["student_id"].strip(),
                                "status": row["status"].strip()
                            })
            except Exception as e:
                print(f"[Error] Failed to load attendance data: {e}")

    def save_data(self):
        """Saves students and attendance records to CSV files."""
        # Save students
        try:
            with open(self.students_csv, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = ["student_id", "name", "class_section"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students.values():
                    writer.writerow(student.to_dict())
        except Exception as e:
            print(f"[Error] Failed to save student data: {e}")

        # Save attendance
        try:
            with open(self.attendance_csv, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = ["date", "student_id", "status"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.attendance:
                    writer.writerow(record)
        except Exception as e:
            print(f"[Error] Failed to save attendance data: {e}")

    def add_student(self, student_id: str, name: str, class_section: str) -> bool:
        """Adds a new student to the system. Returns True if successful, False otherwise."""
        student_id = student_id.strip()
        if not student_id:
            print("[Error] Student ID cannot be empty.")
            return False
        if not name.strip():
            print("[Error] Student Name cannot be empty.")
            return False
        if not class_section.strip():
            print("[Error] Class/Section cannot be empty.")
            return False

        if student_id in self.students:
            print(f"[Error] A student with ID '{student_id}' already exists.")
            return False

        student = Student(student_id, name, class_section)
        self.students[student_id] = student
        self.save_data()
        print(f"[Success] Student '{name}' added successfully.")
        return True

    def view_students(self):
        """Displays all students registered in the system."""
        if not self.students:
            print("[Info] No students registered in the system.")
            return

        print("\n=== Student List ===")
        print(f"{'Student ID':<15} | {'Name':<25} | {'Class/Section':<15}")
        print("-" * 60)
        for student in self.students.values():
            print(f"{student.student_id:<15} | {student.name:<25} | {student.class_section:<15}")
        print("====================")

    def search_student(self, student_id: str) -> bool:
        """Searches and displays a student by ID."""
        student_id = student_id.strip()
        if student_id in self.students:
            student = self.students[student_id]
            print("\n=== Student Details ===")
            print(f"ID:            {student.student_id}")
            print(f"Name:          {student.name}")
            print(f"Class/Section: {student.class_section}")
            percentage = self.calculate_attendance_percentage(student_id)
            print(f"Attendance:    {percentage:.2f}%")
            print("=======================")
            return True
        else:
            print(f"[Error] Student with ID '{student_id}' not found.")
            return False

    def mark_attendance(self, student_id: str, date_str: str, status: str) -> bool:
        """Marks attendance for a student on a specific date."""
        student_id = student_id.strip()
        status = status.strip().title()

        # Validation
        if student_id not in self.students:
            print(f"[Error] Student with ID '{student_id}' does not exist.")
            return False

        if status not in ["Present", "Absent"]:
            print("[Error] Invalid status. Please specify 'Present' or 'Absent'.")
            return False

        # Validate date
        try:
            validated_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = validated_date.strftime("%Y-%m-%d")
        except ValueError:
            print("[Error] Invalid date format. Use YYYY-MM-DD.")
            return False

        # Prevent duplicates
        for record in self.attendance:
            if record["student_id"] == student_id and record["date"] == formatted_date:
                print(f"[Error] Attendance for student ID '{student_id}' on {formatted_date} has already been marked as '{record['status']}'.")
                return False

        # Add record
        self.attendance.append({
            "date": formatted_date,
            "student_id": student_id,
            "status": status
        })
        self.save_data()
        print(f"[Success] Attendance marked as {status} for student '{self.students[student_id].name}' on {formatted_date}.")
        return True

    def view_attendance(self):
        """Displays all attendance records."""
        if not self.attendance:
            print("[Info] No attendance records found.")
            return

        print("\n=== Attendance Records ===")
        print(f"{'Date':<12} | {'Student ID':<15} | {'Name':<20} | {'Status':<10}")
        print("-" * 65)
        # Sort by date descending and student ID ascending
        sorted_attendance = sorted(self.attendance, key=lambda x: (x["date"], x["student_id"]), reverse=True)
        for record in sorted_attendance:
            sid = record["student_id"]
            student_name = self.students[sid].name if sid in self.students else "Unknown Student"
            print(f"{record['date']:<12} | {sid:<15} | {student_name:<20} | {record['status']:<10}")
        print("==========================")

    def calculate_attendance_percentage(self, student_id: str) -> float:
        """Calculates the attendance percentage for a student."""
        student_records = [r for r in self.attendance if r["student_id"] == student_id]
        if not student_records:
            return 0.0
        present_count = sum(1 for r in student_records if r["status"] == "Present")
        return (present_count / len(student_records)) * 100

    def generate_summary_report(self):
        """Displays a summary report of attendance for all students."""
        if not self.students:
            print("[Info] No student records available to summarize.")
            return

        print("\n=== Attendance Summary Report ===")
        print(f"{'ID':<10} | {'Name':<20} | {'Class/Sec':<12} | {'Present':<7} | {'Absent':<7} | {'Percentage':<10}")
        print("-" * 75)
        for student_id, student in self.students.items():
            student_records = [r for r in self.attendance if r["student_id"] == student_id]
            total_days = len(student_records)
            present_days = sum(1 for r in student_records if r["status"] == "Present")
            absent_days = total_days - present_days
            percentage = (present_days / total_days * 100) if total_days > 0 else 0.0

            print(f"{student.student_id:<10} | {student.name:<20} | {student.class_section:<12} | {present_days:<7} | {absent_days:<7} | {percentage:.2f}%")
        print("=================================")


def get_non_empty_input(prompt: str) -> str:
    """Helper function to get a non-empty string input from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[Error] Input cannot be blank. Please try again.")


def main():
    """Main application loop."""
    manager = AttendanceManager()

    while True:
        print("\n" + "=" * 35)
        print("   Attendance Management System   ")
        print("=" * 35)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student by ID")
        print("4. Mark Attendance")
        print("5. View Attendance Records")
        print("6. Generate Attendance Summary Report")
        print("7. Exit")
        print("=" * 35)

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            print("\n--- Add Student ---")
            student_id = get_non_empty_input("Enter Student ID: ")
            name = get_non_empty_input("Enter Student Name: ")
            class_section = get_non_empty_input("Enter Class/Section: ")
            manager.add_student(student_id, name, class_section)

        elif choice == "2":
            manager.view_students()

        elif choice == "3":
            print("\n--- Search Student ---")
            student_id = get_non_empty_input("Enter Student ID to Search: ")
            manager.search_student(student_id)

        elif choice == "4":
            print("\n--- Mark Attendance ---")
            if not manager.students:
                print("[Error] No students available. Add students first.")
                continue

            student_id = get_non_empty_input("Enter Student ID: ")
            if student_id not in manager.students:
                print(f"[Error] Student ID '{student_id}' does not exist.")
                continue

            # Accept current date or input date
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            date_input = input(f"Enter Date (YYYY-MM-DD) [Press Enter for Today ({today_str})]: ").strip()
            if not date_input:
                date_input = today_str

            # Validate date input
            try:
                datetime.datetime.strptime(date_input, "%Y-%m-%d")
            except ValueError:
                print("[Error] Invalid date format. Use YYYY-MM-DD.")
                continue

            status_input = input("Enter Status (P for Present / A for Absent): ").strip().upper()
            if status_input == "P" or status_input == "PRESENT":
                status = "Present"
            elif status_input == "A" or status_input == "ABSENT":
                status = "Absent"
            else:
                print("[Error] Invalid status. Enter 'P' or 'A'.")
                continue

            manager.mark_attendance(student_id, date_input, status)

        elif choice == "5":
            manager.view_attendance()

        elif choice == "6":
            manager.generate_summary_report()

        elif choice == "7":
            print("\nExiting program. Goodbye!")
            break

        else:
            print("\n[Error] Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
