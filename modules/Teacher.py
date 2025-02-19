class Teacher:
    def __init__(self, name):
        self.name = name
        self.subjects = []  # Список предметов, которые ведет учитель

    def assign_subject(self, subject):
        self.subjects.append(subject)  # Добавляем предмет в список
