from .Students import Student


class EnglishStudent(Student):
    def __init__(self, id_card, name, address, phone, language, initial_score, exam_score, target_score):
        super().__init__(id_card, name, address, phone, language)
        self.initial_score = initial_score
        self.exam_score = exam_score
        self.target_score = target_score

    def display_info(self):
        parent_info = super().display_info()
        parent_info.update({
            "initial_Score": self.initial_score,
            "exam_Score": self.exam_score,
            "target_Score": self.target_score,
        })
        return parent_info
    
    def check_target(self):

        import re

        score_exam  = float(''.join(re.findall(r'\d+\.\d+|\d+', self.exam_score)))
        score_target = float(''.join(re.findall(r'\d+\.\d+|\d+', self.target_score)))

        if(score_exam < score_target):

            return False

        return True
    
    def parse_score(self, score_str):
        cert, score = score_str.split()
        score = float(score)
        if "TOEFL" in cert:
            score = score * 9.0 / 120.0  # Quy đổi TOEFL về IELTS
        return score
