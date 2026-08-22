# Student Performance Management System

A Python-based desktop application for managing student records and tracking student performance. The application provides a graphical user interface (GUI), login authentication, database management, and student record operations.

## Technologies Used

- Python
- Tkinter
- SQLite
- CSV

## Features

- User login authentication
- Dashboard interface
- Add student records
- Update student records
- Delete student records
- View student records
- Search students by name
- Filter students based on performance
- Automatic performance classification based on marks
- Export student records to CSV
- Light and dark theme
- Input validation

## Performance Classification

The system automatically classifies student performance based on marks:

- 75 and above – Excellent
- 60–74 – Good
- 40–59 – Average
- Below 40 – Needs Improvement

## Database

The application uses SQLite for storing user login information and student records.

The student database stores:

- Student ID
- Name
- Roll Number
- Course
- Marks
- Performance

## Project Structure

```text
student-management-system/
│
├── main.py
├── login.py
├── dashboard.py
├── student.py
├── database.py
└── README.md
