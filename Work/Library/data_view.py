"""
Просмотр справочников с исходными данными
"""

import pandas as pd
import tkinter as tki
from tkinter import ttk
from tkinter import filedialog as fld
import argparse
import numpy as np


def clear_top():
    """
    Очищает все виджеты в верхнем фрейме (top).

    Returns
    -------
    None.

    """
    for widgets in top.winfo_children():
        widgets.destroy()


def read_data(file_path):
    """
    Читает данные из файла Pickle и отображает их в таблице.

    Parameters
    ----------
    file_path : str
        Путь к файлу Pickle.

    Returns
    -------
    None.

    """

    global GDS, HEIGHT, WIDTH, VRS, PNT
    GDS = pd.read_pickle(file_path)
    HEIGHT = GDS.shape[0]
    WIDTH = GDS.shape[1]
    # Очистка существующих виджетов
    clear_top()
    # Отображение заголовков столбцов
    headers = GDS.columns
    for j, header in enumerate(headers):
        lbl = tki.Label(top, text=header, font=(
            'HYWenHei', 12, 'bold'), bg='#EF9B6C')
        lbl.grid(row=0, column=j)
    # Корректировка индекса для строк данных
    start_row = 1
    # Инициализация массивов переменных и виджетов
    VRS = np.empty(shape=(HEIGHT, WIDTH), dtype="O")
    PNT = np.empty(shape=(HEIGHT, WIDTH), dtype="O")
    for i in range(HEIGHT):
        for j in range(WIDTH):
            VRS[i, j] = tki.StringVar()
            PNT[i, j] = tki.Entry(
                top, textvariable=VRS[i, j], bg='#FAF7DF', font=('HYWenHei', 10))
            PNT[i, j].grid(row=i+start_row, column=j)
            PNT[i, j].bind('<Button-1>', select_row)
            cnt = GDS.iloc[i, j]
            VRS[i, j].set(str(cnt))


def store_excel():
    """
    Сохраняет данные в файл Excel.

    Returns
    -------
    None.

    """

    ftypes = [('Excel файлы', '*.xlsx'), ('Все файлы', '*')]
    dlg = fld.SaveAs(filetypes=ftypes)
    fl = dlg.show()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            GDS.iloc[i, j] = PNT[i, j].get()
    GDS.to_excel(fl, index=False)


def store_pic():
    """
    Сохраняет данные в файл Pickle.

    Returns
    -------
    None.

    """
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if PNT[i, j].winfo_exists():  # Проверка существования виджета
                GDS.iloc[i, j] = PNT[i, j].get()
    GDS.to_pickle(PICKLE_FILE_PATH)  # Сохранение в исходный файл Pickle


SELECTED_ROW = None


def select_row(event):
    """
    Выбирает строку при нажатии на ячейку.

    Parameters
    ----------
    event : tkinter.Event
        Событие нажатия на ячейку.

    Returns
    -------
    None.

    """
    global SELECTED_ROW
    widget = event.widget
    row = widget.grid_info()['row']
    SELECTED_ROW = row


def delete_row():
    """
    Удаляет выбранную строку из таблицы.

    Returns
    -------
    None.

    """
    global GDS, HEIGHT, WIDTH, VRS, PNT, SELECTED_ROW
    if SELECTED_ROW is not None:
        row_index = SELECTED_ROW - 1  # Корректировка для строки заголовка
        GDS = GDS.drop(GDS.index[row_index]).reset_index(drop=True)
        HEIGHT = GDS.shape[0]
        WIDTH = GDS.shape[1]
        VRS = np.delete(VRS, row_index, axis=0)
        for j in range(WIDTH):
            if PNT[row_index, j].winfo_exists():
                PNT[row_index, j].destroy()
        PNT = np.delete(PNT, row_index, axis=0)
        for i in range(row_index, HEIGHT):
            for j in range(WIDTH):
                PNT[i, j].grid(row=i+1, column=j)
        SELECTED_ROW = None


def add_row():
    """
    Добавляет новую строку в таблицу.

    Returns
    -------
    None.

    """
    global GDS, HEIGHT, WIDTH, VRS, PNT
    new_row = pd.DataFrame([['' for _ in range(WIDTH)]], columns=GDS.columns)
    GDS = pd.concat([GDS, new_row], ignore_index=True)
    HEIGHT = GDS.shape[0]
    WIDTH = GDS.shape[1]
    new_vrs = np.empty(shape=(1, WIDTH), dtype="O")
    for j in range(WIDTH):
        new_vrs[0, j] = tki.StringVar()
    VRS = np.concatenate((VRS, new_vrs), axis=0)
    new_pnt = np.empty(shape=(1, WIDTH), dtype="O")
    for j in range(WIDTH):
        new_pnt[0, j] = tki.Entry(top, textvariable=VRS[HEIGHT-1, j],
                                  bg='#FAF7DF', font=('HYWenHei', 10))
        new_pnt[0, j].grid(row=HEIGHT, column=j)
    PNT = np.concatenate((PNT, new_pnt), axis=0)


# Настройка главного окна Tkinter
GDS = pd.DataFrame([])
HEIGHT = GDS.shape[0]
WIDTH = GDS.shape[1]
PNT = np.empty([])
VRS = np.empty([])
top = []
PICKLE_FILE_PATH = None  

root = tki.Tk()

# Построение таблицы
top = tki.LabelFrame(root, text="Таблица артефактов",
                     bg='#EF9B6C', font=('HYWenHei', 12))
top.grid(column=0, row=0)
bottom = tki.LabelFrame(root, text="Управление",
                        bg='#D0F69F', font=('HYWenHei', 12))
# Добавление прнивязки для расширения нижнего фрейма
bottom.grid(column=0, row=1, sticky="we")

# Установка веса столбца для расширения нижнего фрейма
root.grid_columnconfigure(0, weight=1)

# Создание стиля для кнопок
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Добавление кнопок с соответствующими функциями
btn_0 = ttk.Button(bottom, text='Добавить строку',
                   style="TButton", command=add_row)
btn_0.grid(row=0, column=0)
btn_1 = ttk.Button(bottom, text='Удалить строку',
                   style="TButton", command=delete_row)
btn_1.grid(row=0, column=1)
btn_2 = ttk.Button(bottom, text='Очистить таблицу',
                   style="TButton", command=clear_top)
btn_2.grid(row=0, column=2)
btn_3 = ttk.Button(bottom, text='Сохранить в Excel',
                   style="TButton", command=store_excel)
btn_3.grid(row=0, column=3)
btn_4 = ttk.Button(bottom, text='Сохранить в Pickle',
                   style="TButton", command=store_pic)
btn_4.grid(row=0, column=4)
btn_5 = ttk.Button(bottom, text='В меню',
                   style="TButton", command=root.destroy)
btn_5.grid(row=0, column=5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Отображение и редактирование таблицы из файла Pickle.")
    parser.add_argument("pickle_file_path", help="Путь к файлу Pickle")
    args = parser.parse_args()

    PICKLE_FILE_PATH = args.pickle_file_path

    # Чтение данных из указанного файла Pickle при запуске
    read_data(PICKLE_FILE_PATH)

    tki.mainloop()
