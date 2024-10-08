import csv
import sqlite3

def convert_data_to_maps(lst, file):
    csv_reader = csv.DictReader(file)
    
    for med in csv_reader:
        med.pop("Image URL")
        med_dic = {k.lower(): v for k, v in dict(med).items()}
        med_dic_v2 = {k.replace(' ', '_') : v for k, v in med_dic.items()}
        lst.append(med_dic_v2)

#data_list = []
#file = open('../dataset/Medicine_Details.csv', mode='r')
#convert_data_to_maps(data_list, file)

#print(data_list)

def convert_json_to_sql(j):
    medicine_db = j.copy()

    medicine_db['Uses'] = medicine_db['Uses'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    medicine_db['Side_effects'] = medicine_db['Side_effects'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    conn = sqlite3.connect('../dataset/medicines.db')
    medicine_db.to_sql('medicine', conn, if_exists='replace', index=False)
    conn.close()
