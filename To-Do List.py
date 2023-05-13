import tkinter as tk
from tkinter import messagebox
import datetime

root = tk.Tk()
root.title("To-Do List")

tasks = []

def add_task():
    task = task_entry.get()
    if task != "":
        tasks.append(task)
        task_listbox.insert(tk.END, task)
    task_entry.delete(0, tk.END)

def clear_tasks():
    tasks.clear()
    task_listbox.delete(0, tk.END)

def delete_task():
    if not task_listbox.curselection():
        messagebox.showerror("Ошибка", "Пожалуйста, выберите задачу для удаления.")
        return
    selected_task = task_listbox.curselection()[0]
    task_listbox.delete(selected_task)
    tasks.pop(selected_task)

def complete_task():
    if not task_listbox.curselection():
        messagebox.showerror("Ошибка", "Пожалуйста, выберите задачу для отметки как выполненную.")
        return
    selected_task = task_listbox.curselection()[0]
    task_listbox.itemconfig(selected_task, bg="#adff2f")

def add_timed_task():
    task = task_entry.get()
    if task != "":
        tasks.append(task)

        now = datetime.datetime.now()
        time_str = timer_entry.get()
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите время в формате Часы:Минуты:Секунды.")
            return

        due_time = now + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        task_listbox.insert(tk.END, f"{task} (до {due_time.strftime('%H:%M:%S')})")

    task_entry.delete(0, tk.END)
    timer_entry.delete(0, tk.END)

task_label = tk.Label(root, text="Задачи:")
task_label.grid(row=0, column=0, padx=5, pady=5)

task_listbox = tk.Listbox(root, height=10, selectmode=tk.SINGLE)
task_listbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

task_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=task_listbox.yview)
task_scroll.grid(row=1, column=1, sticky=tk.N+tk.S)
task_listbox.config(yscrollcommand=task_scroll.set)

task_entry = tk.Entry(root, width=40)
task_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

add_task_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

clear_tasks_button = tk.Button(root, text="Очистить список", command=clear_tasks)
clear_tasks_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

delete_task_button = tk.Button(root, text="Удалить задачу", command=delete_task)
delete_task_button.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

complete_task_button = tk.Button(root, text="Отметить как выполненную", command=complete_task)
complete_task_button.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

timer_label = tk.Label(root, text="Впишите таймер (Часы:Минуты:Секунды):")
timer_label.grid(row=0, column=2, padx=5, pady=5)






timer_entry = tk.Entry(root, width=20)
timer_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E+tk.W)

add_timed_task_button = tk.Button(root, text="Добавить задачу с таймером", command=add_timed_task)
add_timed_task_button.grid(row=3, column=2, padx=5, pady=5, sticky=tk.E+tk.W)

root.mainloop()