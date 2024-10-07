import csv

def convert_data_to_maps(lst, file):
    csv_reader = csv.DictReader(file)
    
    for med in csv_reader:
        med.pop("Image URL")
        med_dic = {k.lower(): v for k, v in dict(med).items()}
        med_dic_v2 = {k.replace(' ', '_') : v for k, v in med_dic.items()}
        lst.append(med_dic_v2)

data_list = []
file = open('./dataset/Medicine_Details.csv', mode='r')
convert_data_to_maps(data_list, file)

print(data_list)
