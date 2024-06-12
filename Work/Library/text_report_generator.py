"""
Генерация и просмотр текстового отчета по критериям
"""

import tkinter as tki
from tkinter import ttk
from tkinter import filedialog as fld
import pandas as pd
import numpy as np
import report_creator


def clear_top():
    """
    Очищает все виджеты в верхнем фрейме (top).

    Returns
    -------
    None.

    """
    for widgets in top.winfo_children():
        widgets.destroy()


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
    if not fl:
        return
    for i in range(HEIGHT):
        for j in range(WIDTH):
            GDS.iloc[i, j] = PNT[i, j].get()
    GDS.to_excel(fl, index=False)


def store_text():
    """
    Сохраняет данные в файл CSV с указанным разделителем и десятичным разделителем.

    Returns
    -------
    None.

    """
    ftypes = [('CSV files', '*.csv'), ('All files', '*')]
    dlg = fld.SaveAs(filetypes=ftypes)
    fl = dlg.show()
    if not fl:
        return

    for i in range(HEIGHT):
        for j in range(WIDTH):
            GDS.iloc[i, j] = PNT[i, j].get()

    # Получение выбранного разделителя и десятичного разделителя
    separator = separator_var.get()
    decimal = decimal_var.get()

    # Сохранение данных в файл CSV с указанным разделителем и десятичным разделителем
    GDS.to_csv(fl, index=False, sep=separator, decimal=decimal)


def generate_report():
    """
    Генерирует текстовый отчет на основе выбранных критериев.

    Returns
    -------
    None.

    """
    # Загрузка данных из файлов
    artifacts = pd.read_pickle('../Data/artifacts.pckl')
    characters = pd.read_pickle('../Data/characters.pckl')
    rarities = pd.read_pickle('../Data/rarities.pckl')

    # Объединение данных артефактов с данными персонажей по идентификатору персонажа
    data = pd.merge(artifacts, characters, left_on='id персонажа, исп. артефакт',
                    right_on='id персонажа', how='left')

    # Приведение данных о редкости артефактов к целочисленному типу
    data['Редкость артефакта'] = data['Редкость артефакта'].astype('int64')

    # Объединение данных с информацией о редкостях артефактов
    data = pd.merge(data, rarities, on='Редкость артефакта', how='left')

    # Расчет требуемого опыта для каждого артефакта
    data['Требуемый опыт'] = data.apply(lambda row: report_creator.calculate_required_exp(
        row['Текущий уровень'], row['Максимально возможный уровень артефакта']), axis=1)

    # Генерация и сохранение в файл текстового отчета
    user_input = artifacts_var.get()
    row_criteria = {'Сет артефакта': user_input}
    columns = ['Название артефакта', 'Текущий уровень', 'Требуемый опыт']
    reference_tables = {'characters': characters, 'rarities': rarities}
    text_report = report_creator.generate_text_report(
        data, reference_tables, row_criteria, columns)
    text_report.to_csv("../Output/text_report.csv",
                       index=False, encoding="utf-8")
    display_report("../Output/text_report.csv")


def display_report(filepath):
    """
    Отображает отчет из указанного файла.

    Parameters
    ----------
    filepath : str
        Путь к файлу отчета.

    Returns
    -------
    None.

    """
    clear_top()  # Очистка существующих виджетов в верхнем фрейме

    # Чтение файла отчета
    report_data = pd.read_csv(filepath, sep=',', encoding='utf-8')

    # Обновление глобальных переменных для отражения новых данных
    global GDS, HEIGHT, WIDTH, VRS, PNT
    GDS = report_data
    HEIGHT = GDS.shape[0]
    WIDTH = GDS.shape[1]

    # Отображение заголовков столбцов
    headers = list(GDS.columns)
    for j, header in enumerate(headers):
        lbl = tki.Label(top, text=header, font=(
            'HYWenHei', 12, 'bold'), bg='#EF9B6C')
        lbl.grid(row=0, column=j)

    # Отображение данных в таблице
    start_row = 1
    VRS = np.empty((HEIGHT, WIDTH), dtype=object)
    PNT = np.empty((HEIGHT, WIDTH), dtype=object)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            VRS[i, j] = tki.StringVar(value=str(GDS.iloc[i, j]))
            PNT[i, j] = tki.Entry(
                top, textvariable=VRS[i, j], bg='#FAF7DF',
                font=('HYWenHei', 10))
            PNT[i, j].grid(row=i + start_row, column=j)


