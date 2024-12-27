from database import Gradebook as db
from database import Person 
from database import make_gradebook_file
from database import DatabaseError as DatabaseError

make_gradebook_file("Adam", "1.A", "database/1.A")

Adam = Person("Adam", "Jirásek", "2.9.2004", {"ZPRO": [1, 2, 3, 4, 5], "MECH": [2.5, 2]})

David = Person("David", "Žůrek", "idk", {"ZPRO": [1, 1, 1, 1], "MECH": [4, 4]})

book = db("database/1.A")
book.create_record(Adam)
book.create_record(David)
book.write_database_to_disk()

Adam.birth_date = "1.1.1900"
book.modify_record(Adam)
book.write_database_to_disk()
book.show_table()
