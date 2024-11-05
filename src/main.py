import pandas as pd
import glob
import os

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


##waterLevelsData = waterLevelsData.sort_values(by=['szerokosc geo', 'czas pomiaru'])


avgWaterLevels =  waterLevelsData.groupby('nazwa stacji')['stan aktualny'].mean()


print(avgWaterLevels)
#print(waterLevelsData) 