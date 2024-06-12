import tkinter as tk
from tkinter import ttk
import subprocess
import shutil
import os

# Global list to keep track of all subprocesses
subprocesses = []

def open_artifacts_window():
    file_path = '../Data/artifacts.pckl'
    process = subprocess.Popen(['python', '../Library/data_view.py', file_path])
    subprocesses.append(process)

def open_characters_window():
    file_path = '../Data/characters.pckl'
    process = subprocess.Popen(['python', '../Library/data_view.py', file_path])
    subprocesses.append(process)

def run_script1():
    process = subprocess.Popen(['python', '../Library/text_display.py'])
    subprocesses.append(process)

def run_script2():
    process = subprocess.Popen(['python', '../Library/text_report_generator.py'])
    subprocesses.append(process)

def run_script3():
    process = subprocess.Popen(['python', '../Library/graphics_display.py'])
    subprocesses.append(process)

def wipe_folder(folder_path):
    """
    Delete and recreate a folder to wipe its contents.
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def quit_all():
    # Terminate all subprocesses
    for proc in subprocesses:
        proc.terminate()
    # Give some time to terminate gracefully before killing forcefully
    for proc in subprocesses:
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()

    # Wipe the contents of the graphics and output folders
    wipe_folder('../Graphics')
    wipe_folder('../Output')

    # Terminate the main window
    menu_window.destroy()

# Create the main window
menu_window = tk.Tk()
menu_window.title("Menu")
menu_window.geometry("400x300")  # Adjusted size of the window
menu_window.configure(bg="#D0F69F")  # Set the background color

# Create a style for the buttons
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Create the buttons for opening data views
artifacts_button = ttk.Button(menu_window, text="Просмотреть таблицу артефактов", style="TButton", command=open_artifacts_window)
characters_button = ttk.Button(menu_window, text="Просмотреть таблицу персонажей", style="TButton", command=open_characters_window)

# Create buttons for running additional scripts
script1_button = ttk.Button(menu_window, text="Просмотр отчетов-таблиц", style="TButton", command=run_script1)
script2_button = ttk.Button(menu_window, text="Генерация текстового отчета", style="TButton", command=run_script2)
script3_button = ttk.Button(menu_window, text="Просмотр графических отчетов", style="TButton", command=run_script3)

# Create a quit button
quit_button = ttk.Button(menu_window, text="Завершить приложение", style="TButton", command=quit_all)

# Position the buttons
artifacts_button.pack(pady=10)
characters_button.pack(pady=10)
script1_button.pack(pady=10)
script2_button.pack(pady=10)
script3_button.pack(pady=10)
quit_button.pack(pady=10)

# Run the Tkinter event loop
menu_window.mainloop()