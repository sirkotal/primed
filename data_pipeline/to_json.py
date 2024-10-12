import csv
import json
import re
import ast
from html import unescape
from datetime import datetime
from unidecode import unidecode


def parse_use_cases_side_effects(input_string):
    connectors = {"of", "and", "in", "for", "with", "the", "to", "a", "an"}
    
    use_cases = []
    current_case = []
    
    words = input_string.split()
    
    connector_found = False
    for word in words:
        if word.lower() in connectors:
            current_case.append(word)
            connector_found = True
        elif word[0].isupper():
            if connector_found:
                current_case.append(word)
            else:
                if current_case:
                    use_cases.append(" ".join(current_case).strip())
                current_case = [word]
            connector_found = False
        else:
            current_case.append(word)
            connector_found = False

    if current_case:
        use_cases.append(" ".join(current_case).strip())

    return use_cases


def parse_drug_details():
    data = {}

    with open("dataset/sources/medicine_details.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            key = row["Medicine Name"]
            use_cases = parse_use_cases_side_effects(row["Uses"])
            side_effects = parse_use_cases_side_effects(row["Side_effects"])
            row["Uses"] = use_cases
            row["Side_effects"] = side_effects
            row.pop("Image URL", None)
            data[key] = row

    with open("dataset/output/medicine_details.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    print("Successfully wrote data to dataset/output/medicine_details.json")


def remove_urls(text): # deletes everything in a string from the point where a url is found
    url_pattern = re.compile(r'https?://|www\.')
    match = url_pattern.search(text)
    if match:
        text = text[:match.start()]
    return text.strip()


def parse_sicknesses():
    data = {}

    with open("dataset/sources/sicknesses_clean.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Disease/ Illness"

        for row in csvReader:
            key = remove_urls(row[key_name])
            row.pop(key_name, None)
            data[key] = row
            if (data[key]["Link"]) != '':
                data[key]["Link"] = ast.literal_eval(data[key]["Link"])
            data[key] = { k: unidecode(v) if k != "Link" else v for k, v in data[key].items() }

    with open("dataset/output/sicknesses.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    print("Successfully wrote data to dataset/output/sicknesses.json")


def parse_pharmaceutical_companies():
    data = {}

    with open("dataset/sources/pharmaceutical_companies.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Company Name"

        for row in csvReader:
            key = remove_urls(row[key_name])
            row.pop(key_name, None)
            data[key] = row
            years = data[key]["Year"].split("-")
            try:
                year_start = years[0]
                year_end = years[1]
            except:
                year_start = ""
                year_end = ""
            data[key]["Year Start"] = year_start
            data[key]["Year End"] = year_end
            data[key].pop("Year", None)

    with open("dataset/output/pharmaceutical_companies.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    print("Successfully wrote data to pharmaceutical_companies.json")


def parse_diseases():
    data = {}

    with open("dataset/sources/diseases.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Disease"

        for row in csvReader:
            key = row["Disease"]
            primary_organ = row["Primary organ/body part affected"]
            autoantibodies = row["Autoantibodies"]
            acceptance = row["Acceptance as an autoimmune disease"]
            prevalence = row["Prevalence rate (US)"]
            data[key] = row
            data[key] = { k: unidecode(v) for k, v in data[key].items() }
    
    with open("dataset/output/diseases.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    print("Successfully wrote data to diseases.json")

def parse_drug_reviews():
    data = {}

    with open("dataset/sources/drug_reviews.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            key = row["uniqueID"]
            data[key] = row
            data[key] = { k: unidecode(unescape(v)) for k, v in data[key].items() }

            if data[key]["review"].startswith("\"") and data[key]["review"].endswith("\""):
                data[key]["review"] = data[key]["review"][1:-1]

            date_obj = datetime.strptime(data[key]["date"], "%d-%b-%y")
            data[key]["date"] = date_obj.strftime("%Y-%m-%d")

        total_rows = len(data)
        half_point = total_rows // 2
        quarter_point = total_rows // 4

        keys = list(data.keys())

        data_first_q = {key: data[key] for key in keys[:quarter_point]}

        data_second_q = {key: data[key] for key in keys[quarter_point:half_point]}

        data_third_q = {key: data[key] for key in keys[half_point:(quarter_point*3)]}

        data_fourth_q = {key: data[key] for key in keys[(quarter_point*3):]}

    with open("dataset/output/drug_reviews_part_1.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data_first_q, indent=4))
    print("Successfully wrote data to dataset/output/drug_reviews_part_1.json")
    with open("dataset/output/drug_reviews_part_2.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data_second_q, indent=4))
    print("Successfully wrote data to dataset/output/drug_reviews_part_2.json")
    with open("dataset/output/drug_reviews_part_3.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data_third_q, indent=4))
    print("Successfully wrote data to dataset/output/drug_reviews_part_3.json")
    with open("dataset/output/drug_reviews_part_4.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data_fourth_q, indent=4))
    print("Successfully wrote data to dataset/output/drug_reviews_part_4.json")


# parse_drug_details()
# parse_sicknesses()
# parse_pharmaceutical_companies()
# parse_diseases()
# parse_drug_reviews()
