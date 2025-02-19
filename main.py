import random
import tkinter as tk
from collections import defaultdict
from tkinter import messagebox

from modules.Class import Class
from modules.SchoolSchedule import SchoolSchedule
from modules.Subject import Subject
from modules.Teacher import Teacher

# Глобальные переменные для хранения данных
subjects = {}
teachers = []
classes = []


def input_subjects_gui():
    def add_subject():
        subject_name = entry_subject.get()
        if subject_name:
            subjects[subject_name] = Subject(subject_name)
            listbox_subjects.insert(tk.END, subject_name)
            entry_subject.delete(0, tk.END)

    def finish_subjects():
        window_subjects.destroy()

    window_subjects = tk.Toplevel(root)
    window_subjects.title("Ввод предметов")

    tk.Label(window_subjects, text="Название предмета:").pack()
    entry_subject = tk.Entry(window_subjects)
    entry_subject.pack()

    tk.Button(window_subjects, text="Добавить", command=add_subject).pack()
    tk.Button(window_subjects, text="Завершить", command=finish_subjects).pack()

    listbox_subjects = tk.Listbox(window_subjects)
    listbox_subjects.pack()


def input_teachers_gui():
    def add_teacher():
        teacher_name = entry_teacher.get()
        if teacher_name:
            teachers.append(Teacher(teacher_name))
            listbox_teachers.insert(tk.END, teacher_name)
            entry_teacher.delete(0, tk.END)

    def assign_subjects_to_teacher():
        selected_teacher_name = listbox_teachers.get(tk.ACTIVE)
        if selected_teacher_name:
            selected_teacher = next(
                t for t in teachers if t.name == selected_teacher_name
            )
            subject_names = listbox_subjects.curselection()
            for idx in subject_names:
                subject_name = listbox_subjects.get(idx)
                selected_teacher.assign_subject(subjects[subject_name])

            messagebox.showinfo(
                "Учитель назначен",
                f"Предметы назначены учителю {selected_teacher_name}",
            )

    def finish_teachers():
        window_teachers.destroy()

    window_teachers = tk.Toplevel(root)
    window_teachers.title("Ввод учителей и назначение предметов")

    tk.Label(window_teachers, text="ФИО учителя:").pack()
    entry_teacher = tk.Entry(window_teachers)
    entry_teacher.pack()

    tk.Button(window_teachers, text="Добавить учителя", command=add_teacher).pack()

    # Список для выбора предметов
    tk.Label(window_teachers, text="Выберите предметы для учителя:").pack()
    listbox_subjects = tk.Listbox(window_teachers, selectmode=tk.MULTIPLE)
    for subject_name in subjects:
        listbox_subjects.insert(tk.END, subject_name)
    listbox_subjects.pack()

    # Список для отображения учителей
    tk.Label(window_teachers, text="Учителя:").pack()
    listbox_teachers = tk.Listbox(window_teachers)
    listbox_teachers.pack()

    tk.Button(
        window_teachers, text="Назначить предметы", command=assign_subjects_to_teacher
    ).pack()
    tk.Button(window_teachers, text="Завершить", command=finish_teachers).pack()


def input_classes_gui():
    def add_class():
        class_name = entry_class_name.get()
        if class_name:
            new_class = Class(class_name)
            classes.append(new_class)
            listbox_classes.insert(tk.END, class_name)
            entry_class_name.delete(0, tk.END)

    def finish_classes():
        window_classes.destroy()

    window_classes = tk.Toplevel(root)
    window_classes.title("Ввод классов")

    tk.Label(window_classes, text="Название класса:").pack()
    entry_class_name = tk.Entry(window_classes)
    entry_class_name.pack()

    tk.Button(window_classes, text="Добавить класс", command=add_class).pack()
    tk.Button(window_classes, text="Завершить", command=finish_classes).pack()

    listbox_classes = tk.Listbox(window_classes)
    listbox_classes.pack()


def distribute_hours_gui():
    def save_hours():
        # Обновляем количество часов для каждого класса и предмета
        for cls in classes:
            for subject_name, entry in cls.subjects_hours.items():
                hours = entry.get()
                if hours.isdigit():
                    cls.subjects_hours[subject_name] = int(hours)
                else:
                    cls.subjects_hours[subject_name] = 0  # Если не введено, ставим 0

        messagebox.showinfo("Сохранено", "Часы для всех классов сохранены.")

    if not classes:
        messagebox.showwarning(
            "Ошибка", "Нет добавленных классов. Пожалуйста, добавьте классы."
        )
        return

    window_hours = tk.Toplevel(root)
    window_hours.title("Часы для классов")

    for cls in classes:
        tk.Label(window_hours, text=f"Класс {cls.name}:").pack()
        cls.subjects_hours = {
            subject.name: tk.Entry(window_hours) for subject in subjects.values()
        }
        for subject_name, entry in cls.subjects_hours.items():
            tk.Label(window_hours, text=f"{subject_name}:").pack()
            entry.pack()

    tk.Button(
        window_hours, text="Сохранить часы для всех классов", command=save_hours
    ).pack()


def generate_schedule_gui():
    # Генерация расписания
    school_schedule = SchoolSchedule(classes, teachers, days=5)
    school_schedule.generate_schedule()
    schedule_text = school_schedule.print_schedule()

    if not schedule_text.strip():
        schedule_text = (
            "Расписание не было сгенерировано. Пожалуйста, проверьте введенные данные."
        )

    text_schedule.delete(1.0, tk.END)
    text_schedule.insert(tk.END, schedule_text)


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Генератор расписания для школы")

    tk.Button(root, text="Ввести предметы", command=input_subjects_gui).pack()
    tk.Button(root, text="Ввести учителей", command=input_teachers_gui).pack()
    tk.Button(root, text="Ввести классы", command=input_classes_gui).pack()
    tk.Button(
        root, text="Распределить часы по классам", command=distribute_hours_gui
    ).pack()
    tk.Button(
        root, text="Сгенерировать расписание", command=generate_schedule_gui
    ).pack()

    text_schedule = tk.Text(root, height=20, width=60)
    text_schedule.pack()

    root.mainloop()
