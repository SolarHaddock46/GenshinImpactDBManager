# -*- coding: utf-8 -*-
"""
Работа с текстовыми отчетами
Автор: Поляков К. Л.
"""

import numpy as np
import pandas as pd
import tkinter as tki
from tkinter import ttk
from tkinter import filedialog as fld
import report_creator

# Function to clear the 'top' frame
def clear_top():
    """
    Очистка фрейма top
    """
    for widgets in top.winfo_children():
       widgets.destroy()

# Function to read data from a CSV file
def read_data():
    """
    Reading and displaying data from a CSV file
    """
    global GDS, height, width, top, vrs, pnt, csv_file_path
    
    # Open file dialog to select a CSV file
    csv_file_path = fld.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*")])
    if not csv_file_path:
        return
    
    # Read the CSV file using pandas
    GDS = pd.read_csv(csv_file_path)
    height = GDS.shape[0]
    width = GDS.shape[1]
    
    # Clear existing widgets
    clear_top()
    
    # Display column headers
    headers = list(GDS.columns)
    for j, header in enumerate(headers):
        lbl = tki.Label(top, text=header, font=('HYWenHei', 12, 'bold'), bg='#EF9B6C')
        lbl.grid(row=0, column=j)
    
    # Adjust index for data rows
    start_row = 1
    
    # Initialize variable and widget arrays
    vrs = np.empty(shape=(height, width), dtype="O")
    pnt = np.empty(shape=(height, width), dtype="O")
    
    for i in range(height): 
        for j in range(width): 
            vrs[i, j] = tki.StringVar()
            pnt[i, j] = tki.Entry(top, textvariable=vrs[i, j], bg='#FAF7DF', font=('HYWenHei', 10)) 
            pnt[i, j].grid(row=i+start_row, column=j)
            pnt[i, j].bind('<Button-1>', select_row)
            cnt = GDS.iloc[i, j]
            vrs[i, j].set(str(cnt))
    
    # Resize the table cells to match the longest string in each column
    for j in range(width):
        max_length = max(GDS.iloc[:, j].astype(str).apply(len).max(), len(headers[j]))
        for i in range(height + 1):  # +1 for header row
            pnt[i-1, j].config(width=max_length)

# Function to save data to Excel file
def store_excel():
    """
    Получение даных таблицы из Tcl/Tk
    с помощью метода get() и сохранение в Excel
    """
    ftypes = [('Excel файлы', '*.xlsx'), ('Все файлы', '*')]
    dlg = fld.SaveAs(filetypes=ftypes)
    fl = dlg.show()
    if not fl:
        return
    for i in range(height): 
        for j in range(width): 
            GDS.iloc[i, j] = pnt[i, j].get()
    GDS.to_excel(fl, index=False)

# Function to save data to a CSV file
def store_text():
    """
    Getting table data from Tcl/Tk using the get() method and saving it to a CSV file
    """
    ftypes = [('CSV files', '*.csv'), ('All files', '*')]
    dlg = fld.SaveAs(filetypes=ftypes)
    fl = dlg.show()
    if not fl:
        return
    
    for i in range(height): 
        for j in range(width): 
            GDS.iloc[i, j] = pnt[i, j].get()
    
    # Get the selected separator and decimal separator
    separator = separator_var.get()
    decimal = decimal_var.get()
    
    # Save the data to a CSV file with the specified separator and decimal
    GDS.to_csv(fl, index=False, sep=separator, decimal=decimal)

selected_row = None

# Function to select a row in the table
def select_row(event):
    """
    Обработка выбора строки в таблице
    """
    global selected_row
    widget = event.widget
    row = widget.grid_info()['row']
    selected_row = row
    
def generate_and_display_freq_table(data, var):
    freq_table = data[var].value_counts().reset_index()
    freq_table.columns = [var, 'Частота']
    freq_table['Доля в %'] = freq_table['Частота'] / len(data) * 100
    freq_table.to_csv(f'../Output/freq_table_{var}.csv', index=False, encoding='utf-8')
    display_report(f"../Output/freq_table_{var}.csv")

# Function to handle report type selection
def select_report_type(event):
    """
    Обработка выбора типа отчета
    """
    report_type = report_type_var.get()
    # Implement logic based on selected report type
    print(f"Selected report type: {report_type}")

def generate_report():
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
    
    # Get selected report type
    report_type = report_type_var.get()
    if report_type == "Сводная таблица":
        # Generate pivot table report
        index = ['Сет артефакта']
        columns = ['Вид артефакта']
        values = 'Требуемый опыт'
        aggfunc = 'sum'
        pivot_table = report_creator.generate_pivot_table(data, index, columns, values, aggfunc)
        pivot_table.to_csv('../Output/pivot_table.csv', index=True, encoding='utf-8')
        display_report("../Output/pivot_table.csv")
    elif report_type == "Частотный анализ для переменной 'Сет артефакта'":
        generate_and_display_freq_table(data, 'Сет артефакта')
    elif report_type == "Частотный анализ для переменной 'Вид артефакта'":
        generate_and_display_freq_table(data, 'Вид артефакта')
    elif report_type == "Артефакты персонажей":
        # Generate report on artifacts equipped on each character
        character_artifacts = data.groupby('Имя персонажа')['Название артефакта'].apply(list).reset_index()
        
        # Beautify the array output
        character_artifacts['Название артефакта'] = character_artifacts['Название артефакта'].apply(lambda x: ', '.join(x))
        
        character_artifacts.to_csv('../Output/character_artifacts.csv', index=False, encoding='utf-8')
        display_report("../Output/character_artifacts.csv")
    else:
        print("Неизвестный тип отчета")

