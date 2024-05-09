"""

ДЗ2

Программа составляет текстовые и графические отчеты на основе данных из ДЗ1.
Текстовые отчеты сохраняются в папку Output.
Графические отчеты сохраняются в папку Graphics.

Для генерации pickle-файлов необходимо запустить скрипт pickle_maker.py.

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_required_exp(current, max_level):
    """
    Вычисляет требуемый опыт для повышения уровня артефакта с текущего до максимального.

    Parameters
    ----------
    current : int
        Текущий уровень артефакта.
    max_level : int
        Максимальный уровень артефакта.

    Returns
    -------
    total_exp : int
        Общий требуемый опыт для повышения уровня артефакта.
    """
    if max_level <= 12:
        exps = pd.read_pickle('../Data/exps_3star.pckl')
    elif max_level <= 16:
        exps = pd.read_pickle('../Data/exps_4star.pckl')
    else:
        exps = pd.read_pickle('../Data/exps_5star.pckl')

    total_exp = 0
    for i in range(current, max_level):
        exp = exps.iloc[i - 1, 1]
        total_exp += exp

    return total_exp


def generate_text_report(data: pd.DataFrame, reference_tables: dict,
                         row_criteria: dict, columns: list) -> pd.DataFrame:
    """
    Генерирует текстовый отчет на основе заданных критериев и столбцов.

    Parameters
    ----------
    data : pd.DataFrame
        Исходный DataFrame с данными.
    reference_tables : dict
        Словарь с референсными таблицами для объединения данных.
    row_criteria : dict
        Словарь с критериями для фильтрации строк.
    columns : list
        Список столбцов для включения в отчет.

    Returns
    -------
    report : pd.DataFrame
        DataFrame с отфильтрованными и выбранными данными для отчета.
    """
    for ref_name, ref_df in reference_tables.items():
        if ref_name == 'characters':
            data = pd.merge(data, ref_df, left_on='id персонажа, исп. артефакт',
                            right_on='id персонажа', how='left')
        else:
            data = pd.merge(data, ref_df, on='Редкость артефакта', how='left')

    mask = True
    for col, val in row_criteria.items():
        if isinstance(val, list):
            mask &= data[col].between(val[0], val[1])
        else:
            mask &= (data[col] == val)

    report = data.loc[mask, columns]
    return report


def generate_pivot_table(data: pd.DataFrame, index: list, columns: list,
                         values: str, aggfunc) -> pd.DataFrame:
    """
    Генерирует сводную таблицу на основе заданных параметров.

    Parameters
    ----------
    data : pd.DataFrame
        Исходный DataFrame с данными.
    index : list
        Список столбцов для использования в качестве индексов.
    columns : list
        Список столбцов для использования в качестве столбцов.
    values : str
        Имя столбца для агрегации значений.
    aggfunc : function
        Функция агрегации для применения к значениям.

    Returns
    -------
    pivot_table : pd.DataFrame
        Сгенерированная сводная таблица.
    """
    pivot_table = pd.pivot_table(
        data, index=index, columns=columns, values=values, aggfunc=aggfunc)
    pivot_table = pivot_table.fillna('-')
    return pivot_table


def generate_chart(data: pd.DataFrame, chart_type: str, x: str, y: str, **kwargs):
    """
    Генерирует диаграмму на основе заданных параметров.

    Parameters
    ----------
    data : pd.DataFrame
        Исходный DataFrame с данными.
    chart_type : str
        Тип диаграммы
        (scatter, boxplot, bar, line, heatmap, pairplot, violinplot, regplot,
        lmplot, hist).
    x : str
        Имя столбца для оси x.
    y : str
        Имя столбца для оси y.
    **kwargs : dict
        Дополнительные именованные аргументы для настройки диаграммы.

    Raises
    ------
    ValueError
        Если указан неподдерживаемый тип диаграммы.

    Returns
    -------
    None
    """
    # Настройка параметров диаграммы
    title = kwargs.pop('title', '')
    xlabel = kwargs.pop('xlabel', x)
    ylabel = kwargs.pop('ylabel', y)
    filename = kwargs.pop('filename', f'{chart_type}_chart.png')

    # Генерация диаграммы в зависимости от типа
    if chart_type == 'scatter':
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=x, y=y, **kwargs)
    elif chart_type == 'boxplot':
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=data, x=x, y=y, **kwargs)
    elif chart_type == 'bar':
        plt.figure(figsize=(10, 6))
        sns.barplot(data=data, x=x, y=y, **kwargs)
    elif chart_type == 'line':
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=data, x=x, y=y, **kwargs)
    elif chart_type == 'heatmap':
        plt.figure(figsize=(10, 8))
        pivot_data = data.pivot_table(index=kwargs.get('index'), columns=kwargs.get(
            'columns'), values=kwargs.get('values'), aggfunc=kwargs.get('aggfunc', 'mean'))
        sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', **kwargs)
    elif chart_type == 'pairplot':
        sns.pairplot(data, vars=kwargs.get('vars'), hue=kwargs.get(
            'hue'), diag_kind=kwargs.get('diag_kind', 'auto'), **kwargs)
        filename = f"pairplot_{kwargs.get('hue', '')}.png"
    elif chart_type == 'violinplot':
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=data, x=x, y=y, **kwargs)
    elif chart_type == 'regplot':
        plt.figure(figsize=(10, 6))
        sns.regplot(data=data, x=x, y=y, **kwargs)
    elif chart_type == 'lmplot':
        sns.lmplot(data=data, x=x, y=y, **kwargs)
        filename = f"lmplot_{x}_{y}.png"
    elif chart_type == 'hist':
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data, x=x, **kwargs)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    # Форматирование осей и расположения текста
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    # Сохранение в файл
    plt.savefig(f'../Graphics/{filename}')
    plt.close()


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
data['Требуемый опыт'] = data.apply(lambda row: calculate_required_exp(
    row['Текущий уровень'], row['Максимально возможный уровень артефакта']), axis=1)

# Генерация и сохранение в файл текстового отчета
row_criteria = {'Сет артефакта': 'Хроники Чертогов в пустыне'}
columns = ['Название артефакта', 'Текущий уровень', 'Требуемый опыт']
reference_tables = {'characters': characters, 'rarities': rarities}
text_report = generate_text_report(
    data, reference_tables, row_criteria, columns)
with open('../Output/text_report.txt', 'w', encoding='utf-8') as f:
    f.write("Текстовый отчет:\n")
    f.write(text_report.to_string(index=False))

# Генерация и сохранение сводной таблицы для анализа
# требуемого опыта в разрезе сетов и видов артефактов
index = ['Сет артефакта']
columns = ['Вид артефакта']
values = 'Требуемый опыт'
aggfunc = 'sum'
pivot_table = generate_pivot_table(data, index, columns, values, aggfunc)
with open('../Output/pivot_table.txt', 'w', encoding='utf-8') as f:
    f.write("Сводная таблица:\n")
    f.write(pivot_table.to_string())

# Формирование статистических отчетов для качественных переменных
qualitative_vars = ['Сет артефакта', 'Вид артефакта']
for var in qualitative_vars:
    freq_table = data[var].value_counts().reset_index()
    freq_table.columns = [var, 'Частота']
    freq_table['Доля в %'] = freq_table['Частота'] / len(data) * 100
    with open(f'../Output/freq_table_{var}.txt', 'w', encoding='utf-8') as f:
        f.write(f"Статистический отчет для качественной переменной '{var}':\n")
        f.write(freq_table.to_string(index=False))

# Генерация и сохранение отчета о всех артефактах, экипированного на каждого персонажа
character_artifacts = data.groupby('Имя персонажа')[
    'Название артефакта'].apply(list).reset_index()
with open('../Output/character_artifacts.txt', 'w', encoding='utf-8') as f:
    f.write("Отчет об артефактах, экипированных на каждого персонажа:\n")
    f.write(character_artifacts.to_string(index=False))
    
print('Текстовые отчеты сгенерированы и записаны в папку Output')

# Генерация различных графиков для визуализации данных
generate_chart(data, 'bar', 'Сет артефакта', 'Требуемый опыт',
               hue='Редкость артефакта',
               title='Распределение требуемого опыта по сетам и редкости артефактов',
               filename='bar_set_rarity_required_exp.png')

generate_chart(data, 'hist', 'Текущий уровень', None, bins=20,
               title='Распределение текущих уровней артефактов',
               filename='hist_current_level.png')

generate_chart(data, 'boxplot', 'Вид артефакта', 'Текущий уровень',
               title='Распределение текущих уровней по видам артефактов',
               filename='boxplot_type_current_level.png')

generate_chart(data, 'scatter', 'Редкость артефакта', 'Текущий уровень',
               title='Зависимость текущего уровня артефактов от их редкости',
               filename='scatter_rarity_current_level.png')

# Генерация графика суммарного требуемого опыта для возвышения артефактов каждого персонажа
character_total_exp = data.groupby('Имя персонажа')[
    'Требуемый опыт'].sum().reset_index()
generate_chart(character_total_exp, 'bar', 'Имя персонажа', 'Требуемый опыт',
               title='Требуемый опыт для возвышения артефактов каждого персонажа',
               filename='bar_character_total_required_exp.png')

print('Графические отчеты сгенерированы и записаны в папку Graphics')
