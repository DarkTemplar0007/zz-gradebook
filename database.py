# Some inspiraion from https://github.com/vndee/toydb-python.git was taken

import os
from pathlib import Path
import json
from typing import Type
class DatabaseError(Exception): # Base class for database errors
    pass

class Person: # Class for data to be stored in database
    def __init__(self, name,surname, birth_date, grades):
        self.name = name
        self.surname = surname
        self.username = _generate_username()
        self.birth_date = birth_date
        self.grades = grades()
    
    def _generate_username(self):
       return "foo" 

    def serialize(self) -> str:
        return json.dumps({
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "birth_date": self.birth_date,
            "grades": self.grades,
            })

def make_gradebook_file(teacher_name: str, class_name: str, file_path: str):
    try:
        with open(filepath, "w") as file:
            file.write(json.dumps({
                "class": class_name,
                "teacher": teacher_name,
                }))
    except OSError as e:
        raise DatabaseError(f"Error initialising database file.\n {e}")

class Gradebook:
    def __init__(self, class_name: str, file_path: str):
        self.filepath = file_path
        try:
            self.database_file = open(self.filepath "a")
        except OSError as e:
            raise DatabaseError(f"Error reading database file\n {e}")

    def write_database_to_disk(self):
        try:
            self.database_file.flush()
            os.fsync(self.database_file.fileno())
        except IOError as e:
            raise DatabaseError(f"Write to disk failed.\n {e}")

    def read_student(self, line) -> Person:
        try:
            data = json.loads(line)
            return Person(name = data["name"],
                          surname = data["surname"], 
                          username = data["username"],
                          birth_date = data["birth_date"],
                          grades = data["grades"]
                          )
        except json.JSONDecodeError as e:
            raise DatabaseError(f"Error converting data from json\n {e}")

    def create_record(self, Student: Type[Person]) -> str:
        try:
            if self.student_in_database(Student.username) == False:
                self.database_file.write(Student.serialize())
        except:
            IOError as e:
                raise DatabaseError(f"Error creating record\n {e}")

    def student_in_database(self, username: str) -> Bool:
        try:
            for line in self.database_file:
                data = json.loads(line)
                if data["username"] == username:
                    return True
            return False
        except json.JSONDecodeError as e:
            raise DataError(f"Error converting data from json\n {e}")
        except KeyError as e:
            raise DataError(f"Error reading username from record\n {e}")

    def modify_student(self, modified_student: Type[Person]):
        try:
            lines = self.database_file.readlines()
            linenum = 0
            for line in lines:
                if line["username"] == modified_student.username:
                    lines[linenum] = modified_student.serialize()
            self.databse_file.writelines(lines)
        except json.JSONDecodeErorr, KeyError, IOError as e: 
            raise DatabaseError(f" Error modifiing student record\n{e}")

