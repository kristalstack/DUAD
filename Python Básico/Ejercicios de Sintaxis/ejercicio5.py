# Grade calculator

print("Enter the number of grades:")
total_grades = int(input())

grade_counter = 1
approved_count = 0
failed_count = 0

approved_sum = 0
failed_sum = 0
total_average = 0

while grade_counter <= total_grades:

    print("Enter grade number", grade_counter)
    current_grade = float(input())

    if current_grade < 70:
        failed_count += 1
        failed_sum += current_grade
    else:
        approved_count += 1
        approved_sum += current_grade

    total_average += current_grade / total_grades

    grade_counter += 1


# Avoid division by zero
if failed_count > 0:
    failed_average = failed_sum / failed_count
else:
    failed_average = 0

if approved_count > 0:
    approved_average = approved_sum / approved_count
else:
    approved_average = 0


print("\nApproved grades:", approved_count)
print("Average of approved grades:", approved_average)

print("\nFailed grades:", failed_count)
print("Average of failed grades:", failed_average)

print("\nTotal average:", total_average)