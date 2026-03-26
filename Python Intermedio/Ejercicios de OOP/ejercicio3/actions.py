from student import Student


def get_valid_grade(subject_name):
    while True:
        try:
            grade = float(input(f"Enter {subject_name} grade (0-100): "))

            if 0 <= grade <= 100:
                return grade
            else:
                print("Invalid grade. Must be between 0 and 100.")

        except ValueError:
            print("Invalid input. Enter a number.")


def calculate_student_average(student):
    return (
        student.spanish +
        student.english +
        student.social_studies +
        student.science
    ) / 4


def add_students(students):
    while True:
        try:
            amount = int(input("How many students do you want to add? "))
            if amount > 0:
                break
            else:
                print("Enter a number greater than 0.")
        except ValueError:
            print("Invalid input.")

    for i in range(amount):
        print(f"\nStudent #{i + 1}")

        full_name = input("Full name: ")
        section = input("Section: ")

        spanish = get_valid_grade("Spanish")
        english = get_valid_grade("English")
        social_studies = get_valid_grade("Social Studies")
        science = get_valid_grade("Science")

        student = Student(
            full_name,
            section,
            spanish,
            english,
            social_studies,
            science
        )

        students.append(student)

    print("\nStudents added successfully.")


def show_all_students(students):
    if not students:
        print("\nNo students registered.")
        return

    for i, student in enumerate(students, start=1):
        avg = calculate_student_average(student)

        print(f"\nStudent #{i}")
        print(f"Name: {student.full_name}")
        print(f"Section: {student.section}")
        print(f"Spanish: {student.spanish}")
        print(f"English: {student.english}")
        print(f"Social Studies: {student.social_studies}")
        print(f"Science: {student.science}")
        print(f"Average: {avg:.2f}")


def show_top_3_students(students):
    if not students:
        print("\nNo students registered.")
        return

    sorted_students = sorted(
        students,
        key=calculate_student_average,
        reverse=True
    )

    top_students = sorted_students[:3]

    print("\nTop 3 students:")
    for i, student in enumerate(top_students, start=1):
        avg = calculate_student_average(student)
        print(f"{i}. {student.full_name} - {avg:.2f}")


def show_average_of_all_students(students):
    if not students:
        print("\nNo students registered.")
        return

    total = 0

    for student in students:
        total += calculate_student_average(student)

    average = total / len(students)

    print(f"\nGeneral average: {average:.2f}")