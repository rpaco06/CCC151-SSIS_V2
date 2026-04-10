# Student Information System v2

Built with Python (tkinter/ttkbootstrap) and MySQL.

## Setup

1. Install libraries:

2. Create the database in MySQL:
```sql
CREATE DATABASE ssis_v2;
```

3. Open `database.py` and change the password to your MySQL root password:
```python
"password": "your_password_here"
```

4. Run `seed_students.py` to populate the database with sample data.

5. Run `main.py` to start the app.

## Features
- CRUDL for Students, Programs, and Colleges
- Search, Sort, and Pagination
- Built with Python and MySQL