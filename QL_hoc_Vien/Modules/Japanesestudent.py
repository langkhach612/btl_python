from .Students import Student

class JapaneseStudent(Student):
    
    LEVELS = {"n5": 1, "n4": 2, "n3": 3, "n2": 4, "n1": 5}

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

        import re

        score_exam  = int(''.join(re.findall(r'\d+\.\d+|\d+', self.exam_level)))
        score_target = int(''.join(re.findall(r'\d+\.\d+|\d+', self.target_level)))

        if(score_exam >  score_target): #N5min

            return False

        return True

    def parse_score(self, level):
        return self.LEVELS[level]