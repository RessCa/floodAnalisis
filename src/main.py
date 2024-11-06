import pandas as pd
import glob
import os

def dedectFlood(group):
    group = group.reset_index(drop=True)
    highestLevelIndex = group['stan aktualny'].idxmax()

    for i in range(1, len(group)):
        if i <= highestLevelIndex:
            if group['stan aktualny'].iloc[i] < group['stan aktualny'].iloc[i-1]: 
                return False
        elif i > highestLevelIndex:
            if group['stan aktualny'].iloc[i] > group['stan aktualny'].iloc[i-1]:
                return False
            
    return True


folderPath = "data/"

waterLevelsData = []

for filePath in glob.glob(os.path.join(folderPath, "*.csv")):
    with open(filePath, "r", encoding="utf-8") as file:
        next(file)
        for line in file:
            row = line.strip().split(",")
        
            selectedRow = row[:3]
            selectedRow.append(row[4].replace(" cm", ""))
            selectedRow.append(row[6].strip().split(" ")[0])
            selectedRow += row[-2:]

            waterLevelsData.append(selectedRow)


waterLevelsData = pd.DataFrame(waterLevelsData, columns=['numer stacji', 'nazwa stacji', 'rzeka', 'stan aktualny', 'czas pomiaru', 'szerokosc geo', 'dlugosc geo'])
waterLevelsData = waterLevelsData.loc[
        (waterLevelsData['stan aktualny']!='-') &
        (waterLevelsData['rzeka'].str.startswith('Odra'))
    ]


waterLevelsData['stan aktualny'] = pd.to_numeric(waterLevelsData['stan aktualny'])
waterLevelsData['czas pomiaru'] = pd.to_datetime(waterLevelsData['czas pomiaru'])
waterLevelsData['szerokosc geo'] = pd.to_numeric(waterLevelsData['szerokosc geo'])


results = waterLevelsData.groupby('nazwa stacji').filter(dedectFlood).drop_duplicates(subset=['nazwa stacji'])
results = results.reset_index(drop=True).drop(columns=['stan aktualny', 'czas pomiaru', 'szerokosc geo', 'dlugosc geo'])


print(results)