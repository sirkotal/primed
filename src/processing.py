import csv

data_list = []

with open('./dataset/Medicine_Details.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    for med in csv_reader:
        data_list.append(dict(med))

print(data_list)
