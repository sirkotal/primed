import csv

def convert_data_to_maps(lst, file):
    csv_reader = csv.DictReader(file)
    
    for med in csv_reader:
        lst.append(dict(med))

data_list = []
file = open('./dataset/Medicine_Details.csv', mode='r')
convert_data_to_maps(data_list, file)

print(data_list)
