from Modules.Manage_student import ManageStudent
from Modules.Students import *
from Modules.Englishstudent import *
from Modules.Japanesestudent import *
from Modules.Koreanstudent import *

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def print_menu():
    print("\nMenu:")
    print("1. Add Student")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. Find Student")
    print("5. Display list students by Language")
    print("6. Calculate Success Rate")
    print("7. Sort Students")
    print("8. Top Students")
    print("9. List students fail target")
    print("10. exit program")
    print("11. display ALL")
    print("12. help")

def check_input_eng(cert_type):

    if cert_type == "1":
        cert = "IELTS"
        valid_range = [x * 0.5 for x in range(2, 19)]  # Danh sách từ 1.0 đến 9.0 với bước 0.5
    else:
        cert = "TOEFL"
        valid_range = list(range(1, 121))  # Danh sách từ 1 đến 120 với bước 1

    while True:
        try:
            score = float(input(f"Enter {cert} score ({valid_range[0]}-{valid_range[-1]}): "))
            if score in valid_range:
                return f"{cert} {score}"
            else:
                print(f"Invalid score! Must be in range {valid_range[0]}-{valid_range[-1]}.")
        except ValueError:
            print("Invalid input! Please enter a numerical value.")
        
        ques = input("Do you want to try again? (y/n): ").lower()
        while ques not in ["y", "n"]:
            ques = input("Invalid choice! Press y (yes) or n (no): ").lower()
        if ques == "n":
            return False  

def check_in_empty(str_input):
    while(str_input.strip() == ""):
        str_input = input(f"Enter again,not allow value none: ")
    return str_input
    
def main():
    manager = ManageStudent()

    print_menu()

    while True:

        choice = input("Enter your choice(press 12(help) or 10(exit), e.g ...): ")

# chức năng thêm sinh vien
        if choice == "1":
            id_card = input("Enter ID Card: ")
            while(manager.check_id_card(id_card) or id_card.strip() == ""):
                id_card = check_in_empty(id_card)
                if(manager.check_id_card(id_card)):
                    id_card = input("Enter ID Card again, this id has existed: ")

            name = input("Enter Name: "); name = check_in_empty(name)
            address = input("Enter Address: "); address = check_in_empty(address)
            phone = input("Enter Phone: ")
            while(manager.check_phone(phone) == True or phone.strip() == ""):
                phone = check_in_empty(phone)
                if(manager.check_phone(phone)):
                    phone = input("Enter Phone again, phone number has existed: ")

            while True:
                language = input("Enter Language (English/Japanese/Korean): ")
                if language.lower() in ["english", "japanese", "korean"]:
                    break
                else:
                    print("Invalid language! Please enter English, Japanese, or Korean.")

            if language.lower() == "english":
                cert_type = input("Choose certificate (1: IELTS, 2: TOEFL): ")
                while cert_type not in ["1", "2"]:
                    cert_type = input("Invalid choice! Choose 1 for IELTS or 2 for TOEFL: ")
                
                print("Enter Initial Score: ")
                initial_score = check_input_eng(cert_type)
                if(initial_score == False): continue

                print("Enter Exam Score: ")
                exam_score = check_input_eng(cert_type)
                if(exam_score == False): continue

                print("Enter target Score: ")
                target_score = check_input_eng(cert_type)
                if(target_score == False): continue
                
                student = EnglishStudent(id_card, name, address, phone, language, initial_score, exam_score, target_score)

            elif language.lower() == "japanese":
                list_level = ["n1","n2","n3","n4","n5"]
                initial_level = input("Enter Initial Level (e.g., n5): ").lower()
                while (initial_level not in list_level):
                    initial_level = input("allow value n1->n5, try again: ").lower()
                exam_level = input("Enter Exam Level: ").lower()
                while (exam_level not in list_level):
                    exam_level = input("allow value n1->n5, try again: ").lower()
                target_level = input("Enter Target Level: ").lower()
                while (target_level not in list_level):
                    target_level = input("allow value n1->n5, try again: ").lower()
                student = JapaneseStudent(id_card, name, address, phone, language, initial_level, exam_level, target_level)

            elif language.lower() == "korean":
                list_level = ["so cap", "trung cap", "cao cap"]
                initial_level = input("Enter Initial Level (e.g., so cap): ")
                while (initial_level not in list_level):
                    initial_level = input("Level include <'so cap', 'trung cap', 'cao cap'>, try again: ")
                exam_level = input("Enter Exam Level: ")
                while (exam_level not in list_level):
                    exam_level = input("Level include <'so cap', 'trung cap', 'cao cap'>, try again: ")
                target_level = input("Enter Target Level: ")
                while (target_level not in list_level):
                    target_level = input("Level include <'so cap', 'trung cap', 'cao cap'>, try again: ")
                student = KoreanStudent(id_card, name, address, phone, language, initial_level, exam_level, target_level)

            else:
                print("Invalid language!")
                continue

            manager.add_student(student)

# chức năng sửa thông tin theo id
        elif choice == "2":
            while True:
                id_card = input("Enter ID Card of the student to update: ")
                check = manager.check_id_card(id_card)
                if check:
                    break
                print("Student not found. Please try again.")
            
            update_fields = {}
            while True:
                print("You can update the following fields: name, address, phone, language, initial_level, test_score, target_level")
                field = input("Enter the field to update (or enter 'done' to finish): ").lower()
                if field == "done":
                    break
                if field not in ["name", "address", "phone", "language", "initial_level", "test_score", "target_level"]:
                    print(f"Warning: Field '{field}' does not exist and will be ignored.")
                    continue
                value = input(f"Enter the new value for {field}: ")
                update_fields[field] = value
            if manager.update_student(id_card, **update_fields):
                print("Student updated successfully.")
            else:
                print("No object updated")

# chức năng xóa sinh viên theo id
        elif choice == "3":
            id_card = input("Enter ID Card of the student to delete: ")
            manager.delete_student(id_card)

# chức năng tìm kiếm sinh viên với id hoặc sđt
        elif choice == "4":
            field = input("Enter the field to search by (ID or phone): ")
            while field not in ["ID", "phone"]:
                field = input("allow find by ID or phone: ")
            value = input("Enter the value to search for: ")
            results = manager.find_student(field, value)
            print(results)

# chức năng in danh sách sinh viên theo ngôn ngữ đang học
        elif choice == "5":
            language = input("Enter language to display students (English/Japanese/Korean): ").lower()
            while language not in ['english', 'japanese', 'korean']:
                language = input("allow in (English/Japanese/Korean): ").lower()
            students = manager.display_by_language(language)
            if students == []: 
                print(f"no student studying {language}")
                continue

# chức năng tính tỉ lệ sinh viên đạt mục tiêu 
        elif choice == "6":
            print("list students pass target: ")
            success_rate = manager.calculate_success_rate()
            print(f"Success rate: {success_rate:.2f}%")

# chức năng sắp xếp lại danh sách sinh viên
        elif choice == "7":
            manager.sort_students()
# chức năng đưa ra top các sinh viên có bài kiểm tra cao nhất
        elif choice == "8":
            manager.top_students() # sort to exam_score

# chức năng in danh sách các sinh viên không đạt mục tiêu
        elif choice == "9":
            print("list students fail target: ")
            manager.static_fail_student()

# thoát chương trình
        elif choice == "10":
            break

# in ra danh sách tất cả các sinh viên từ database
        elif choice == "11":
            manager.display_all()

# help
        elif choice == "12":
            print_menu()

        else:
            print("Functionality not implemented yet!")

if __name__ == "__main__":
    main()
