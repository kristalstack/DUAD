import csv
import os
from student import Student


def export_to_csv(students, filename="students.csv"):
    if not students:
        print("\nThere are no students to export.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "full_name",
            "section",
            "spanish",
            "english",
            "social_studies",
            "science"
        ])

        for student in students:
            writer.writerow([
                student.full_name,
                student.section,
                student.spanish,
                student.english,
                student.social_studies,
                student.science
            ])

    print(f"\nData exported successfully to {filename}.")


def import_from_csv(filename="students.csv"):
    if not os.path.exists(filename):
        print("\nNo previously exported file was found.")
        return []

    students = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student = Student(
                row["full_name"],
                row["section"],
                float(row["spanish"]),
                float(row["english"]),
                float(row["social_studies"]),
                float(row["science"])
            )

            students.append(student)

    print(f"\nData imported successfully from {filename}.")
    return students