"""
Генератор pickle-файлов по исходным данным в файлах Excel и CSV.
"""
import pandas as pd


# Чтение данных из CSV файлов и сохранение их в формате pickle
artifacts = pd.read_csv('artifacts.csv')
characters = pd.read_csv('characters.csv')
rarities = pd.read_csv('rarities.csv')

artifacts.to_pickle('../Data/artifacts.pckl')
characters.to_pickle('../Data/characters.pckl')
rarities.to_pickle('../Data/rarities.pckl')

# Чтение данных из Excel файлов и сохранение их в формате pickle
exps_3star = pd.read_excel("3star.xlsx")
exps_4star = pd.read_excel("4star.xlsx")
exps_5star = pd.read_excel("5star.xlsx")

exps_3star.to_pickle('../Data/exps_3star.pckl')
exps_4star.to_pickle('../Data/exps_4star.pckl')
exps_5star.to_pickle('../Data/exps_5star.pckl')

