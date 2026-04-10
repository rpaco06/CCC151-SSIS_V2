import re

def is_empty(data):
    return not all(data.values())

def valid_student_id(sid):
    return bool(re.match(r"^\d{4}-\d{4}$", sid))

def validate_college(data):
    if is_empty(data):
        return "Please fill in all fields."
    return None

def validate_program(data):
    if is_empty(data):
        return "Please fill in all fields."
    return None

def validate_student(data):
    if is_empty(data):
        return "Please fill in all fields."
    if not valid_student_id(data["id"]):
        return "Student ID must follow the format YYYY-NNNN (e.g. 2024-0001)."
    return None