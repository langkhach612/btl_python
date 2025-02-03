from .Students import Student

class KoreanStudent(Student):

    LEVELS = {"so cap": 1, "trung cap": 2, "cao cap": 3}

    def __init__(self, id_card, name, address, phone, language, initial_level, exam_level, target_level):
        super().__init__(id_card, name, address, phone, language)
        self.initial_level = initial_level
        self.exam_level = exam_level
        self.target_level = target_level

    def display_info(self):
        parent_info = super().display_info()
        parent_info.update({
            "initial_level": self.initial_level,
            "exam_level": self.exam_level,
            "target_level": self.target_level,
        })
        return parent_info
    
    def check_target(self):
        if(self.exam_level == "so cap"):
            if(self.target_level != "so cap"):
                return False
        elif(self.exam_level == "trung cap"):
            if(self.target_level == "cao cap"):
                return False
            else:
                return True
        else:
            return True
    
    def parse_score(self, level):
        return self.LEVELS.get(level, 0)