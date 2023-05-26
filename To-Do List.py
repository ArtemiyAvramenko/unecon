import json
import threading
import tkinter as tk
from tkinter import messagebox
import datetime

root = tk.Tk()
root.title("To-Do List")

tasks = []

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"total": 0, "completed": 0}

def save_tasks():
    data = {"total": len(tasks), "completed": len([t for t in tasks if t["completed"]])}
    with open("tasks.json", "w") as f:
        json.dump(data, f)

def add_task():
    task = task_entry.get()
    if task != "":
        tasks.append(task)
        task_listbox.insert(tk.END, task)
        update_stats() # обновление статистики
    task_entry.delete(0, tk.END)

def reset_stats():
    with open("tasks.json", "w") as f:
        data = {"total": 0, "completed": 0}
        json.dump(data, f)

def clear_tasks():
    tasks.clear()
    task_listbox.delete(0, tk.END)
    reset_stats() # обнуление статистики
    update_stats()

def delete_task():
    if not task_listbox.curselection():
        messagebox.showerror("Ошибка", "Пожалуйста, выберите задачу для удаления.")
        return
    selected_task = task_listbox.curselection()[0]
    task_listbox.delete(selected_task)
    tasks.pop(selected_task)
    update_stats() # обновление статистики

def complete_task():
    if not task_listbox.curselection():
        messagebox.showerror("Ошибка", "Пожалуйста, выберите задачу для отметки как выполненную.")
        return
    selected_task = task_listbox.curselection()[0]
    task = task_listbox.get(selected_task)
    if not task.endswith("(done)"):
        task_listbox.itemconfig(selected_task, bg="#adff2f")
        task_listbox.delete(selected_task)
        tasks.pop(selected_task)
        tasks.append(task + " (done)")
        task_listbox.insert(tk.END, task + " (done)")
        update_stats() # обновление статистики

stats_label = tk.Label(root, text="")
stats_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

def update_stats_label():
    data = load_tasks()
    if data["total"] == 0:
        stats_label.configure(text="")
    else:
        percent_completed = int(data["completed"] / data["total"] * 100)
        stats_label.configure(text=f"Выполнено: {percent_completed}% ({data['completed']} из {data['total']})")

update_stats_label()

def update_stats():
    num_tasks = len(tasks)
    if num_tasks == 0:
        stats_label.configure(text="")
    else:
        num_completed = sum([1 for task in tasks if task.endswith("(done)")])
        percent_completed = int(num_completed / num_tasks * 100)
        stats_label.configure(text=f"Выполнено: {percent_completed}% ({num_completed} из {num_tasks})")

def countdown(task_label, due_time):
    remaining_seconds = (due_time - datetime.datetime.now()).total_seconds()
    while remaining_seconds > 0:
        mins, secs = divmod(remaining_seconds, 60)
        hours, mins = divmod(mins, 60)
        task_label.configure(text=f"{task_label['text']} ({int(hours):02}:{int(mins):02}:{int(secs):02})")
        remaining_seconds = max(0, remaining_seconds - 1)
        datetime.time.sleep(1)



def add_timed_task():
    task = task_entry.get()
    if task != "":
        due_time = datetime.datetime.now()
        time_str = timer_entry.get()
        if time_str:
            try:
                hours, minutes, seconds = map(int, time_str.split(":"))
                due_time += datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите время в формате Часы:Минуты:Секунды.")
                return
            if due_time > datetime.datetime.now():
                task_listbox.insert(tk.END, f"{task} (до {due_time.strftime('%H:%M:%S')})")
                task_label = task_listbox.get(tk.END)
                threading.Thread(target=countdown, args=(task_label, due_time)).start()
                task_entry.delete(0, tk.END)
                timer_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректное время в будущем.")
        else:
            tasks.append(task)
            task_listbox.insert(tk.END, task)
            task_entry.delete(0, tk.END)
            update_stats()

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

stats_label = tk.Label(root, text="")
stats_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E+tk.W)

update_stats()
root.mainloop()

