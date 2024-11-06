import pandas as pd
import folium
import glob
import os

def dedectFlood(group):
    group = group.reset_index(drop=True)
    min = group['stan aktualny'].min()
    max = group['stan aktualny'].max()
    highestLevelIndex = group['stan aktualny'].idxmax()

    if max < min+100:
        return False

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
waterLevelsData['dlugosc geo'] = pd.to_numeric(waterLevelsData['dlugosc geo'])


results = waterLevelsData.groupby('nazwa stacji').filter(dedectFlood)
results = results.reset_index(drop=True)#.drop(columns=['czas pomiaru'])
results = results.sort_values(['nazwa stacji', 'czas pomiaru'])


for index, result in results.iterrows():
    if index == 0:
        map = folium.Map(location=[result['szerokosc geo'], result['dlugosc geo']])
        
    folium.Marker(location=[result['szerokosc geo'], result['dlugosc geo']], popup = result['nazwa stacji']).add_to(map)

map.save("map.html")


print(results)