import csv
import json

data = {}

with open("./Medicine_Details.csv", encoding="utf-8") as csvf:
    csvReader = csv.DictReader(csvf)

    for row in csvReader:
        key = row["Medicine Name"]
        data[key] = row

with open("./Medicine_Details.json", "w", encoding="utf-8") as jsonf:
    jsonf.write(json.dumps(data, indent=4))
