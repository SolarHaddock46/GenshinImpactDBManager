import pandas as pd
import matplotlib.pyplot as plt

def calculateExpToMax(current, rarity):
    if rarity == 3:
        exps = pd.read_excel("3star.xlsx")
    elif rarity == 4:
        exps = pd.read_excel("4star.xlsx")
    elif rarity == 5:
        exps = pd.read_excel("5star.xlsx")
    else:
        raise ValueError("Invalid rarity. Rarity should be 3, 4, or 5.")

    exps.to_pickle('exps.pckl')

    total_exp = 0
    for i in range(current, rarity * 4):
        exp = exps.iloc[i - 1, 1]  
        total_exp += exp
        
    return total_exp


