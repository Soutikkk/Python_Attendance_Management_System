# Python Attendance Management System

A simple, terminal-based, object-oriented application for tracking student attendance. It uses CSV files for persistent storage and includes validation logic to prevent duplicates and ensure data integrity.
(Vibecoded)

## Features

- **Menu-Driven Interface**: Easy to navigate command-line menus.
- **Student Management**: Add new students with unique IDs, names, and classes/sections.
- **Attendance Tracker**: Mark attendance (Present/Absent) for any student on a specific date.
- **Robust Validation**:
  - Ensures Student IDs are unique.
  - Prevents duplicate attendance marking for a student on the same date.
  - Validates date formats (YYYY-MM-DD) and status inputs.
  - Gracefully handles invalid menu selections.
- **File Persistence**: Stores all student details in `students.csv` and attendance records in `attendance.csv`.
- **Search Capability**: Look up a student by their ID to check details and current attendance percentage.
- **Summary Report**: Generate an overall attendance summary report displaying present/absent counts and attendance percentages for all students.

---

## File Structure

```
├── attendance_system.py  # Main Python executable
├── students.csv          # Persisted student data (auto-generated)
├── attendance.csv        # Persisted attendance records (auto-generated)
└── README.md             # Project documentation
```

---

## How to Run

### Prerequisites
- Python 3.x installed on your machine.

### Execution
1. Clone this repository or download the source code:
   ```bash
   git clone https://github.com/Soutikkk/Python_Attendance_Management_System.git
   cd Python_Attendance_Management_System
   ```
2. Run the application:
   ```bash
   python attendance_system.py
   ```

---

## Sample Usage and Output

### 1. Main Menu
```
===================================
   Attendance Management System   
===================================
1. Add Student
2. View Students
3. Search Student by ID
4. Mark Attendance
5. View Attendance Records
6. Generate Attendance Summary Report
7. Exit
===================================
Enter choice (1-7): 
```

### 2. Adding a Student
```
--- Add Student ---
Enter Student ID: S101
Enter Student Name: Alice Johnson
Enter Class/Section: Grade 10-A
[Success] Student 'Alice Johnson' added successfully.
```

### 3. Registering Duplicate Student ID (Validation)
```
--- Add Student ---
Enter Student ID: S101
Enter Student Name: Bob Smith
Enter Class/Section: Grade 10-B
[Error] A student with ID 'S101' already exists.
```

### 4. Viewing Students
```
=== Student List ===
Student ID      | Name                      | Class/Section  
------------------------------------------------------------
S101            | Alice Johnson             | Grade 10-A     
S102            | Bob Smith                 | Grade 10-B     
====================
```

### 5. Marking Attendance
```
--- Mark Attendance ---
Enter Student ID: S101
Enter Date (YYYY-MM-DD) [Press Enter for Today (2026-06-20)]: 
Enter Status (P for Present / A for Absent): P
[Success] Attendance marked as Present for student 'Alice Johnson' on 2026-06-20.
```

### 6. Marking Duplicate Attendance (Validation)
```
--- Mark Attendance ---
Enter Student ID: S101
Enter Date (YYYY-MM-DD) [Press Enter for Today (2026-06-20)]: 
Enter Status (P for Present / A for Absent): A
[Error] Attendance for student ID 'S101' on 2026-06-20 has already been marked as 'Present'.
```

### 7. Searching for a Student
```
--- Search Student ---
Enter Student ID to Search: S101

=== Student Details ===
ID:            S101
Name:          Alice Johnson
Class/Section: Grade 10-A
Attendance:    100.00%
=======================
```

### 8. Generating the Summary Report
```
=== Attendance Summary Report ===
ID         | Name                 | Class/Sec    | Present | Absent  | Percentage
---------------------------------------------------------------------------
S101       | Alice Johnson        | Grade 10-A   | 1       | 0       | 100.00%
S102       | Bob Smith            | Grade 10-B   | 0       | 0       | 0.00%
=================================
```

---

## Technical Details

### CSV File Schemas

#### `students.csv`
```csv
student_id,name,class_section
S101,Alice Johnson,Grade 10-A
S102,Bob Smith,Grade 10-B
```

#### `attendance.csv`
```csv
date,student_id,status
2026-06-20,S101,Present
```

### Object-Oriented Principles
- **Encapsulation**: Student attributes and behaviors are encapsulated in the `Student` class. The `AttendanceManager` coordinates student listings, attendance logs, verification logic, and file I/O operations.
- **Data Integrity**: Checks for invalid dates, missing students, duplicate IDs, and duplicate attendance are centralized inside core manager methods.
