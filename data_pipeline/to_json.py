import csv
import json
import re

data = {}

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
    with open("./dataset/Medicine_Details.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            key = row["Medicine Name"]
            use_cases = parse_use_cases_side_effects(row["Uses"])
            side_effects = parse_use_cases_side_effects(row["Side_effects"])
            row["Uses"] = use_cases
            row["Side_effects"] = side_effects
            row.pop("Image URL", None)
            data[key] = row

    with open("./dataset/medicine_details.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def remove_urls(text): # deletes everything in a string from the point where a url is found
    url_pattern = re.compile(r'https?://|www\.')
    match = url_pattern.search(text)
    if match:
        text = text[:match.start()]
    return text.strip()

def parse_illnesses():
    with open("./dataset/Sicknesses_clean.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        key_name = "Disease/ Illness"

        for row in csvReader:
            key = remove_urls(row[key_name])
            row.pop(key_name, None)
            data[key] = row

    with open("./dataset/sicknesses.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))

parse_medicine_details()
parse_illnesses()
