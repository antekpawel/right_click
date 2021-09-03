import re
import sys
import pandas as pd
pd.options.mode.chained_assignment = None

# filename = (sys.argv[1])
# filename = filename.replace('\\', '/').replace('"', '')
filename = 'xxx.txt'
tags = pd.read_csv(filename, delimiter="\t")
sort_list = []
sort_add = ''

while True:
    val = input("Wpisz kolejność numerowania.\n"
                "Wpisz kolejno kilka typów, aby uzyskac sortowanie piętrowe\n"
                "([1] Type, [2] Area, [3] Medium, [h] help): ")\
        .replace(',', '').replace(' ', '')\
        .replace('Type', '1').replace('TYPE', '1').replace('type', '1')\
        .replace('Area', '2').replace('AREA', '2').replace('area', '2')\
        .replace('Medium', '3').replace('MEDIUM', '3').replace('medium', '3')

    if val.upper() == 'H' or val.upper() == 'HELP':
        print('\nPodaj numer lub nazwę kolumny, po której chcesz posortować dokument.\n'
              'Podanie kilku adresów kolumn w jednym ciągu spowoduje\n'
              'sortowanie po nich kolejno zgodnie z podaną kolejnością.\n'
              'Podanie nieprawidłowych danych \n'
              'wywoła wyświetlenie się komunikatu i ponowne zapytanie.\n'
              '\nProgram służy do automatycznego i bezbłędnego ponumerowania pliku z atrybutami\n'
              'z programu GStarCAD.\n')
    elif 4 > len(val) and re.search(re.compile('^[123]+$'), val):
        for c in val:
            if c == '1':
                sort_add = 'TYPE'
            elif c == '2':
                sort_add = 'AREA'
            elif c == '3':
                sort_add = 'MEDIUM'
            sort_list.append(sort_add)
        sorted_tags = tags.sort_values(sort_list, ignore_index=True)
        break
    else:
        print('Nieprawidłowa dana wejściowa')

sorted_tags['TYPE'] = sorted_tags['TYPE'].str.replace('\d+', '')
dzban = sorted_tags[sort_add][0]
iterator = 1
sorted_tags['NUMBER'] = 0
sorted_tags['NUMBER'] = sorted_tags['NUMBER'].astype('int32')

for index, row in sorted_tags.iterrows():
    if row[sort_add] == dzban:
        sorted_tags['NUMBER'][index] = iterator
        iterator = iterator + 1
    else:
        iterator = 1
        sorted_tags['NUMBER'][index] = iterator
        dzban = row['TYPE']
sorted_tags['NUMBER'] = sorted_tags['NUMBER'].astype('str')

for index, row in sorted_tags.iterrows():
    sorted_tags['TYPE'][index] = sorted_tags['TYPE'][index] + (3 - len(sorted_tags['NUMBER'][index])) * '0' + \
                                 sorted_tags['NUMBER'][index]
sorted_tags = sorted_tags.drop(columns=['NUMBER'])

sorted_tags.to_csv('ponumerowane.txt', header=True, index=None, sep='\t', mode='w')
sorted_tags.to_excel('ponumerowane.xlsx')
