import json

with open('cenzura.txt', encoding='utf-8') as file:
    cenz_list = list(set([word.lower().split('\n')[0] for word in file]))[1:]

with open('cenzura.json', 'w', encoding='utf-8') as cenz_file:
    json.dump(cenz_list, cenz_file)
