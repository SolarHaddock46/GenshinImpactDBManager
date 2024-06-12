"""
Главное меню
"""
import tkinter as tki
from tkinter import ttk
from tkinter import messagebox
import subprocess
import shutil
import os

# Глобальный массив запущенных подпроцессов
subprocesses = []


def open_artifacts_window():
    """
    Открывает новое окно для просмотра данных об артефактах.
    Запускает подпроцесс, выполняющий скрипт data_view.py с указанием 
    путь к файлу artifacts.pckl в качестве аргумента.

    Returns
    -------
    None.

    """
    file_path = '../Data/artifacts.pckl'
    process = subprocess.Popen(
        ['python', '../Library/data_view.py', file_path])
    subprocesses.append(process)


def open_characters_window():
    """
    Открывает новое окно для просмотра данных о персонажах.
    Запускает подпроцесс, выполняющий скрипт data_view.py с аргументом
    characters.pckl в качестве аргумента.

    Returns
    -------
    None.

    """
    file_path = '../Data/characters.pckl'
    process = subprocess.Popen(
        ['python', '../Library/data_view.py', file_path])
    subprocesses.append(process)


def run_text_display():
    """
    Запускает скрипт text_display.py для отображения отчетов-таблиц.
    Запускает подпроцесс, выполняющий скрипт text_display.py.

    Returns
    -------
    None.

    """
    process = subprocess.Popen(['python', '../Library/text_display.py'])
    subprocesses.append(process)


def run_text_report_generator():
    """
    Запускает скрипт text_report_generator.py для создания текстовых отчетов.
    Запускает подпроцесс, выполняющий скрипт text_report_generator.py.

    Returns
    -------
    None.

    """
    process = subprocess.Popen(
        ['python', '../Library/text_report_generator.py'])
    subprocesses.append(process)


def run_graphics_display():
    """
    Запускает скрипт graphics_display.py для отображения графических отчетов.
    Запускает подпроцесс, выполняющий скрипт graphics_display.py.

    Returns
    -------
    None.

    """
    process = subprocess.Popen(['python', '../Library/graphics_display.py'])
    subprocesses.append(process)


def wipe_folder(folder_path):
    """
    Удаляет все содержимое указанной папки.
    Если папка существует, ее содержимое удаляется с помощью shutil.rmtree(). 
    Затем папка создается заново как пустой каталог с помощью os.makedirs().

    Parameters
    ----------
    folder_path : str
        Путь к удаляемой папке.

    Returns
    -------
    None.

    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def quit_all():
    """
    Завершает все подпроцессы, стирает графические и выходные папки и завершает работу приложения.
    Все запущенные подпроцессы завершаются изящно с таймаутом в 2 секунды. 
    Если они не завершаются в течение этого времени, они завершаются принудительно.
    Содержимое папок 'Graphics' и 'Output' удаляется, если пользователь дает согласие.
    Наконец, уничтожается главное окно приложения.

    Returns
    -------
    None.

    """
    # Спрашиваем пользователя, хочет ли он очистить папки
    consent = messagebox.askyesno("Завершение приложения",
                                  "Вы хотите очистить папки 'Graphics' и 'Output' перед выходом?")
    # Останавливаем все подпроцессы
    for proc in subprocesses:
        proc.terminate()
    # Если за 2 секунды подпроцесс не останавливается, завершаем принудительно
    for proc in subprocesses:
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()

    if consent:
        # Очищаем папки, если пользователь разрешил
        wipe_folder('../Graphics')
        wipe_folder('../Output')

    # Останавливаем окно меню
    menu_window.destroy()


# Создание главного окна
menu_window = tki.Tk()
menu_window.title("Главное меню")
menu_window.geometry("400x300")  
menu_window.configure(bg="#D0F69F")  # Установка цвета фона

# Установка стиля кнопок
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Создание кнопок
artifacts_button = ttk.Button(menu_window, text="Просмотреть таблицу артефактов",
                              style="TButton", command=open_artifacts_window)
characters_button = ttk.Button(
    menu_window, text="Просмотреть таблицу персонажей", style="TButton",
    command=open_characters_window)
script1_button = ttk.Button(
    menu_window, text="Просмотр отчетов-таблиц", style="TButton",
    command=run_text_display)
script2_button = ttk.Button(
    menu_window, text="Генерация текстового отчета", style="TButton",
    command=run_text_report_generator)
script3_button = ttk.Button(
    menu_window, text="Просмотр графических отчетов", style="TButton",
    command=run_graphics_display)
quit_button = ttk.Button(
    menu_window, text="Завершить приложение", style="TButton", command=quit_all)

# Позиционирование кнопок
artifacts_button.pack(pady=10)
characters_button.pack(pady=10)
script1_button.pack(pady=10)
script2_button.pack(pady=10)
script3_button.pack(pady=10)
quit_button.pack(pady=10)

menu_window.mainloop()
