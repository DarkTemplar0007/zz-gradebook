# Some inspiraion from https://github.com/vndee/toydb-python.git was taken

import os
from pathlib import Path
import json
from paths import DATABASE_DIR

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

def make_gradebook_file(teacher_name, class_name):
    try:
        with open(DATABASE_DIR / class_name, "w") as file:
            file.write(json.dumps({
                "class": class_name,
                "teacher": teacher_name,
                }))
    except OSError as e:
        raise DatabaseError(f"Error initialising database file.\n {e}")

class Gradebook:
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.database_file = open(DATABASE_DIR/class_name, "a") # Bez databáze nemá objekt smysl

    def write_database_to_disk(self):
        try:
            self.database_file.flush()
            os.fsync(self.database_file.fileno())
        except IOError as e:
            raise DatabaseError(f"Write to disk failed.\n {e}")

    def read_student(self, username: str) -> Person:
        try:
            for line in self.database_file:
                data = json.loads(line)
                
                if data["username"] == username:
                    return Person(name = data["name"],
                                  surname = data["surname"], 
                                  username = data["username"],
                                  birth_date = data["birth_date"],
                                  grades = data["grades"]
                                  )
            raise DatabaseError(f"Could not find record with username {username}")
        
        except json.JSONDecodeError as e:
            raise DataError(f"Error converting data from json\n {e}")
        except KeyError as e:
            raise DataError(f"Error reading username from record\n {e}")

    def create_record(self, Person) -> str:
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
