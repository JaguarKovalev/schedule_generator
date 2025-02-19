class SchoolSchedule:
    def __init__(self, classes, teachers, days=5):
        self.classes = classes
        self.teachers = teachers
        self.days = days  # Установим 5 дней для расписания
        self.schedule = defaultdict(lambda: defaultdict(list))
        self.teacher_availability = defaultdict(
            lambda: defaultdict(lambda: [True] * 6)
        )  # Занятость учителей

    def generate_schedule(self):
        for cls in self.classes:
            for subject_name, hours in cls.subjects_hours.items():
                available_teachers = [
                    t
                    for t in self.teachers
                    if subject_name in [s.name for s in t.subjects]
                ]
                for _ in range(hours):
                    day = random.randint(1, self.days)
                    lesson_time = len(
                        self.schedule[cls.name][day]
                    )  # Получаем текущее количество уроков в день
                    if lesson_time < 6:  # Максимум 6 уроков в день
                        random.shuffle(
                            available_teachers
                        )  # Перемешиваем список учителей
                        for teacher in available_teachers:
                            if self.teacher_availability[teacher.name][day][
                                lesson_time
                            ]:  # Проверяем доступность учителя
                                # Назначаем урок
                                self.schedule[cls.name][day].append(
                                    (subject_name, teacher.name)
                                )
                                self.teacher_availability[teacher.name][day][
                                    lesson_time
                                ] = False  # Устанавливаем учителя как занятого
                                break  # Выходим из цикла после назначения урока

    def print_schedule(self):
        schedule_str = ""
        for cls_name, days in self.schedule.items():
            schedule_str += f"Расписание для класса {cls_name}:\n"
            for day in sorted(days.keys()):  # Сортируем дни перед выводом
                lessons = days[day]
                schedule_str += f"  День {day}:\n"
                for i, (subject, teacher) in enumerate(lessons, start=1):
                    schedule_str += f"    Урок {i}: {subject} - {teacher}\n"
            schedule_str += "\n"
        return schedule_str
