from typing import List, Dict, Union

# Type aliases
Grade = int
StudentDict = Dict[str, Union[str, List[Grade]]]
StudentList = List[StudentDict]
Average = Union[float, str]

def add_new_student(students: StudentList) -> None:
    """
    Add a new student to the students list.

    Args:
        students (list): List of student dictionaries

    Raises:
        TypeError: If 'students' is not a list

    Prompts user for student name and adds it to the list if
    it doesn't already exist.
    Each student is represented as a dictionary with 'name'
    and 'grades' keys.
    If student name is None or student already exists,
    an error message is printed.
    """
    if not isinstance(students, list):
        raise TypeError("Students must be a list")

    name: str = input("Enter student name: ").strip()

    if not name:
        print("Error: student name cannot be empty.")
        return

    # Check if student already exists
    name_lower: str = name.lower()
    if any(student["name"].lower() == name_lower
           for student in students):
        print(f"Student '{name}' already exists.")
        return

    # Add new student
    new_student: StudentDict = {"name": name, "grades": []}
    students.append(new_student)


def add_grades_for_student(students: StudentList) -> None:
    """
    Add grades for a student.

    Args:
        students (list): List of student dictionaries

    Raises:
        TypeError: If 'students' is not a list

    Prompts user for student name and then allows
    entering multiple grades.
    If student is not found in the list, an error message is printed.
    Grades should be integers between 0 and 100, otherwise
    an error message is printed.
    """
    if not isinstance(students, list):
        raise TypeError("Students must be a list")

    if not students:
        print("No students available. Please add students first.")
        return

    name: str = input("Enter student name: ").strip()

    if not name:
        print("Error: Student name cannot be empty.")
        return

    # Find the student
    name_lower: str = name.lower()
    student_found: StudentDict = next(
        (student for student in students if
         student["name"].lower() == name_lower),
        {}
    )

    if not student_found:
        print(f"Student '{name}' not found.")
        return

    # Prompt user for grades
    while True:
        grade_input: str = (
            input("Enter a grade (or 'done' to finish): ")
            .strip()
            .lower()
        )

        if grade_input == 'done':
            break

        try:
            grade: Grade = int(grade_input)
            if 0 <= grade <= 100:
                student_found["grades"].append(grade)
            else:
                print("Error: Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100, "
                  "or 'done' to finish.")


def calculate_average(grades: List[Grade]) -> Average:
    """
    Calculate the average of a list of grades.

    Args:
        grades (list): List of numerical grades

    Returns:
        float or str: Average grade as float, or "N/A" if
        no grades added for the student.
    """
    if not grades:
        return "N/A"

    try:
        return sum(grades) / len(grades)
    except ZeroDivisionError:
        return "N/A"


def generate_report(students: StudentList) -> str:
    """
    Generate a formatted report of all students as a string.

    Args:
        students (list): List of student dictionaries

    Returns:
        str: Formatted report string
    """
    if not students:
        return "No students available."

    report_lines: List[str] = ["--- Student Report ---"]
    valid_averages: List[float] = []

    # Calculate average grade for each student
    for student in students:
        avg: Average = calculate_average(student["grades"])

        if isinstance(avg, float):
            report_lines.append(f"{student['name']}'s average grade "
                                f"is {avg:.1f}.")
            valid_averages.append(avg)
        else: # "N/A"
            report_lines.append(f"{student['name']}'s average grade is N/A.")

    # Statistics block
    report_lines.append("----------------------")
    if not valid_averages:
        report_lines.append("No students have grades to "
                            "calculate statistics.")
        return "\n".join(report_lines)

    max_avg: float = max(valid_averages)
    min_avg: float = min(valid_averages)
    overall_avg: float = sum(valid_averages) / len(valid_averages)

    report_lines.append(f"Max Average: {max_avg:.1f}")
    report_lines.append(f"Min Average: {min_avg:.1f}")
    report_lines.append(f"Overall Average: {overall_avg:.1f}")

    return "\n".join(report_lines)


def show_report(students: StudentList) -> None:
    """
    Display a report about all students.

    Args:
        students (list): List of student dictionaries

    Raises:
        TypeError: If 'students' is not a list
    """
    if not isinstance(students, list):
        raise TypeError("Students must be a list")

    report: str = generate_report(students)
    print(report)


def find_top_performer(students: StudentList) -> None:
    """
    Find and display the student with the highest average grade.

    Args:
        students (list): List of student dictionaries

    Raises:
        TypeError: If 'students' is not a list
    """
    if not isinstance(students, list):
        raise TypeError("Students must be a list")

    if not students:
        print("No students available.")
        return

    # Filter students who have grades
    students_with_grades: StudentList = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No students have grades to determine top performer.")
        return

    try:
        # Find student with the highest average
        top_student: StudentDict = max(
            students_with_grades,
            key=lambda s: calculate_average(s["grades"])
        )

        top_avg: float = calculate_average(top_student["grades"])
        print(f"The student with the highest average is "
              f"{top_student['name']} with a grade of {top_avg:.1f}.")

    except Exception as e:
        print(f"Error finding top performer: {e}")


def main():
    """
    Main function to run the Student Grade Analyzer program.
    This function initializes an empty list for
    student data and displays a menu for the user to
    interact with the program.
    It handles all user menu selections.
    """
    students: StudentList = []

    application_menu: str = (
        "--- Student Grade Analyzer ---\n"
        "1. Add a new student\n"
        "2. Add grades for a student\n"
        "3. Generate a full report\n"
        "4. Find the top student\n"
        "5. Exit program"
    )

    print(application_menu)

    while True:
        try:
            choice: str = input("Enter your choice: ").strip()

            if not choice:
                print("Please enter your choice.")
                continue

            if choice == "1":
                add_new_student(students)
            elif choice == "2":
                add_grades_for_student(students)
            elif choice == "3":
                show_report(students)
            elif choice == "4":
                find_top_performer(students)
            elif choice == "5":
                print("\nExiting program.")
                break
            else:
                print("Invalid choice. "
                      "Please enter a number between 1 and 5.")

            print(f"\n{application_menu}")

        except KeyboardInterrupt:
            print("\n\nExiting program.")
            break
        except Exception as e:
            print(f"An unexpected error detected: {e}")


if __name__ == "__main__":
    main()