import os
from pathlib import Path
import json
from paths import PROJECT_ROOT
from paths import GRADEBOOK_DIR

class Person:
    def __init__(self, name,surname, birth_date, grades):
        self.name = name
        self.surname = surname
        self.username = _generate_username()
        self.birth_date = birth_date
        self.grades = grades()
    def _generate_username(self):
       return "foo" 

    def serialize(self):
        return json.dumps({
            "first_name": self.name,
            "last_name": self.surname,
            "username": self.username,
            "birth_date": self.birth_date,
            "grades": self.grades
            })

def make_gradebook(teacher_name, class_name):
    try:
        with open(GRADEBOOK_DIR/class_name, "x") as file:
            file.write(json.dumps({
                "class": class_name
                "teacher":teacher_name
                }))
    except OSError as e:
        print(f"Error when creating database file.\n{e}")

class Gradebook:
    def __init__(self, class_name):
        self.class_name = class_name
        self.database_file = open(GARDEBOOK_DIR/class_name, "a")
    def read_student(self, name):
       pass 
    def create_record(self):
        pass


        