def display_report(filepath):
    """
    Display the content of the report in the GUI.
    """
    clear_top()  # Clear existing widgets in the top frame
    
    # Read the report file
    report_data = pd.read_csv(filepath, sep=',', encoding='utf-8')
    
    # Update global variables to reflect the new data
    global GDS, height, width, vrs, pnt
    GDS = report_data
    height = GDS.shape[0]
    width = GDS.shape[1]
    
    # Display column headers
    headers = list(GDS.columns)
    for j, header in enumerate(headers):
        lbl = tki.Label(top, text=header, font=('HYWenHei', 12, 'bold'), bg='#EF9B6C')
        lbl.grid(row=0, column=j)
    
    # Display data in the grid
    start_row = 1
    vrs = np.empty((height, width), dtype=object)
    pnt = np.empty((height, width), dtype=object)
    
    for i in range(height):
        for j in range(width):
            vrs[i, j] = tki.StringVar(value=str(GDS.iloc[i, j]))
            pnt[i, j] = tki.Entry(top, textvariable=vrs[i, j], bg='#FAF7DF', font=('HYWenHei', 10))
            pnt[i, j].grid(row=i + start_row, column=j)
    
    # Auto-resize table cells for the "Артефакты персонажей" report
    if filepath == "../Output/character_artifacts.csv":
        for j in range(width):
            max_length = max(GDS.iloc[:, j].astype(str).apply(len).max(), len(headers[j]))
            for i in range(height + 1):  # +1 for header row
                pnt[i-1, j].config(width=max_length)

# Setting up the main Tkinter window
hex_color = "#00FFFF"  # Define color in hex format

GDS = pd.DataFrame([])
height = GDS.shape[0]
width = GDS.shape[1]
pnt = np.empty([])
vrs = np.empty([])
top = []
csv_file_path = None  # Initialize the variable to store the CSV file path

# Построение изображения
root = tki.Tk()

# Построение таблицы
top = tki.LabelFrame(root, text="Таблица отчета", bg='#EF9B6C', font=('HYWenHei', 12))
top.grid(column=0, row=0)
bottom = tki.LabelFrame(root, text="Управление", bg='#D0F69F', font=('HYWenHei', 12))
bottom.grid(column=0, row=1, sticky="we")  # Add sticky="we" to expand the bottom frame

# Set the weight of the column to allow the bottom frame to expand
root.grid_columnconfigure(0, weight=1)

# Create a style for the buttons
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

artifacts_var = tki.StringVar()
artifacts_entry = ttk.Entry(bottom, textvariable=artifacts_var, font=('HYWenHei', 12), width=20)
artifacts_entry.grid(row=0, column=1, columnspan=3, padx=(0, 10), pady=10, sticky="we")

# Adding dropdown menu for selecting report type
report_type_label = ttk.Label(bottom, text="Тип отчета:", font=('HYWenHei', 12))
report_type_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="e")

report_type_var = tki.StringVar()
report_type_menu = ttk.Combobox(bottom, textvariable=report_type_var, font=('HYWenHei', 12), state='readonly', width=20)
report_type_menu['values'] = ("Сводная таблица", "Частотный анализ для переменной 'Сет артефакта'", "Частотный анализ для переменной 'Вид артефакта'", "Артефакты персонажей")  # Add available report types
report_type_menu.current(0)  # Set default report type
report_type_menu.bind("<<ComboboxSelected>>", select_report_type)
report_type_menu.grid(row=0, column=1, columnspan=3, padx=(0, 10), pady=10, sticky="we")

# Adding generate button for creating a text report
generate_btn = ttk.Button(bottom, text='Создать текстовый отчет', style="TButton", command=generate_report)
generate_btn.grid(row=0, column=4, columnspan=2, padx=(5, 10), pady=10, sticky="we")

# Adding control buttons
btn_3 = ttk.Button(bottom, text='Сохранить в Excel', style="TButton", command=store_excel)
btn_3.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=10, sticky="we")

btn_4 = ttk.Button(bottom, text='Сохранить в CSV', style="TButton", command=store_text)
btn_4.grid(row=1, column=2, columnspan=2, padx=(5, 5), pady=10, sticky="we")

btn_5 = ttk.Button(bottom, text='Завершить', style="TButton", command=root.destroy)
btn_5.grid(row=1, column=4, columnspan=2, padx=(5, 10), pady=10, sticky="we")

# Adding dropdown menus for separator and decimal separator
separator_label = ttk.Label(bottom, text="Разделитель CSV:", font=('HYWenHei', 12))
separator_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="e")

separator_var = tki.StringVar()
separator_menu = ttk.Combobox(bottom, textvariable=separator_var, font=('HYWenHei', 12), state='readonly', width=5)
separator_menu['values'] = (',', ';', '\t')  # Add available separators
separator_menu.current(0)  # Set default separator to comma
separator_menu.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")

decimal_label = ttk.Label(bottom, text="Десятичный разделитель CSV:", font=('HYWenHei', 12))
decimal_label.grid(row=2, column=2, padx=(10, 0), pady=10, sticky="e")

decimal_var = tki.StringVar()
decimal_menu = ttk.Combobox(bottom, textvariable=decimal_var, font=('HYWenHei', 12), state='readonly', width=5)
decimal_menu['values'] = ('.', ',')  # Add available decimal separators
decimal_menu.current(0)  # Set default decimal separator to dot
decimal_menu.grid(row=2, column=3, padx=(0, 10), pady=10, sticky="w")

tki.mainloop()
