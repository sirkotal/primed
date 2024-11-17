import json
from collections import defaultdict
from text_cleanup import repair_string
import re

def summarize_drug_reviews(drug_reviews):
    summary_data = defaultdict(lambda: {"total_rating": 0, "count": 0, "excelent": 0, "average": 0, "poor": 0, "reviews": []})

    for review_data in drug_reviews:
        drug_name = review_data["drugName"]
        
        summary_data[drug_name]["total_rating"] += int(review_data["rating"])
        summary_data[drug_name]["count"] += 1
        summary_data[drug_name]["reviews"].append(review_data["review"])
        if int(review_data["rating"]) > 7:
            summary_data[drug_name]["excelent"] += 1
        elif int(review_data["rating"]) < 4:
            summary_data[drug_name]["poor"] += 1
        else:
            summary_data[drug_name]["average"] += 1

    summarizedList = []
    for drug_name, data in summary_data.items():
        summarized_entry = {
            "drugName": drug_name,
            "average_rating": data["total_rating"] / data["count"],
            "excelent_rating_perc": data["excelent"] / data["count"],
            "average_rating_perc": data["average"] / data["count"],
            "poor_rating_perc": data["poor"] / data["count"],
            "reviews": data["reviews"]
        }
        summarizedList.append(summarized_entry)

    return summarizedList


with open('./dataset/output/drug_details.json', 'r') as f:
    drug_details = json.load(f)

with open('./dataset/output/diseases.json', 'r') as f:
    diseases = json.load(f)

with open('./dataset/output/cuf_sicknesses.json', 'r') as f:
    cuf_sicknesses = json.load(f)

with open('./dataset/output/pharmaceutical_companies.json', 'r') as f:
    companies = json.load(f)


def load_reviews(filenames):
    reviews = []
    for filename in filenames:
        with open(filename, 'r') as f:
            data = json.load(f)
            reviews.extend(data.values())
    return reviews


review_files = [
    './dataset/output/drug_reviews_part_1.json',
    './dataset/output/drug_reviews_part_2.json',
    './dataset/output/drug_reviews_part_3.json',
    './dataset/output/drug_reviews_part_4.json'
]

drug_reviews = load_reviews(review_files)
summarizedList = summarize_drug_reviews(drug_reviews)


def find_reviews(composition):
    reviews = []
    composition_terms = composition.split()
    
    for review in summarizedList:
        if 'drugName' in review and review['drugName'] in composition_terms:
            reviews.append(review)
    return reviews


def find_diseases(terms):
    matched_diseases = []

    for term in terms:
        name_parts = term.split()
        for part in name_parts:
            if part in diseases:
                sickness_info = diseases[part]
                description = "".join([f"//{k}//{v}" for k, v in sickness_info.items()])
                matched_diseases.append({
                    "Sickness": part,
                    "Description": description
                })
            for key, sickness_info in diseases.items():
                if key.lower() in part:
                    description = "".join([f"//{k}//{v}" for k, v in sickness_info.items()])
                    matched_diseases.append({
                        "Sickness": key,
                        "Description": description
                    })
    
    return matched_diseases

def find_cuf_diseases(terms):
    matched_diseases = []
    keys = list(cuf_sicknesses.keys())

    for term in terms:
        for sickness_name in keys:
            if sickness_name.lower() in term.lower() or term.lower() in sickness_name.lower():
                sickness_info = cuf_sicknesses[sickness_name]
                description = "".join([f"//{k}//{v}" for k, v in sickness_info.items()])
                matched_diseases.append({
                    "Sickness": sickness_name,
                    "Description": description
                })
    
    return matched_diseases

def find_company(manufacturer_name):
    name_parts = manufacturer_name.split()
    
    for part in name_parts:
        if part in companies:
            return companies[part]
        
        for key in companies.keys():
            if key in part:
                return companies[key]
            
    return companies.get(manufacturer_name, {'Description': '', 'Year Start': '', 'Year End': ''})

def combine_data():
    combined_data = []
    for drug, details in drug_details.items():
        related_diseases = find_diseases(details['Uses'])
        related_cuf_diseases = find_cuf_diseases(details['Uses'])
    
        related_reviews = find_reviews(details['Composition'])
        all_reviews = []

        if related_reviews:
            total_ratings = sum(review['average_rating'] for review in related_reviews)
            for review in related_reviews:
                all_reviews += review['reviews']
            reviews_average_rating = round(total_ratings / len(related_reviews), 2) if related_reviews else 0
        else:
            reviews_average_rating = "0"
            all_reviews = []
    
        company_info = find_company(details['Manufacturer'])
    
        combined_entry = {
            "drug": drug,
            "composition": details['Composition'],
            "applicable_diseases": details['Uses'],
            "diseases_info": [disease['Description'] for disease in related_diseases if 'Description' in disease],
            "diseases_info2": [disease['Description'] for disease in related_cuf_diseases if 'Description' in disease],
            "possible_side_effects": details['Side_effects'],
            "excellent_review_perc": details['Excellent Review %'],
            "average_review_perc": details['Average Review %'],
            "poor_review_perc": details['Poor Review %'],
            "reviews_average_rating": str(reviews_average_rating),
            "reviews": all_reviews,
            "manufacturer": details['Manufacturer'],
            "manufacturer_desc": repair_string(company_info['Description']),
            "manufacturer_start": repair_string(company_info['Year Start']),
            "manufacturer_end": company_info['Year End']
        }

        combined_data.append(combined_entry)

    with open('./docker/data/combined_drug_data.json', 'w') as f:
        json.dump(combined_data, f, indent=4)
    
    print("Combined data created successfully!")
