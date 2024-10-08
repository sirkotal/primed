import csv
import json
import re
import ast
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

def parse_medicine_details():
    data = {}

    with open("../dataset/Medicine_Details.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            key = row["Medicine Name"]
            use_cases = parse_use_cases_side_effects(row["Uses"])
            side_effects = parse_use_cases_side_effects(row["Side_effects"])
            row["Uses"] = use_cases
            row["Side_effects"] = side_effects
            row.pop("Image URL", None)
            data[key] = row

    with open("../dataset/medicine_details.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def remove_urls(text): # deletes everything in a string from the point where a url is found
    url_pattern = re.compile(r'https?://|www\.')
    match = url_pattern.search(text)
    if match:
        text = text[:match.start()]
    return text.strip()


def parse_illnesses():
    data = {}

    with open("../dataset/Sicknesses_clean.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Disease/ Illness"

        for row in csvReader:
            key = remove_urls(row[key_name])
            row.pop(key_name, None)
            data[key] = row
            if (data[key]["Link"]) != '':
                data[key]["Link"] = ast.literal_eval(data[key]["Link"])
            data[key] = {k: unidecode(v) if k != "Link" else v for k, v in data[key].items()}

    with open("../dataset/sicknesses.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def parse_pharmaceutical_companies():
    data = {}

    with open("../dataset/Pharmaceutical_companies.csv", encoding="utf-8") as csvf:
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


    with open("../dataset/pharmaceutical_companies.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# parse_medicine_details()
def parse_companies():
    with open("../dataset/Pharmaceutical_companies.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Company Name"

        for row in csvReader:
            key = row["Company Name"]
            year = row["Year"]
            description = row["Description"]
            data[key] = row

    with open("../dataset/companies.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def parse_diseases():
    with open("../dataset/Diseases.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Disease"

        for row in csvReader:
            key = row["Disease"]
            primary_organ = row["Primary organ/body part affected"]
            autoantibodies = row["Autoantibodies"]
            acceptance = row["Acceptance as an autoimmune disease"]
            prevalence = row["Prevalence rate (US)"]
            data[key] = row
    
    with open("../dataset/diseases.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))

parse_medicine_details()
data.clear()
parse_illnesses()
data.clear()
parse_companies()
data.clear()
parse_diseases()
