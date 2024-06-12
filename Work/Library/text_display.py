"""
Просмотр отчетов-таблиц
"""
import tkinter as tki
from tkinter import ttk
from tkinter import filedialog as fld
import pandas as pd
import numpy as np
import report_creator


def clear_top():
    """
    Очищает верхний фрейм от всех виджетов.

    Returns
    -------
    None.

    """
    for widgets in TOP.winfo_children():
        widgets.destroy()


def store_excel():
    """
    Сохраняет данные из таблицы в файл Excel.

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
    Сохраняет данные из таблицы в CSV-файл с выбранным разделителем и десятичным разделителем.

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

    # Получение указанных пользователем разделителей и сохранение с их учетом
    separator = separator_var.get()
    decimal = decimal_var.get()
    GDS.to_csv(fl, index=False, sep=separator, decimal=decimal)


def generate_and_display_freq_table(data, var):
    """
    Генерирует и отображает таблицу частот для выбранной переменной.

    Parameters
    ----------
    data : pandas.DataFrame
        Исходные данные.
    var : str
        Название переменной для анализа.

    Returns
    -------
    None.

    """
    freq_table = data[var].value_counts().reset_index()
    freq_table.columns = [var, 'Частота']
    freq_table['Доля в %'] = freq_table['Частота'] / len(data) * 100
    freq_table.to_csv(
        f'../Output/freq_table_{var}.csv', index=False, encoding='utf-8')
    display_report(f"../Output/freq_table_{var}.csv")



def select_report_type(event):
    """
    Обработчик события выбора типа отчета из выпадающего меню.

    Parameters
    ----------
    event : tkinter.Event
        Событие выбора типа отчета.

    Returns
    -------
    None.

    """
    report_type = report_type_var.get()


def generate_report():
    """
    Генерирует выбранный тип отчета на основе загруженных данных.

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

    # Получение указанного пользователем типа отчета и генерация соответствующего отчета
    report_type = report_type_var.get()
    if report_type == "Сводная таблица":
        index = ['Сет артефакта']
        columns = ['Вид артефакта']
        values = 'Требуемый опыт'
        aggfunc = 'sum'
        pivot_table = report_creator.generate_pivot_table(
            data, index, columns, values, aggfunc)
        pivot_table.to_csv('../Output/pivot_table.csv',
                           index=True, encoding='utf-8')
        display_report("../Output/pivot_table.csv")
    elif report_type == "Частотный анализ для переменной 'Сет артефакта'":
        generate_and_display_freq_table(data, 'Сет артефакта')
    elif report_type == "Частотный анализ для переменной 'Вид артефакта'":
        generate_and_display_freq_table(data, 'Вид артефакта')
    elif report_type == "Артефакты персонажей":
        character_artifacts = data.groupby('Имя персонажа')[
            'Название артефакта'].apply(list).reset_index()
        # Фильтрация списка артефактов
        character_artifacts['Название артефакта'] = character_artifacts['Название артефакта'].apply(
            lambda x: ', '.join(x))
        character_artifacts.to_csv(
            '../Output/character_artifacts.csv', index=False, encoding='utf-8')
        display_report("../Output/character_artifacts.csv")


