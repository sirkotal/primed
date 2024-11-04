import re
import os
import csv
import ast
import json
import pandas as pd
from io import StringIO
from html import unescape
from datetime import datetime
from unidecode import unidecode


# source datasets
diseases_csv = "../dataset/sources/diseases.csv"
drug_details_csv = "../dataset/sources/drug_details.csv"
drug_reviews_csv = "../dataset/sources/drug_reviews.csv"
pharmaceutical_companies_csv = "../dataset/sources/pharmaceutical_companies.csv"
sicknesses_clean_csv = "../dataset/sources/sicknesses_clean.csv"


# output datasets
diseases_json = "../dataset/output/diseases.json"
drug_details_json = "../dataset/output/drug_details.json"
drug_reviews_json = "../dataset/output/drug_reviews.json"
pharmaceutical_companies_json = "../dataset/output/pharmaceutical_companies.json"
sicknesses_json = "../dataset/output/sicknesses_clean.json"


def _parse_use_cases_side_effects(input_string):
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


def _remove_urls(text): # deletes everything in a string from the point where a url is found
    url_pattern = re.compile(r'https?://|www\.')
    match = url_pattern.search(text)
    if match:
        text = text[:match.start()]
    return text.strip()


def _remove_null_values(dataset: str, _drop_row_if_all_null: bool=False, _drop_if_null: list[str]=None) -> csv.DictReader:

    df = pd.read_csv(dataset)

    if _drop_row_if_all_null:
        df = df.dropna(how='all')
    if _drop_if_null is not None:
        df = df.dropna(subset=_drop_if_null)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return csv.DictReader(csv_buffer)


def _split_json(data: dict, output_path: str, parts: int) -> None:
    path = output_path.split('.json')[0]

    keys = list(data.keys())
    total_rows = len(data)
    entries_per_part = total_rows // parts
    remainder = total_rows % parts

    for i in range(parts):
        low = i * entries_per_part
        high =  (i + 1) * entries_per_part
        if i == parts - 1:
            high += remainder
        current_data = { key: data[key] for key in keys[low:high] }
        _write_to_json(current_data, f"{path}_part_{i + 1}.json")


def _write_to_json(data: dict, json_path: str, divide: int=1) -> None:
    try:
        if divide > 1:
            _split_json(data, json_path,divide)
        else:
            with open(json_path, "w", encoding="utf-8") as jsonf:
                jsonf.write(json.dumps(data, indent=4))
            print(f"Successfully wrote data to {json_path}")
    except Exception as e:
        print(f"Error occurred when writing to {json_path}: {e}")


def parse_drug_details(key_name='Medicine Name'):
    data = {}

    dict_reader = _remove_null_values(drug_details_csv, _drop_row_if_all_null=True, _drop_if_null=[key_name])
    # separator= " ; "

    for row in dict_reader:
        key = row[key_name]
        use_cases = _parse_use_cases_side_effects(row["Uses"])
        side_effects = _parse_use_cases_side_effects(row["Side_effects"])
        row["Uses"] = use_cases  # separator.join(use_cases)
        row["Side_effects"] = side_effects  # separator.join(side_effects)
        row.pop("Image URL", None)
        row.pop(key_name, None)
        data[key] = row

    _write_to_json(data, drug_details_json)


def parse_sicknesses(key_name='Disease/ Illness'):
    data = {}

    dict_reader = _remove_null_values(sicknesses_clean_csv, _drop_row_if_all_null=True, _drop_if_null=[key_name])

    for row in dict_reader:
        key = _remove_urls(row[key_name])
        row.pop(key_name, None)
        data[key] = row
        if (data[key]["Link"]) != '':
            data[key]["Link"] = ast.literal_eval(data[key]["Link"])
        data[key] = { k: unidecode(v) if k != "Link" else v for k, v in data[key].items() }

    _write_to_json(data, sicknesses_json)


def parse_pharmaceutical_companies(key_name='Company Name'):
    data = {}

    dict_reader = _remove_null_values(pharmaceutical_companies_csv, _drop_row_if_all_null=True, _drop_if_null=[key_name])

    for row in dict_reader:
        key = _remove_urls(row[key_name])
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

    _write_to_json(data, pharmaceutical_companies_json)


def parse_diseases(key_name='Disease'):
    data = {}

    dict_reader = _remove_null_values(diseases_csv, _drop_row_if_all_null=True, _drop_if_null=[key_name])

    for row in dict_reader:
        key = row[key_name]
        row.pop(key_name)
        data[key] = row
        data[key] = { k: unidecode(v) for k, v in data[key].items() }
    
    _write_to_json(data, diseases_json)


def parse_drug_reviews(key_name='uniqueID'):
    data = {}

    dict_reader = _remove_null_values(drug_reviews_csv, _drop_row_if_all_null=True, _drop_if_null=['drugName'])

    for row in dict_reader:
        key = row[key_name]
        row.pop(key_name)
        data[key] = row
        data[key] = { k: unidecode(unescape(v)) for k, v in data[key].items() }

        if data[key]["review"].startswith("\"") and data[key]["review"].endswith("\""):
            data[key]["review"] = data[key]["review"][1:-1]

        date_obj = datetime.strptime(data[key]["date"], "%d-%b-%y")
        data[key]["date"] = date_obj.strftime("%Y-%m-%d")
    
    _write_to_json(data, drug_reviews_json, divide=4)
 