students = []

"""function add_student taking str with name using
input and adding it to list students[]"""

def add_student():
    studentname = input("Enter student name: ").strip()

    for student in students:

        if student["name"].lower() == studentname.lower():  # Checking for the possible existence of a student
            print("Student already exists.")
            return

    students.append({"name": studentname, "grades": []})  # dict for students
    print(f"Student '{studentname}' added successfully.")

"""function add_grades add grades to students"""

def add_grades():
    studentname = input("Enter student name: ").strip()

    for student in students:

        if student["name"].lower() == studentname.lower():  # find student

            while True: # infinite loop
                grade_input = input("Enter a grade (or 'done' to finish): ").strip()

                if grade_input.lower() == "done": # loop termination condition
                    break

                # try-catch block to handle potential input errors
                try:
                    grade = int(grade_input)

                    if 0 <= grade <= 100:
                        student["grades"].append(grade)

                    else:
                        print("Grade must be between 0 and 100.")

                except ValueError:
                    print("Invalid input. Please enter a number.")

            return

    # print (grade)
    print("Student not found.")

"""Function to generate a report on students.
Calculates averages, max, min, and overall average.
Handles cases where a student has no grades (ZeroDivisionError)."""
def show_report():
    if not students:
        print("No students added yet.")
        return

    sum_ = 0
    count = 0
    max_avg = None
    min_avg = None

    print("--- Student Report ---")

    for student in students:
        grades = student["grades"]
        try:

            avg = sum(grades) / len(grades) # Calculate average grade
            print(f"{student['name']}'s average grade is {avg:.1f}.")

            sum_ += avg
            count += 1

            # Update max and min
            max_avg = avg if max_avg is None else max(max_avg, avg)

            min_avg = avg if min_avg is None else min(min_avg, avg)
        except ZeroDivisionError:
            print(f"{student['name']}'s average grade is N/A.")

    if count > 0:
        overall_avg = sum_ / count
        # Print summary statistics
        print(f"""-----------------------------
        Max Average: {max_avg:.1f}
        Min Average: {min_avg:.1f}
        Overall Average: {overall_avg:.1f}""")
    else:
        print("No grades available to calculate averages.")

"""  Function to find the student with the highest average grade.
     Filters students with grades and finds the max by average."""
def top_student():
    valid_students = [s for s in students if s["grades"]] # Only students with grades

    if not valid_students:
        print("No students with grades to evaluate.")
        return
    # Find the student with the highest average (using lambda for key)
    best_student = max(valid_students, key=lambda s: sum(s["grades"]) / len(s["grades"]))
    top_avg = sum(best_student["grades"]) / len(best_student["grades"])
    print(f"The student with the highest average is {best_student['name']} with a grade of {top_avg:.1f}.")

# Main function of the program - menu loop for user interaction.
def main():
    while True:
        print("""\n--- Student Grade Analyzer ---
        1. Add a new student
        2. Add grades for a student
        3. Generate a full report
        4. Find the top student
        5. Exit program""")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                add_student()
            elif choice == 2:
                add_grades()
            elif choice == 3:
                show_report()
            elif choice == 4:
                top_student()
            elif choice == 5:
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please select from 1 to 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

"""Check if the script is run directly (standard Python idiom).
   If so, run main(). This prevents code execution when the module is imported."""
if __name__ == "__main__":
    main()