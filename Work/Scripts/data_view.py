# -*- coding: utf-8 -*-
"""
Работа с таблицами
Автор: Поляков К. Л.
"""

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import argparse

GDS = pd.DataFrame([])
height = 0
width = 0
top = []
vrs = np.empty([])
pnt = np.empty([])
pickle_file_path = None
selected_row = None


def clear_top():
    """
    Очистка содержимого фрейма 'top'.
    """
    for widget in top.winfo_children():
        widget.destroy()


def read_data(file_path=None):
    """
    Читает данные из Pickle файла и отображает их в таблице.
    """
    global GDS, height, width, top, vrs, pnt
    try:
        GDS = pd.read_pickle(file_path)
        height, width = GDS.shape
        clear_top()

        headers = GDS.columns
        for j, header in enumerate(headers):
            lbl = tk.Label(top, text=header, font=('HYWenHei', 12, 'bold'), bg='#EF9B6C')
            lbl.grid(row=0, column=j, sticky="ew")

        vrs = np.empty((height, width), dtype=object)
        pnt = np.empty((height, width), dtype=object)

        for i in range(height):
            for j in range(width):
                vrs[i, j] = tk.StringVar(value=str(GDS.iloc[i, j]))
                pnt[i, j] = tk.Entry(top, textvariable=vrs[i, j], bg='#FAF7DF', font=('HYWenHei', 10))
                pnt[i, j].grid(row=i + 1, column=j)
                pnt[i, j].bind('<Button-1>', select_row)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")


def store_excel():
    """
    Сохраняет данные из таблицы в Excel файл.
    """
    ftypes = [('Excel files', '*.xlsx'), ('All files', '*')]
    fl = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".xlsx")
    if fl:
        try:
            for i in range(height):
                for j in range(width):
                    GDS.iloc[i, j] = pnt[i, j].get()
            GDS.to_excel(fl, index=False)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


def store_pic():
    """
    Сохраняет данные из таблицы обратно в Pickle файл.
    """
    try:
        for i in range(height):
            for j in range(width):
                GDS.iloc[i, j] = pnt[i, j].get()
        GDS.to_pickle(pickle_file_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


def select_row(event):
    """
    Выбор строки в таблице.
    """
    global selected_row
    widget = event.widget
    selected_row = widget.grid_info()['row'] - 1


def delete_row():
    """
    Удаляет выбранную строку из таблицы.
    """
    global GDS, height
    if selected_row is not None and 0 <= selected_row < height:
        GDS = GDS.drop(GDS.index[selected_row]).reset_index(drop=True)
        height -= 1
        read_data(pickle_file_path)  # Refresh the table display
        selected_row = None


def add_row():
    """
    Добавляет новую строку в таблицу.
    """
    global GDS, height
    new_row = pd.DataFrame([['' for _ in range(width)]], columns=GDS.columns)
    GDS = pd.concat([GDS, new_row], ignore_index=True)
    height = GDS.shape[0]
    read_data(pickle_file_path)  # Refresh the table display


def open_window(file_path=None):
    """
    Открывает окно для работы с таблицей.
    """
    global top, bottom, pickle_file_path, root
    pickle_file_path = file_path

    root = tk.Tk()
    root.title("Редактор данных")
    if 'artifacts' in pickle_file_path:
        top = tk.LabelFrame(root, text="Таблица артефактов", bg='#EF9B6C', font=('HYWenHei', 12))
    elif 'characters' in pickle_file_path:
        top = tk.LabelFrame(root, text="Таблица персонажей", bg='#EF9B6C', font=('HYWenHei', 12))
    top.grid(column=0, row=0, pady=5, padx=5, sticky="nsew")
    bottom = tk.LabelFrame(root, text="Управление", bg='#D0F69F', font=('HYWenHei', 12))
    bottom.grid(column=0, row=1, pady=5, padx=5, sticky="ew")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    style = ttk.Style()
    style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

    buttons = [
        ("Добавить строку", add_row),
        ("Удалить строку", delete_row),
        ("Очистить таблицу", clear_top),
        ("Сохранить в Excel", store_excel),
        ("Сохранить в Pickle", store_pic),
        ("В меню", root.destroy)
    ]
    for i, (label, command) in enumerate(buttons):
        btn = ttk.Button(bottom, text=label, style="TButton", command=command)
        btn.grid(row=0, column=i, padx=5, pady=5)

    read_data(file_path)

    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Редактор данных")
    parser.add_argument("file_path", help="Путь к файлу Pickle для редактирования")
    args = parser.parse_args()

    open_window(args.file_path)


if __name__ == "__main__":
    main()