import database as db
while True:
    action = int(input(
        '''What would you like to do
        1) create new gradebook
        2) read gradebook
        3) exit

        :'''))
    match action:
        case 1:
            try:
                name, class_name, file_path = map(str, input("Give me teacher's name, class name and path to new file separated by comma: ").split(","))
                db.make_gradebook_file(name, class_name, file_path)
            except Exception as e:
                print(f"Following error ocured:\n {e}")
                continue
        case 3:
            break
        case 2:
            try:
                gradebook = db.Gradebook(str(input("Give me path to gradebook file: ")))
            except Exception as e:
                print(f"Following error ocured:\n {e}")
                continue

            while True:
                try:
                    action_on_gradebook = int(input('''What would you like to do:
                1) Show data in gradebook as table
                2) Make a new record
                3) Modify existing record
                4) Analyze student's grades
                5) Delete record
                6) exit

                : '''))
                    match action_on_gradebook:
                        case 1:
                            gradebook.show_table()
                        case 2:
                            name, surname, birth_date = map(str, input("Give me name, surname and birth date separated by comma: ").split(","))
                            grades = {subject: [] for subject in list(map(str, input("Give me subjects, separated by comma: ").split(",")))}
                            for subject in grades:
                               print(f"{subject}:{grades[subject]}")
                               grades.update({subject: [char for char in list(map(str, input(f"Give me updated list of {subject} grades, each separated by comma : ").split(","))) if char != '']})
                            gradebook.create_record(db.Person(name, surname, birth_date, grades))
                            gradebook.write_database_to_disk()

                        case 3:
                            student = gradebook.read_record(str(input("Give me username: ")))
                            for subject in student.grades:
                                print(f"{subject}:{student.grades[subject]}")
                                student.grades.update({subject: [char for char in list(map(str, input(f"Give me updated list of {subject} grades, each separated by comma : ").split(","))) if char not in ('','\n')]})
                            print(student.grades)
                            gradebook.modify_record(student)
                            gradebook.write_database_to_disk()
                        case 4:
                            print(gradebook.read_record(str(input("Give me username: "))).arithmetic_mean(str(input("Give me subject: "))))
                        case 5:
                            print("Waiting to be implemented")
                        case 6:
                            break

                except Exception as e:
                    print(f"Following error ocured in inner loop:\n {e}")
                    continue

