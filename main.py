from db_manager import (
    create_tables, add_student, add_grade,
    view_student, show_all_averages,
    subject_wise_topper, subject_average
)

def main():
    create_tables()

    while True:
        print("\n===== Student Performance Tracker (with SQL) =====")
        print("1. Add Student")
        print("2. Add Grades")
        print("3. View Student Details")
        print("4. Show Class Averages")
        print("5. Show Subject-wise Topper 🏆")
        print("6. Show Subject-wise Average 📊")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            name = input("Enter student name: ")
            roll = input("Enter roll number: ")
            add_student(name, roll)

        elif choice == '2':
            roll = input("Enter roll number: ")
            while True:
                subject = input("Enter subject (or type 'done' to stop): ")
                if subject.lower() == 'done':
                    break
                try:
                    grade = float(input(f"Enter grade for {subject}: "))
                    if 0 <= grade <= 100:
                        add_grade(roll, subject, grade)
                    else:
                        print("⚠ Grade must be between 0 and 100")
                except ValueError:
                    print("⚠ Invalid grade")

        elif choice == '3':
            roll = input("Enter roll number: ")
            view_student(roll)

        elif choice == '4':
            show_all_averages()

        elif choice == '5':
            subject = input("Enter subject name: ")
            subject_wise_topper(subject)

        elif choice == '6':
            subject = input("Enter subject name: ")
            subject_average(subject)

        elif choice == '7':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()