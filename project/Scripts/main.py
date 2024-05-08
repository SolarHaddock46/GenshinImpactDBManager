
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and save dictionaries
artifacts = pd.read_csv('artifacts.csv')
characters = pd.read_csv('characters.csv')
rarities = pd.read_csv('rarities.csv')

artifacts.to_pickle('../Data/artifacts.pckl')
characters.to_pickle('../Data/characters.pckl')
rarities.to_pickle('../Data/rarities.pckl')

exps_3star = pd.read_excel("3star.xlsx")
exps_4star = pd.read_excel("4star.xlsx")
exps_5star = pd.read_excel("5star.xlsx")

exps_3star.to_pickle('../Data/exps_3star.pckl')
exps_4star.to_pickle('../Data/exps_4star.pckl')
exps_5star.to_pickle('../Data/exps_5star.pckl')

def calculate_required_exp(current, max_level):
    if max_level <= 12:
        exps = pd.read_pickle('../Data/exps_3star.pckl')
    elif max_level <= 16:
        exps = pd.read_pickle('../Data/exps_4star.pckl')
    else:
        exps = pd.read_pickle('../Data/exps_5star.pckl')

    total_exp = 0
    for i in range(current, max_level):  # Calculate up to max level (exclusive)
        exp = exps.iloc[i - 1, 1]  
        total_exp += exp
        
    return total_exp

def generate_text_report(data: pd.DataFrame, reference_tables: dict, row_criteria: dict, columns: list) -> pd.DataFrame:
    # Merge reference tables using correct ID columns (assuming they exist)
    for ref_name, ref_df in reference_tables.items():        
        if ref_name == 'characters':
            data = pd.merge(data, ref_df, left_on='id персонажа, исп. артефакт', right_on='id персонажа', how='left')
        else:
            data = pd.merge(data, ref_df, on='Редкость артефакта', how='left')

    # Apply row criteria
    mask = True
    for col, val in row_criteria.items():
        if isinstance(val, list):
            mask &= data[col].between(val[0], val[1])
        else:
            mask &= (data[col] == val)

    report = data.loc[mask, columns]
    return report

def generate_pivot_table(data: pd.DataFrame, index: list, columns: list, values: str, aggfunc) -> pd.DataFrame:
    pivot_table = pd.pivot_table(data, index=index, columns=columns, values=values, aggfunc=aggfunc)
    pivot_table = pivot_table.fillna('-')  # Replace NaN with '-'
    return pivot_table

def generate_chart(data: pd.DataFrame, chart_type: str, x: str, y: str, **kwargs):
    title = kwargs.pop('title', '')
    xlabel = kwargs.pop('xlabel', x)
    ylabel = kwargs.pop('ylabel', y)
    filename = kwargs.pop('filename', f'{chart_type}_chart.png')

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
        pivot_data = data.pivot_table(index=kwargs.get('index'), columns=kwargs.get('columns'), values=kwargs.get('values'), aggfunc=kwargs.get('aggfunc', 'mean'))
        sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', **kwargs)
    elif chart_type == 'pairplot':
        sns.pairplot(data, vars=kwargs.get('vars'), hue=kwargs.get('hue'), diag_kind=kwargs.get('diag_kind', 'auto'), **kwargs)
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
        sns.histplot(data=data, x=x, **kwargs)  # Remove separate 'hue' parameter
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Automatically adjust x-axis labels
    plt.gcf().autofmt_xdate()
    
    # Automatically adjust subplot parameters to fit everything
    plt.tight_layout()
    
    plt.savefig(f'../Output/Plots/{filename}')
    plt.close()
    
    

# Load data from pickle files
artifacts = pd.read_pickle('../Data/artifacts.pckl')
characters = pd.read_pickle('../Data/characters.pckl')
rarities = pd.read_pickle('../Data/rarities.pckl')

# Merge data and perform calculations
data = pd.merge(artifacts, characters, left_on='id персонажа, исп. артефакт', right_on='id персонажа', how='left')
data['Редкость артефакта'] = data['Редкость артефакта'].astype('int64')  # Ensure numeric type for calculations 
data = pd.merge(data, rarities, on='Редкость артефакта', how='left')  # Merge on rarity
data['Требуемый опыт'] = data.apply(lambda row: calculate_required_exp(row['Текущий уровень'], row['Максимально возможный уровень артефакта']), axis=1)

# Generate text report
row_criteria = {'Сет артефакта': 'Берсерк', 'Редкость артефакта': 4}
columns = ['Название артефакта', 'Текущий уровень', 'Требуемый опыт']
reference_tables = {'characters': characters, 'rarities': rarities}
text_report = generate_text_report(data, reference_tables, row_criteria, columns)
with open('../Output/Reports/text_report.txt', 'w', encoding='utf-8') as f:
    f.write("Текстовый отчет:\n")
    f.write(text_report.to_string(index=False))

# Generate pivot table
index = ['Сет артефакта']
columns = ['Вид артефакта']
values = 'Требуемый опыт'
aggfunc = 'sum'
pivot_table = generate_pivot_table(data, index, columns, values, aggfunc)
with open('../Output/Reports/pivot_table.txt', 'w', encoding='utf-8') as f:
    f.write("Сводная таблица:\n")
    f.write(pivot_table.to_string())

# Generate statistical report for qualitative variables
qualitative_vars = ['Сет артефакта', 'Вид артефакта']
for var in qualitative_vars:
    freq_table = data[var].value_counts().reset_index()
    freq_table.columns = [var, 'Частота']
    freq_table['Доля в %'] = freq_table['Частота'] / len(data) * 100
    with open(f'../Output/Reports/freq_table_{var}.txt', 'w', encoding='utf-8') as f:
        f.write(f"Статистический отчет для качественной переменной '{var}':\n")
        f.write(freq_table.to_string(index=False))

# Generate report of artifacts equipped on each character
character_artifacts = data.groupby('Имя персонажа')['Название артефакта'].apply(list).reset_index()
with open('../Output/Reports/character_artifacts.txt', 'w', encoding='utf-8') as f:
    f.write("Отчет об артефактах, экипированных на каждого персонажа:\n")
    f.write(character_artifacts.to_string(index=False))

# Generate clustered bar chart
generate_chart(data, 'bar', 'Сет артефакта', 'Требуемый опыт', hue='Редкость артефакта', title='Распределение требуемого опыта по сетам и редкости артефактов', filename='bar_set_rarity_required_exp.png')

# Generate categorized histogram
generate_chart(data, 'hist', 'Текущий уровень', None, bins=20, title='Распределение текущих уровней артефактов', filename='hist_current_level.png')
# Generate categorized box plot
generate_chart(data, 'boxplot', 'Вид артефакта', 'Текущий уровень', title='Распределение текущих уровней по видам артефактов', filename='boxplot_type_current_level.png')
# Generate categorized scatter plot
generate_chart(data, 'scatter', 'Редкость артефакта', 'Текущий уровень', title='Зависимость текущего уровня от редкости артефакта', filename='scatter_rarity_current_level.png')
# Calculate total required experience for each character
character_total_exp = data.groupby('Имя персонажа')['Требуемый опыт'].sum().reset_index()

# Generate bar plot
generate_chart(character_total_exp, 'bar', 'Имя персонажа', 'Требуемый опыт', title='Требуемый опыт для возвышения артефактов по персонажам', filename='bar_character_total_required_exp.png')