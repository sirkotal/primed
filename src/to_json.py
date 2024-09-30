import csv
import json

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

with open("../dataset/Medicine_Details.csv", encoding="utf-8") as csvf:
    csvReader = csv.DictReader(csvf)

    for row in csvReader:
        key = row["Medicine Name"]
        use_cases = parse_use_cases_side_effects(row["Uses"])
        side_effects = parse_use_cases_side_effects(row["Side_effects"])
        row["Uses"] = use_cases
        row["Side_effects"] = side_effects
        data[key] = row

with open("../dataset/Medicine_Details.json", "w", encoding="utf-8") as jsonf:
    jsonf.write(json.dumps(data, indent=4))
