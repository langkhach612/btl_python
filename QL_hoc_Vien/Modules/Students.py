class Student:
    def __init__(self, id_card, name, address, phone, language):
        self.id_card = id_card
        self.name = name
        self.address = address
        self.phone = phone
        self.language = language

    def display_info(self):
        return {
            "ID": self.id_card,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "language": self.language,
        }