GDS = pd.DataFrame([])
HEIGHT = GDS.shape[0]
WIDTH = GDS.shape[1]
PNT = np.empty([])
VRS = np.empty([])
top = []
CSV_FILE_PATH = None  

root = tki.Tk()

# Построение таблицы
top = tki.LabelFrame(root, text="Таблица отчета",
                     bg='#EF9B6C', font=('HYWenHei', 12))
top.grid(column=0, row=0)
bottom = tki.LabelFrame(root, text="Управление",
                        bg='#D0F69F', font=('HYWenHei', 12))
# Добавление sticky="we" для расширения нижнего фрейма
bottom.grid(column=0, row=1, sticky="we")

# Установка веса столбца для расширения нижнего фрейма
root.grid_columnconfigure(0, weight=1)

# Создание стиля для кнопок
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Добавление текстового поля для указания сета артефактов
artifacts_label = ttk.Label(
    bottom, text="Сет артефактов для отчета:", font=('HYWenHei', 12))
artifacts_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="e")

artifacts_var = tki.StringVar()
artifacts_entry = ttk.Entry(
    bottom, textvariable=artifacts_var, font=('HYWenHei', 12), width=20)
artifacts_entry.grid(row=0, column=1, columnspan=3,
                     padx=(0, 10), pady=10, sticky="we")

# Добавление кнопки для создания текстового отчета
generate_btn = ttk.Button(
    bottom, text='Создать текстовый отчет', style="TButton", command=generate_report)
generate_btn.grid(row=0, column=4, columnspan=2,
                  padx=(5, 10), pady=10, sticky="we")

# Добавление кнопок управления
btn_3 = ttk.Button(bottom, text='Сохранить в Excel',
                   style="TButton", command=store_excel)
btn_3.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=10, sticky="we")

btn_4 = ttk.Button(bottom, text='Сохранить в CSV',
                   style="TButton", command=store_text)
btn_4.grid(row=1, column=2, columnspan=2, padx=(5, 5), pady=10, sticky="we")

btn_5 = ttk.Button(bottom, text='В меню',
                   style="TButton", command=root.destroy)
btn_5.grid(row=1, column=4, columnspan=2, padx=(5, 10), pady=10, sticky="we")

# Добавление выпадающих меню для выбора разделителя и десятичного разделителя
separator_label = ttk.Label(
    bottom, text="Разделитель CSV:", font=('HYWenHei', 12))
separator_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="e")

separator_var = tki.StringVar()
separator_menu = ttk.Combobox(bottom, textvariable=separator_var, font=(
    'HYWenHei', 12), state='readonly', width=5)
separator_menu['values'] = (',', ';', '\t')  # Добавление доступных разделителей
separator_menu.current(0)  # Установка разделителя по умолчанию (запятая)
separator_menu.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")

decimal_label = ttk.Label(
    bottom, text="Десятичный разделитель CSV:", font=('HYWenHei', 12))
decimal_label.grid(row=2, column=2, padx=(10, 0), pady=10, sticky="e")

decimal_var = tki.StringVar()
decimal_menu = ttk.Combobox(bottom, textvariable=decimal_var, font=(
    'HYWenHei', 12), state='readonly', width=5)
decimal_menu['values'] = ('.', ',')  # Добавление доступных десятичных разделителей
decimal_menu.current(0)  # Установка десятичного разделителя по умолчанию (точка)
decimal_menu.grid(row=2, column=3, padx=(0, 10), pady=10, sticky="w")

tki.mainloop()
