"""
Генерация и просмотр графических отчетов
"""
import tkinter as tki
from tkinter import ttk
from PIL import Image, ImageTk
import report_creator


def clear_top():
    """
    Очищает верхний фрейм от всех виджетов.

    Returns
    -------
    None.

    """
    for widgets in top.winfo_children():
        widgets.destroy()


def read_image(img_file_path):
    """
    Отображает изображение в верхнем фрейме.

    Parameters
    ----------
    img_file_path : str
        Путь к файлу изображения.

    Returns
    -------
    None.

    """
    global img_label
    if not img_file_path:
        return

    clear_top()

    img = Image.open(img_file_path)
    img = ImageTk.PhotoImage(img)

    img_label = tki.Label(top, image=img)
    img_label.image = img
    img_label.grid(row=0, column=0)


def select_report_type(event):
    """
    Обрабатывает выбор типа отчета из выпадающего меню.

    Parameters
    ----------
    event : tkinter.Event
        Событие выбора элемента из выпадающего меню.

    Returns
    -------
    None.

    """
    report_type = report_type_var.get()


def generate_report():
    """
    Генерирует выбранный тип отчета и отображает его в верхнем фрейме.

    Returns
    -------
    None.

    """
    report_type = report_type_var.get()
    # Вызов соответствующей функции из report_creator в зависимости от выбранного типа отчета
    data = report_creator.load_data()
    if report_type == "Распределение требуемого опыта по сетам и редкости артефактов":
        filename = 'bar_set_rarity_required_exp.png'
        report_creator.generate_chart(data, 'bar', 'Сет артефакта', 'Требуемый опыт',
                                      hue='Редкость артефакта',
                                      title='Распределение требуемого опыта по сетам и редкости артефактов',
                                      filename=filename)
    elif report_type == "Распределение текущих уровней артефактов":
        filename = 'hist_current_level.png'
        report_creator.generate_chart(data, 'hist', 'Текущий уровень', None,
                                      bins=20,
                                      title='Распределение текущих уровней артефактов',
                                      filename=filename)
    elif report_type == "Распределение текущих уровней по видам артефактов":
        filename = 'boxplot_type_current_level.png'
        report_creator.generate_chart(data, 'boxplot', 'Вид артефакта',
                                      'Текущий уровень',
                                      title='Распределение текущих уровней по видам артефактов',
                                      filename=filename)
    elif report_type == "Зависимость текущего уровня артефактов от их редкости":
        filename = 'scatter_rarity_current_level.png'
        report_creator.generate_chart(data, 'scatter', 'Редкость артефакта',
                                      'Текущий уровень',
                                      title='Зависимость текущего уровня артефактов от их редкости',
                                      filename=filename)
    elif report_type == "Требуемый опыт для возвышения артефактов каждого персонажа":
        filename = 'bar_character_total_required_exp.png'
        character_total_exp = data.groupby('Имя персонажа')[
            'Требуемый опыт'].sum().reset_index()
        report_creator.generate_chart(character_total_exp, 'bar', 'Имя персонажа',
                                      'Требуемый опыт',
                                      title='Требуемый опыт для возвышения артефактов каждого персонажа',
                                      filename=filename)

    read_image(f'../Graphics/{filename}')


# Построение изображения
root = tki.Tk()
root.title("Графические отчеты") 

# Построение фреймов
top = tki.LabelFrame(root, text="Графический отчет",
                     bg='#EF9B6C', font=('HYWenHei', 12))
top.grid(column=0, row=0, padx=10, pady=10)
bottom = tki.LabelFrame(root, text="Управление",
                        bg='#D0F69F', font=('HYWenHei', 12))
# Создание привязки для изменения размера нижнего фрейма при расширении окна
bottom.grid(column=0, row=1, sticky="we", padx=10, pady=10)

# Изменение веса столбца для разрешения расширения
root.grid_columnconfigure(0, weight=1)

# Установка стиля для кнопок
style = ttk.Style()
style.configure("TButton", font=('HYWenHei', 12), background='#B2D15B')

# Добавление выпадающего списка отчетов
report_type_label = ttk.Label(
    bottom, text="Тип отчета:", font=('HYWenHei', 12))
report_type_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="e")

report_type_var = tki.StringVar()
report_type_menu = ttk.Combobox(bottom, textvariable=report_type_var, font=(
    'HYWenHei', 12), state='readonly', width=20)
report_type_menu['values'] = ("Распределение требуемого опыта по сетам и редкости артефактов",
                              "Распределение текущих уровней артефактов",
                              "Распределение текущих уровней по видам артефактов",
                              "Зависимость текущего уровня артефактов от их редкости",
                              "Требуемый опыт для возвышения артефактов каждого персонажа") 
report_type_menu.current(0)  # Первый вариант устанавливается как вариант по умолчанию
report_type_menu.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")
report_type_menu.bind("<<ComboboxSelected>>", select_report_type)

# Создание кнопки генерации отчета
btn_generate = ttk.Button(
    bottom, text='Сгенерировать отчет', style="TButton", command=generate_report)
btn_generate.grid(row=0, column=2, columnspan=2,
                  padx=(5, 10), pady=10, sticky="we")

# Создание кнопки выхода
btn_exit = ttk.Button(bottom, text='В меню',
                      style="TButton", command=root.destroy)
btn_exit.grid(row=0, column=4, columnspan=2,
              padx=(5, 10), pady=10, sticky="we")

tki.mainloop()
