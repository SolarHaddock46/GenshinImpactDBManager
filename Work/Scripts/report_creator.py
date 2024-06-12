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
import os


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
        (scatter, boxplot, bar, hist).
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

def load_data():
    # Load data from pickle files
    artifacts = pd.read_pickle('../Data/artifacts.pckl')
    characters = pd.read_pickle('../Data/characters.pckl')
    rarities = pd.read_pickle('../Data/rarities.pckl')


    # Merge data
    data = pd.merge(artifacts, characters, left_on='id персонажа, исп. артефакт', right_on='id персонажа', how='left')
    data['Редкость артефакта'] = data['Редкость артефакта'].astype('int64')
    data = pd.merge(data, rarities, on='Редкость артефакта', how='left')
    data['Требуемый опыт'] = data.apply(lambda row: calculate_required_exp(row['Текущий уровень'], row['Максимально возможный уровень артефакта']), axis=1)

    return data