
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and save dictionaries
artifacts = pd.read_csv('Data/artifacts.csv')
characters = pd.read_csv('Data/characters.csv')
rarities = pd.read_csv('Data/rarities.csv')

artifacts.to_pickle('Data/artifacts.pckl')
characters.to_pickle('Data/characters.pckl')
rarities.to_pickle('Data/rarities.pckl')

exps_3star = pd.read_excel("Data/3star.xlsx")
exps_4star = pd.read_excel("Data/4star.xlsx")
exps_5star = pd.read_excel("Data/5star.xlsx")

exps_3star.to_pickle('Data/exps_3star.pckl')
exps_4star.to_pickle('Data/exps_4star.pckl')
exps_5star.to_pickle('Data/exps_5star.pckl')

def calculate_required_exp(current, max_level):
    if max_level <= 12:
        exps = pd.read_pickle('Data/exps_3star.pckl')
    elif max_level <= 16:
        exps = pd.read_pickle('Data/exps_4star.pckl')
    else:
        exps = pd.read_pickle('Data/exps_5star.pckl')

    total_exp = 0
    for i in range(current, max_level):  # Calculate up to max level (exclusive)
        exp = exps.iloc[i - 1, 1]  
        total_exp += exp
        
    return total_exp

def generate_text_report(data: pd.DataFrame, reference_tables: dict, row_criteria: dict, columns: list) -> pd.DataFrame:
    # Merge reference tables using correct ID columns (assuming they exist)
    for ref_name, ref_df in reference_tables.items():
        print(f"{ref_name}:")
        print(ref_df.head())  # Print first few rows to inspect columns
        print(ref_df.columns)  # Print column names
        
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
    
    plt.savefig(filename)
    plt.close()
    
    
# Load data from pickle files
artifacts = pd.read_pickle('Data/artifacts.pckl')
characters = pd.read_pickle('Data/characters.pckl')
rarities = pd.read_pickle('Data/rarities.pckl')

# Merge data and perform calculations
data = pd.merge(artifacts, characters, left_on='id персонажа, исп. артефакт', right_on='id персонажа', how='left')
data['Редкость артефакта'] = data['Редкость артефакта'].astype('int64')  # Ensure numeric type for calculations 
data = pd.merge(data, rarities, on='Редкость артефакта', how='left')  # Merge on rarity
data = data.rename(columns={'Максимально возможный уровень артефакта': 'max_level'})  # Rename for convenience
data['Требуемый опыт'] = data.apply(lambda row: calculate_required_exp(row['Текущий уровень'], row['max_level']), axis=1)

# Generate text report
row_criteria = {'Сет артефакта': 'Берсерк', 'Редкость артефакта': 4}
columns = ['Название артефакта', 'Текущий уровень', 'Требуемый опыт']
reference_tables = {'characters': characters, 'rarities': rarities}
text_report = generate_text_report(data, reference_tables, row_criteria, columns)
print("Текстовый отчет:")
print(text_report)

# Generate pivot table
index = ['Сет артефакта']
columns = ['Вид артефакта']
values = 'Требуемый опыт'
aggfunc = 'sum'
pivot_table = generate_pivot_table(data, index, columns, values, aggfunc)
print("Сводная таблица:")
print(pivot_table)

# Generate statistical report for qualitative variables
qualitative_vars = ['Сет артефакта', 'Вид артефакта']
for var in qualitative_vars:
    freq_table = data[var].value_counts().reset_index()
    freq_table.columns = [var, 'Frequency']
    freq_table['Percentage'] = freq_table['Frequency'] / len(data) * 100
    print(f"Статистический отчет для качественной переменной '{var}':")
    print(freq_table)

# Generate statistical report for quantitative variables
quantitative_vars = ['Текущий уровень', 'Требуемый опыт']
stats_table = data[quantitative_vars].describe().T
print("Статистический отчет для количественных переменных:")
print(stats_table)

# Generate clustered bar chart
generate_chart(data, 'bar', 'Сет артефакта', 'Требуемый опыт', hue='Редкость артефакта', title='Распределение требуемого опыта по сетам и редкости артефактов', filename='bar_set_rarity_required_exp.png')

# Generate categorized histogram
generate_chart(data, 'hist', 'Требуемый опыт', None, hue='Сет артефакта', title='Распределение требуемого опыта по сетам артефактов', filename='hist_set_required_exp.png')
# Generate categorized box plot
generate_chart(data, 'boxplot', 'Сет артефакта', 'Требуемый опыт', title='Распределение требуемого опыта по сетам артефактов', filename='boxplot_set_required_exp.png')

# Generate categorized scatter plot
generate_chart(data, 'scatter', 'Текущий уровень', 'Требуемый опыт', hue='Сет артефакта', title='Зависимость требуемого опыта от уровня артефакта по сетам', filename='scatter_level_required_exp_set.png')
