from .Students import *
from .Englishstudent import *
from .Japanesestudent import *
from .Koreanstudent import *


import os
import json
from tabulate import tabulate


class ManageStudent:
    def __init__(self, filename=os.path.join("Data", "Students.json")):
        self.students = []
        self.filename = filename
        self.load_from_file()

# xu ly voi file json de nhap,xuat data(chatgpt)
    def save_to_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json_data = [
                student.display_info() for student in self.students
            ]
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for item in json_data:
                    language = item["language"].lower()
                    if language == "english":
                        def parse_score(score_str):
                            if isinstance(score_str, str) and " " in score_str:
                                parts = score_str.split()
                                try:
                                    return parts[0], float(parts[1])  # Trả về (cert, score)
                                except ValueError:
                                    return None, None  # Nếu lỗi khi chuyển đổi, trả về None
                            return None, None  # Nếu không đúng định dạng, trả về None

                        initial_cert, initial_score = parse_score(item.get("initial_Score"))
                        exam_cert, exam_score = parse_score(item.get("exam_Score"))
                        target_cert, target_score = parse_score(item.get("target_Score"))

                        student = EnglishStudent(
                            item["ID"], item["name"], item["address"], item["phone"], 
                            item["language"], 
                            initial_cert + " " + str(initial_score) if initial_cert else None, 
                            exam_cert + " " + str(exam_score) if exam_cert else None, 
                            target_cert + " " + str(target_score) if target_cert else None
                        )

                    elif language == "japanese":
                        student = JapaneseStudent(
                            item["ID"], item["name"], item["address"], item["phone"], 
                            item["language"], item.get("initial_level"), 
                            item.get("exam_level"), item.get("target_level")
                        )
                    elif language == "korean":
                        student = KoreanStudent(
                            item["ID"], item["name"], item["address"], item["phone"], 
                            item["language"], item.get("initial_level"), 
                            item.get("exam_level"), item.get("target_level")
                        )
                    else:
                        continue
                    self.students.append(student)
        except FileNotFoundError:
            self.students = []

# them hoc vien
    def add_student(self, student):
        self.students.append(student)
        self.save_to_file()
        print("student was added successfully")
   
#sua thong tin hoc vien
    def update_student(self, id_card, **kwargs):
        updated = False
        for student in self.students:
            if student.id_card == id_card:
                if "phone" in kwargs:
                    new_phone = kwargs["phone"]
                    if any(s.phone == new_phone and s.id_card != id_card for s in self.students):
                        print(f"Error: Phone number '{new_phone}' already exists. Update rejected.")
                        return False
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                        updated = True
                    else:
                        print(f"Warning: Field '{key}' does not exist and will be ignored.")
                if updated:
                    self.save_to_file()
                    return True
        return False

#xoa hoc vien
    def delete_student(self, id_card):

        if(self.students == []):
            print("list empty!")
            return
        
        check_exist = False

        for student in self.students:
            if student.id_card == id_card :
                self.students.remove(student)
                print("student deleted sucessful")
                check_exist = True
                break
        
        if(check_exist == False): print("no exist this student_id")

        self.save_to_file()

# in ra data
    def display_all(self):
        
        if(self.students == []):
            print("list empty!")
            return
        
        headers = list(self.students[0].display_info().keys())
        table = [list(student.display_info().values()) for student in self.students]
        print(tabulate(table, headers=headers, tablefmt="grid"))


#tim kiem hoc vien
    def find_student(self, field, value):
        for student in self.students:
            if (field == "ID" and student.id_card == value) or (field == "phone" and student.phone == value):
                return student.display_info()
        return "Student not found"

# in danh sach theo ngon ngu
    def display_by_language(self, language):
        list_stu = [student for student in self.students if student.language == language]
        if(list_stu == []): return []
        headers = list(self.students[0].display_info().keys())
        table = [list(student.display_info().values()) for student in self.students if student.language == language]
        print(tabulate(table, headers=headers, tablefmt="grid"))    
        return True
    