def display_report(filepath):
    """
    Отображает отчет из указанного файла в таблице.

    Parameters
    ----------
    filepath : str
        Путь к файлу отчета.

    Returns
    -------
    None.

    """
    clear_top() 

    # Считывание отчета из созданного файла
    report_data = pd.read_csv(filepath, sep=',', encoding='utf-8')

    # Обновление глобальных переменных
    global GDS, HEIGHT, WIDTH, VRS, PNT
    GDS = report_data
    HEIGHT = GDS.shape[0]
    WIDTH = GDS.shape[1]

    # отображение названий столбцов
    headers = list(GDS.columns)
    for j, header in enumerate(headers):
        lbl = tki.Label(TOP, text=header, font=(
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
                TOP, textvariable=VRS[i, j], bg='#FAF7DF', font=('HYWenHei', 10))
            PNT[i, j].grid(row=i + start_row, column=j)

    # Автоматическое изменение ширины строки для таблицы артефактов на персонажах
    if filepath == "../Output/character_artifacts.csv":
        for j in range(WIDTH):
            max_length = max(GDS.iloc[:, j].astype(
                str).apply(len).max(), len(headers[j]))
            for i in range(HEIGHT + 1):  # +1 for header row
                PNT[i-1, j].config(width=max_length)


# Настройка основого окна
GDS = pd.DataFrame([])
HEIGHT = GDS.shape[0]
WIDTH = GDS.shape[1]
PNT = np.empty([])
VRS = np.empty([])
TOP = []
CSV_FILE_PATH = None 

# Построение изображения
root = tki.Tk()

# Построение таблицы
TOP = tki.LabelFrame(root, text="Таблица отчета",
                     bg='#EF9B6C', font=('HYWenHei', 12))
TOP.grid(column=0, row=0)
bottom = tki.LabelFrame(root, text="Управление",
                        bg='#D0F69F', font=('HYWenHei', 12))
# Добавление привязки для расширения нижнего фрейма при изменении ширины окна
bottom.grid(column=0, row=1, sticky="we")

# Установка веса столбца для возможности расширения нижнего фрейма
root.grid_columnconfigure(0, weight=1)

# Установка стиля кнопок
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

artifacts_var = tki.StringVar()
artifacts_entry = ttk.Entry(
    bottom, textvariable=artifacts_var, font=('HYWenHei', 12), width=20)
artifacts_entry.grid(row=0, column=1, columnspan=3,
                     padx=(0, 10), pady=10, sticky="we")

# Создание выпадающего списка типов отчета
report_type_label = ttk.Label(
    bottom, text="Тип отчета:", font=('HYWenHei', 12))
report_type_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="e")

report_type_var = tki.StringVar()
report_type_menu = ttk.Combobox(bottom, textvariable=report_type_var, font=(
    'HYWenHei', 12), state='readonly', width=20)
report_type_menu['values'] = ("Сводная таблица", "Частотный анализ для переменной 'Сет артефакта'",
                              "Частотный анализ для переменной 'Вид артефакта'",
                              "Артефакты персонажей")  
report_type_menu.current(0)  # Первый вариант задается как основной
report_type_menu.bind("<<ComboboxSelected>>", select_report_type)
report_type_menu.grid(row=0, column=1, columnspan=3,
                      padx=(0, 10), pady=10, sticky="we")

# Создание кнопки генерации отчета
generate_btn = ttk.Button(
    bottom, text='Создать текстовый отчет', style="TButton", command=generate_report)
generate_btn.grid(row=0, column=4, columnspan=2,
                  padx=(5, 10), pady=10, sticky="we")

# Создание кнопок управления
btn_3 = ttk.Button(bottom, text='Сохранить в Excel',
                   style="TButton", command=store_excel)
btn_3.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=10, sticky="we")

btn_4 = ttk.Button(bottom, text='Сохранить в CSV',
                   style="TButton", command=store_text)
btn_4.grid(row=1, column=2, columnspan=2, padx=(5, 5), pady=10, sticky="we")

btn_5 = ttk.Button(bottom, text='В меню',
                   style="TButton", command=root.destroy)
btn_5.grid(row=1, column=4, columnspan=2, padx=(5, 10), pady=10, sticky="we")

# Создание выпадающих списков разделителей для CSV
separator_label = ttk.Label(
    bottom, text="Разделитель CSV:", font=('HYWenHei', 12))
separator_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="e")

separator_var = tki.StringVar()
separator_menu = ttk.Combobox(bottom, textvariable=separator_var, font=(
    

    'HYWenHei', 12), state='readonly', width=5)
separator_menu['values'] = (',', ';', '\t')  
separator_menu.current(0)  # Разделитель по умолчанию - запятая
separator_menu.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")

decimal_label = ttk.Label(
    bottom, text="Десятичный разделитель CSV:", font=('HYWenHei', 12))
decimal_label.grid(row=2, column=2, padx=(10, 0), pady=10, sticky="e")

decimal_var = tki.StringVar()
decimal_menu = ttk.Combobox(bottom, textvariable=decimal_var, font=(
    'HYWenHei', 12), state='readonly', width=5)
decimal_menu['values'] = ('.', ',')  
decimal_menu.current(0)  # Десятичеый разделитель по умолчанию - точка
decimal_menu.grid(row=2, column=3, padx=(0, 10), pady=10, sticky="w")

tki.mainloop()
