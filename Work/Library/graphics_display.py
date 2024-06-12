import tkinter as tki
from tkinter import ttk
from PIL import Image, ImageTk
import report_creator 

# Function to clear the 'top' frame
def clear_top():
    for widgets in top.winfo_children():
        widgets.destroy()

# Function to read and display an image file
def read_image(img_file_path):
    global img_label, top
    
    if not img_file_path:
        return
    
    clear_top()
    
    img = Image.open(img_file_path)
    # img = img.resize((800, 600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    
    img_label = tki.Label(top, image=img)
    img_label.image = img
    img_label.grid(row=0, column=0)

# Function to handle report type selection
def select_report_type(event):
    report_type = report_type_var.get()
    print(f"Selected report type: {report_type}")

# Function to generate the report based on the selected type
def generate_report():
    report_type = report_type_var.get()
    print(f"Generating report for type: {report_type}")
    
    # Call the appropriate function from report_creator based on the selected report type
    data = report_creator.load_data()
    if report_type == "Распределение требуемого опыта по сетам и редкости артефактов":
        filename = 'bar_set_rarity_required_exp.png'
        report_creator.generate_chart(data, 'bar', 'Сет артефакта', 'Требуемый опыт',
                                      hue='Редкость артефакта',
                                      title='Распределение требуемого опыта по сетам и редкости артефактов',
                                      filename=filename)
    elif report_type == "Распределение текущих уровней артефактов":
        filename = 'hist_current_level.png'
        report_creator.generate_chart(data, 'hist', 'Текущий уровень', None, bins=20,
                                      title='Распределение текущих уровней артефактов',
                                      filename=filename)
    elif report_type == "Распределение текущих уровней по видам артефактов":
        filename = 'boxplot_type_current_level.png'
        report_creator.generate_chart(data, 'boxplot', 'Вид артефакта', 'Текущий уровень',
                                      title='Распределение текущих уровней по видам артефактов',
                                      filename=filename)
    elif report_type == "Зависимость текущего уровня артефактов от их редкости":
        filename = 'scatter_rarity_current_level.png'
        report_creator.generate_chart(data, 'scatter', 'Редкость артефакта', 'Текущий уровень',
                                      title='Зависимость текущего уровня артефактов от их редкости',
                                      filename=filename)
    elif report_type == "Требуемый опыт для возвышения артефактов каждого персонажа":
        filename = 'bar_character_total_required_exp.png'
        character_total_exp = data.groupby('Имя персонажа')['Требуемый опыт'].sum().reset_index()
        report_creator.generate_chart(character_total_exp, 'bar', 'Имя персонажа', 'Требуемый опыт',
                                      title='Требуемый опыт для возвышения артефактов каждого персонажа',
                                      filename=filename)
    
    read_image(f'../Graphics/{filename}')

# Setting up the main Tkinter window
hex_color = "#00FFFF"  # Define color in hex format

# Построение изображения
root = tki.Tk()
root.title("Графические отчеты")  # Set window title

# Построение фреймов
top = tki.LabelFrame(root, text="Графический отчет", bg='#EF9B6C', font=('HYWenHei', 12))
top.grid(column=0, row=0, padx=10, pady=10)
bottom = tki.LabelFrame(root, text="Управление", bg='#D0F69F', font=('HYWenHei', 12))
bottom.grid(column=0, row=1, sticky="we", padx=10, pady=10)  # Add sticky="we" to expand the bottom frame

# Set the weight of the column to allow the bottom frame to expand
root.grid_columnconfigure(0, weight=1)

# Create a style for the buttons
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Adding dropdown menu for report type selection
report_type_label = ttk.Label(bottom, text="Тип отчета:", font=('HYWenHei', 12))
report_type_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="e")

report_type_var = tki.StringVar()
report_type_menu = ttk.Combobox(bottom, textvariable=report_type_var, font=('HYWenHei', 12), state='readonly', width=20)
report_type_menu['values'] = ("Распределение требуемого опыта по сетам и редкости артефактов", "Распределение текущих уровней артефактов", "Распределение текущих уровней по видам артефактов", "Зависимость текущего уровня артефактов от их редкости", "Требуемый опыт для возвышения артефактов каждого персонажа")  # Add available report types
report_type_menu.current(0)  # Set default report type
report_type_menu.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")
report_type_menu.bind("<<ComboboxSelected>>", select_report_type)

# Adding generate button
btn_generate = ttk.Button(bottom, text='Сгенерировать отчет', style="TButton", command=generate_report)
btn_generate.grid(row=0, column=2, columnspan=2, padx=(5, 10), pady=10, sticky="we")

# Adding exit button
btn_exit = ttk.Button(bottom, text='В меню', style="TButton", command=root.destroy)
btn_exit.grid(row=0, column=4, columnspan=2, padx=(5, 10), pady=10, sticky="we")

tki.mainloop()