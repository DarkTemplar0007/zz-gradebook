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
        self.username = self._generate_username()
        self.birth_date = birth_date
        self.grades = grades
    
    def _generate_username(self):
       return "foo" 

    def serialize(self) -> str:
        return json.dumps({
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "birth_date": self.birth_date,
            "grades": self.grades,
            }, ensure_ascii = False) + "\n"

def make_gradebook_file(teacher_name: str, class_name: str, file_path: str):
    if os.path.isfile(file_path):
        raise DatabaseError(f"File {file_path} alredy exists, modify it with apropriate Gradebook methods or delete it manually")
    else:
        try:
            with open(file_path, "w") as file:
                file.write(json.dumps({
                    "class": class_name,
                    "teacher": teacher_name,
                    }, ensure_ascii = False) + "\n")
                file.close()
        except OSError as e:
            raise DatabaseError(f"Error initialising database file.\n {e}")

class Gradebook:
    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            self.database_file = open(self.file_path, "r+")
        except OSError as e:
            raise DatabaseError(f"Error reading database file\n {e}")

    def write_database_to_disk(self):
        try:
            self.database_file.flush()
            os.fsync(self.database_file.fileno())
        except IOError as e:
            raise DatabaseError(f"Write to disk failed.\n {e}")

    def read_student(self, username: str) -> Person:
        try:
            self.database_file.seek(0)
            for line in self.database_file.readlines()[1:]:
                data = json.loads(line)
                if data["username"] == username:
                    return Person(name = data["name"],
                                  surname = data["surname"], 
                                  username = data["username"],
                                  birth_date = data["birth_date"],
                                  grades = data["grades"]
                          )
        except json.JSONDecodeError as e:
            raise DatabaseError(f"Error converting data from json\n {e}")

    def create_record(self, Student: Type[Person]):
        try:
            self.database_file.seek(0, 2)
            if self.student_in_database(Student.username) == False:
                self.database_file.write(Student.serialize())
            else:
                raise DatabaseError(f"Student exists, to modify, use modify_record method")
        except IOError as e:
                raise DatabaseError(f"Error creating record\n {e}")

    def student_in_database(self, username: str) -> Bool:
        try:
            self.database_file.seek(0)
            for line in self.database_file.readlines()[1:]:
                data = json.loads(line)
                if data["username"] == username:
                    return True
            return False

        except json.JSONDecodeError as e:
            raise DatabaseError(f"Error converting data from json\n {e}")
        except KeyError as e:
            raise DatabaseError(f"Error reading username from record\n {e}")

    def modify_record(self, modified_student: Type[Person]):
        try:
            self.database_file.seek(0)
            lines = self.database_file.readlines()
            linenum = 0
            for i in range(len(lines)):
                if i == 0:
                    pass
                else:
                    data = json.loads(lines[i])
                    if data["username"] == modified_student.username:
                        lines[i] = modified_student.serialize()
                    linenum += 1
            self.database_file.seek(0)
            self.database_file.writelines(lines)
        except (json.JSONDecodeError, KeyError, IOError) as e: 
            raise DatabaseError(f" Error modifiing student record\n{e}")