# tinh ti le dat muc tieu
    def calculate_success_rate(self):
        total = len(self.students)
        list_stu = []
        if total == 0:
            return 0
        success = 0
        for student in self.students:
            if isinstance(student, EnglishStudent):
                if student.check_target() == True:
                    success += 1
                    list_stu.append(student)
            elif isinstance(student, (JapaneseStudent, KoreanStudent)):
                if student.check_target() == True:
                    success += 1
                    list_stu.append(student)
        headers = list(self.students[0].display_info().keys())
        table = [list(student.display_info().values()) for student in list_stu]
        print(tabulate(table, headers=headers, tablefmt="grid"))
        return (success / total) * 100
    
# thong ke danh sach bi fail
    def static_fail_student(self):
        result = []
        for student in self.students:
            if isinstance(student, EnglishStudent):
                if student.check_target() == False:
                    result.append(student)
            elif isinstance(student, (JapaneseStudent, KoreanStudent)):
                if student.check_target() == False:
                    result.append(student)
        
        if result == [] :
            print ("no exist student failed")
            return
        
        headers = list(self.students[0].display_info().keys())
        table = [list(student.display_info().values()) for student in result]
        print(tabulate(table, headers=headers, tablefmt="grid")) 
       

# sap xep danh sach hoc vien
    def sort_students(self):
        language = input("Enter language to sort (English, Japanese, Korean): ").lower()
        while language not in ["english", "japanese", "korean"]:
            language = input("Enter language to sort (English, Japanese, Korean): ").lower()

        if language == "english":
            by = input("Enter type score: \n1. Initial Score \n2. Target Score\nChoose (1 or 2): ")
            while by not in ['1', '2']:
                by = input("Allow enter 1 or 2: \n1. Initial Score \n2. Target Score\nChoose (1 or 2): ")
            by = "initial_score" if by == "1" else "target_score"
        else:
            by = input("Enter type score: \n1. Initial Level \n2. Target Level\nChoose (1 or 2): ")
            while by not in ['1', '2']:
                by = input("Allow enter 1 or 2: \n1. Initial Level \n2. Target Level\nChoose (1 or 2): ")
            by = "initial_level" if by == "1" else "target_level"

        descending = input("Sort descending? (y/n): ").lower()
        while descending not in ["y", "n"]:
            descending = input("Allow y/n: ").lower()
        descending = descending == "y"

        # Lọc danh sách theo ngôn ngữ
        filtered_students = [s for s in self.students if s.language.lower() == language]

        # Kiểm tra nếu danh sách rỗng
        if not filtered_students:
            print("No students found for the selected language.")
            return

        # Hàm lấy giá trị điểm phù hợp
        def get_sort_key(student):
            value = getattr(student, by)
            return student.parse_score(value)

        # Sắp xếp danh sách
        sorted_students = sorted(filtered_students, key=get_sort_key, reverse=descending)

        # Hiển thị kết quả
        headers = list(sorted_students[0].display_info().keys())
        table = [list(student.display_info().values()) for student in sorted_students]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    

#nguoi hoc xuat sac nhat(lay top 5(min))
    def top_students(self): # sort to exam_score or exam_level
        language = input("Enter language to filter top students (English, Japanese, Korean): ").lower()
        while language not in ["english", "japanese", "korean"]:
            language = input("Invalid input. Enter language to filter top students (English, Japanese, Korean): ").lower()
        
        filtered_students = [s for s in self.students if s.language.lower() == language]
        
        if not filtered_students:
            print("No students found for the selected language.")
            return

        sorted_students = sorted(
            filtered_students,
            key=lambda s: (-s.parse_score(s.exam_score if hasattr(s, 'exam_score') else s.exam_level), s.name)
        )
        
        top_5 = []
        last_score = None
        for student in sorted_students:
            score = student.parse_score(student.exam_score if hasattr(student, 'exam_score') else student.exam_level)
            if len(top_5) < 5 or (last_score is not None and score == last_score):
                top_5.append(student)
                last_score = score
            else:
                break
        
        headers = list(top_5[0].display_info().keys())
        table = [list(student.display_info().values()) for student in top_5]
        print(tabulate(table, headers=headers, tablefmt="grid"))
        
# phuong thuc phu   
    def check_id_card(self,id_card):
        check = False
        for stu in self.students:
            if(stu.id_card == id_card):
                check = True
                break
        return check
    
    def check_phone(self,phone):
        check = False
        for stu in self.students:
            if(stu.phone == phone):
                check = True
                break
        return check
