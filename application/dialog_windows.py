import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from multiprocessing import Process, Queue
from tkinter.simpledialog import askstring
from tkinter import filedialog as f


def show_error_window(title, message):
    root = tk.Tk()
    root.withdraw()
    showerror(title, message)
    root.destroy()


def show_info_window(title, message):
    root = tk.Tk()
    root.withdraw()
    showinfo(title, message)
    root.destroy()


def show_string_input_window(title, message, q):
    root = tk.Tk()
    root.withdraw()
    ans = askstring(title, message)
    root.destroy()
    q.put(ans)


def restore_backup_window(q):
    root = tk.Tk()
    root.withdraw()
    ans = f.askopenfilename()
    root.destroy()
    q.put(ans)


def show_error_window_in_thread(title, message):
    p = Process(target=show_error_window, args=(title, message))
    p.start()
    p.join()


def show_info_window_in_thread(title, message):
    p = Process(target=show_info_window, args=(title, message))
    p.start()
    p.join()


def show_string_input_window_in_thread(title, message):
    queue = Queue()
    p = Process(target=show_string_input_window, args=(title, message, queue))
    p.start()
    p.join()
    ans = queue.get()
    return ans


def restore_backup_window_in_thread():
    queue = Queue()
    p = Process(target=restore_backup_window, args=(queue,))
    p.start()
    p.join()
    ans = queue.get()
    return ans
