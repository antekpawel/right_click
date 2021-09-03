import pandas as pd

filename1 = 'xx.txt'
tags1 = pd.read_csv(filename1, delimiter="\t")

filename2 = 'x.txt'
tags2 = pd.read_csv(filename2, delimiter="\t")

chuj = pd.concat([tags1, tags2]).drop_duplicates(keep=False, ignore_index=True)
tags1['PN'] = 0

for index1, row1 in tags1.iterrows():
    for index2, row2 in tags2.iterrows():
        if tags1['HANDLE'][index1] == tags2['HANDLE'][index2]:
            tags1['PN'][index1] = tags2['PN'][index2]
            tags1['Rozmiar przyłącza'][index1] = tags2['Rozmiar przyłącza'][index2]
            tags1['Rodzaj przyłącza'][index1] = tags2['Rodzaj przyłącza'][index2]
            tags1['Materiał'][index1] = tags2['Materiał'][index2]
            tags1['Uszczelnienie'][index1] = tags2['Uszczelnienie'][index2]
            tags1['Uwagi'][index1] = tags2['Uwagi'][index2]

print(tags1)
