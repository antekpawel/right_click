import math
import re
import sys
import pandas as pd
from pathlib import Path

pd.options.mode.chained_assignment = None


def print_tag_no(column, tag_name):
    no = sum(sorted_tags[column] == tag_name)
    print('Liczba ' + tag_name + f': {no}')

def print_help():
    return print(
        '\nPodaj numer lub nazwę kolumny, po której chcesz posortować dokument.\n'
        'Podanie kilku adresów kolumn w jednym ciągu spowoduje\n'
        'sortowanie po nich kolejno zgodnie z podaną kolejnością.\n'
        'Podanie nieprawidłowych danych \n'
        'wywoła wyświetlenie się komunikatu i ponowne zapytanie.\n'
        '\nProgram służy do automatycznego i bezbłędnego ponumerowania pliku z atrybutami\n'
        'z programu GStarCAD.\n'
    )


# Wczytanie pliku
try:
    filename = (sys.argv[1])
    filename = filename.replace('\\', '/').replace('"', '')
except IndexError:
    filename = 'xxx.txt'

tags = pd.read_csv(filename, delimiter="\t")
sort_list = []
sort_add = ''

# Wczytanie kolejności sortowania
while True:
    val = input("Wpisz kolejność numerowania.\n"
                "Wpisz kolejno kilka typów, aby uzyskac sortowanie piętrowe\n"
                "([1] Type, [2] Area, [3] Medium, [h] help): ") \
        .replace(',', '').replace(' ', '') \
        .replace('Type', '1').replace('TYPE', '1').replace('type', '1') \
        .replace('Area', '2').replace('AREA', '2').replace('area', '2') \
        .replace('Medium', '3').replace('MEDIUM', '3').replace('medium', '3')

    if val.upper() == 'H' or val.upper() == 'HELP':
        print_help()
        continue

    if len(val) > 4 or not re.search(re.compile('^[123]+$'), val):
        print('Nieprawidłowa dana wejściowa')
        print_help()
        continue

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


# Usunięcie niepotrzebnych znaków
sorted_tags['TYPE'] = sorted_tags['TYPE'].str.replace('\d+', '', regex=True)
sorted_tags['TYPE'] = sorted_tags['TYPE'].str.replace('-', '', regex=True)

# Lista pomiarów nieciągłych
tag_tri_mesurement_no = (sum(sorted_tags['TYPE'] == 'FIT') +
                         sum(sorted_tags['TYPE'] == 'HLT') +
                         sum(sorted_tags['TYPE'] == 'LLT') +
                         sum(sorted_tags['TYPE'] == 'MLT') +
                         sum(sorted_tags['TYPE'] == 'ICO') +
                         sum(sorted_tags['TYPE'] == 'ISO'))

# Zmienne do sortowania
sorted_tags["merged_text"] = ""
for tag in reversed(sort_list):
    sorted_tags["merged_text"] += sorted_tags[tag]

dzban = sorted_tags['merged_text'][0]
iterator = 1
sorted_tags['NUMBER'] = 0
sorted_tags['NUMBER'] = sorted_tags['NUMBER'].astype('int32')

# Sortowanie
for index, row in sorted_tags.iterrows():
    if row['merged_text'] == dzban:
        sorted_tags['NUMBER'][index] = iterator
        iterator = iterator + 1
    else:
        iterator = 1
        dzban = row['merged_text']
        sorted_tags['NUMBER'][index] = iterator
        iterator = iterator + 1
max_iter = max(sorted_tags['NUMBER'])
sorted_tags['NUMBER'] = sorted_tags['NUMBER'].astype('str')

number_of_numbers = int(math.log10(max_iter))+1
for index, row in sorted_tags.iterrows():
    sorted_tags['TYPE'][index] = sorted_tags['TYPE'][index] + \
                                 (int(number_of_numbers) - len(sorted_tags['NUMBER'][index])) * '0' + \
                                 sorted_tags['NUMBER'][index]
sorted_tags = sorted_tags.drop(columns=['NUMBER'])
sorted_tags = sorted_tags.drop(columns=['merged_text'])

print('\nKilka końcowych wartośći do sprawdzenia:')
print(sorted_tags.tail())
print('\n')

filename_name = Path(filename).stem
sorted_tags.to_csv('ponumerowane_' + filename_name + '.txt', header=True, index=None, sep='\t', mode='w')

sorted_tags['PN'] = ''
sorted_tags['Rozmiar przyłącza'] = ''
sorted_tags['Rodzaj przyłącza'] = ''
sorted_tags['Materiał'] = ''
sorted_tags['Uszczelnienie'] = ''
sorted_tags['Uwagi'] = ''

sorted_tags.to_excel('ponumerowane_' + filename_name + '.xlsx')

print_tag_no('BLOCKNAME', 'Tag  Manual')
print_tag_no('BLOCKNAME', 'Tag Automat')

tag_con_mesurement_no = (sum(sorted_tags['BLOCKNAME'] == 'Tag Automat')) - tag_tri_mesurement_no
print(f'Liczba pomiarów nieciągłych: {tag_tri_mesurement_no}')
print(f'Liczba pomiarów    ciągłych: {tag_con_mesurement_no}')
print("UWAGA!!! Liczba pomiarów nieciągłych obliczana jest na podstawie ilości czujników o oznaczeniach: \n"
      "FIT, HLT, MLT, LLT, ICO, ISO. Liczba pomiarów ciągłych jest obliczana z różnicy wszystkich czujników \n"
      "i nieciągłych W przypadku, gdy dojdą czujniki nieciągłe o innych oznaczeniach należy je dopisać\n"
      "w kodzie programu. \n ")

filename_old = input("Podaj nazwe starego pliku bez rozszerzenia lub zatwierdź przyciskiem enter: ")

try:
    with open(filename_old + '.xlsx', encoding='utf-8', errors='ignore') as f:
        ideal_gas_data = pd.read_excel(filename_old + ".xlsx", index_col=0)
except IOError:
    if filename_old != "":
        print('Nie udało się otworzyc pliku!')
    else:
        print('A chuj Ci w dupe stary, ja tu funkcję tworzę, a Ty nie korzystasz!')
    input("Nacisnij Enter by wyjść.")

for index1, row1 in sorted_tags.iterrows():
    for index2, row2 in ideal_gas_data.iterrows():
        if sorted_tags['HANDLE'][index1] == ideal_gas_data['HANDLE'][index2]:
            sorted_tags['PN'][index1] = ideal_gas_data['PN'][index2]
            sorted_tags['Rozmiar przyłącza'][index1] = ideal_gas_data['Rozmiar przyłącza'][index2]
            sorted_tags['Rodzaj przyłącza'][index1] = ideal_gas_data['Rodzaj przyłącza'][index2]
            sorted_tags['Materiał'][index1] = ideal_gas_data['Materiał'][index2]
            sorted_tags['Uszczelnienie'][index1] = ideal_gas_data['Uszczelnienie'][index2]
            sorted_tags['Uwagi'][index1] = ideal_gas_data['Uwagi'][index2]

sorted_tags.to_excel('ponumerowane_' + filename_name + '_nowe.xlsx')

input("Nacisnij Enter by wyjść.")
