# -*- coding: utf-8 -*-
"""
Работа с таблицами
Автор: Поляков К. Л.
"""

import numpy as np
import pandas as pd
import tkinter as tki
from tkinter import ttk
from tkinter import filedialog as fld
import argparse

# Function to clear the 'top' frame
def clear_top():
    """
    Очистка фрейма top
    """
    for widgets in top.winfo_children():
       widgets.destroy()

# Function to read data from Pickle file
def read_data(pickle_file_path):
    """
    Чтение и демонстрация данных
    """
    global GDS, height, width, top, vrs, pnt
    GDS = pd.read_pickle(pickle_file_path)
    height = GDS.shape[0]
    width = GDS.shape[1]
    
    # Clear existing widgets
    clear_top()
    
    # Display column headers
    headers = GDS.columns
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

# Function to save data to Excel file
def store_excel():
    """
    Получение даных таблицы из Tcl/Tk
    с помощью метода get() и сохранение в Excel
    """
    ftypes = [('Excel файлы', '*.xlsx'), ('Все файлы', '*')]
    dlg = fld.SaveAs(filetypes=ftypes)
    fl = dlg.show()
    for i in range(height): 
        for j in range(width): 
            GDS.iloc[i, j] = pnt[i, j].get()
    GDS.to_excel(fl, index=False)

# Function to save data to Pickle file
def store_pic():
    """
    Получение даных таблицы из Tcl/Tk
    с помощью метода get() и сохранение в pickle
    """
    for i in range(height): 
        for j in range(width): 
            if pnt[i, j].winfo_exists():  # Check if the widget exists
                GDS.iloc[i, j] = pnt[i, j].get()
    GDS.to_pickle(pickle_file_path)  # Save to the original Pickle file

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

# Function to delete the selected row
def delete_row():
    """
    Удаление выбранной строки из таблицы
    """
    global GDS, height, width, top, vrs, pnt, selected_row
    if selected_row is not None:
        row_index = selected_row - 1  # Adjust for header row
        GDS = GDS.drop(GDS.index[row_index]).reset_index(drop=True)
        height = GDS.shape[0]
        width = GDS.shape[1]
        vrs = np.delete(vrs, row_index, axis=0)
        for j in range(width):
            if pnt[row_index, j].winfo_exists():
                pnt[row_index, j].destroy()
        pnt = np.delete(pnt, row_index, axis=0)
        for i in range(row_index, height):
            for j in range(width):
                pnt[i, j].grid(row=i+1, column=j)
        selected_row = None

# Function to add a new row to the table
def add_row():
    """
    Добавление новой строки в таблицу
    """
    global GDS, height, width, top, vrs, pnt
    new_row = pd.DataFrame([['' for _ in range(width)]], columns=GDS.columns)
    GDS = pd.concat([GDS, new_row], ignore_index=True)
    height = GDS.shape[0]
    width = GDS.shape[1]
    new_vrs = np.empty(shape=(1, width), dtype="O")
    for j in range(width):
        new_vrs[0, j] = tki.StringVar()
    vrs = np.concatenate((vrs, new_vrs), axis=0)
    new_pnt = np.empty(shape=(1, width), dtype="O")
    for j in range(width):
        new_pnt[0, j] = tki.Entry(top, textvariable=vrs[height-1, j], bg='#FAF7DF', font=('HYWenHei', 10))
        new_pnt[0, j].grid(row=height, column=j)
    pnt = np.concatenate((pnt, new_pnt), axis=0)

# Setting up the main Tkinter window
hex_color = "#00FFFF"  # Define color in hex format

GDS = pd.DataFrame([])
height = GDS.shape[0]
width = GDS.shape[1]
pnt = np.empty([])
vrs = np.empty([])
top = []
pickle_file_path = None  # Initialize the variable to store the Pickle file path

# Построение изображения
root = tki.Tk()

# Построение таблицы
top = tki.LabelFrame(root, text="Таблица артефактов", bg='#EF9B6C', font=('HYWenHei', 12))
top.grid(column=0, row=0)
bottom = tki.LabelFrame(root, text="Управление", bg='#D0F69F', font=('HYWenHei', 12))
bottom.grid(column=0, row=1, sticky="we")  # Add sticky="we" to expand the bottom frame

# Set the weight of the column to allow the bottom frame to expand
root.grid_columnconfigure(0, weight=1)

# Create a style for the buttons
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Adding buttons with their respective functionalities
btn_0 = ttk.Button(bottom, text='Добавить строку', style="TButton", command=add_row)
btn_0.grid(row=0, column=0)
btn_1 = ttk.Button(bottom, text='Удалить строку', style="TButton", command=delete_row)
btn_1.grid(row=0, column=1)
btn_2 = ttk.Button(bottom, text='Очистить таблицу', style="TButton", command=clear_top)
btn_2.grid(row=0, column=2)
btn_3 = ttk.Button(bottom, text='Сохранить в Excel', style="TButton", command=store_excel)
btn_3.grid(row=0, column=3)
btn_4 = ttk.Button(bottom, text='Сохранить в Pickle', style="TButton", command=store_pic)
btn_4.grid(row=0, column=4)
btn_5 = ttk.Button(bottom, text='В меню', style="TButton", command=root.destroy)
btn_5.grid(row=0, column=5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display and edit a table from a Pickle file.")
    parser.add_argument("pickle_file_path", help="Path to the Pickle file")
    args = parser.parse_args()

    pickle_file_path = args.pickle_file_path

    # Read data from the specified Pickle file path on startup
    read_data(pickle_file_path)

    tki.mainloop()
