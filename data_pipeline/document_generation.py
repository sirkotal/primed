import json

with open('../dataset/output/drug_details.json', 'r') as f:
    drug_details = json.load(f)

with open('../dataset/output/diseases.json', 'r') as f:
    diseases = json.load(f)

with open('../dataset/output/pharmaceutical_companies.json', 'r') as f:
    companies = json.load(f)

drug_reviews = []
for i in range(1, 5):
    with open(f'../dataset/output/drug_reviews_part_{i}.json', 'r') as f:
        drug_reviews.extend(json.load(f))

def find_reviews(composition):
    reviews = []
    print(f"Composition: {composition}")
    
    for review in drug_reviews:
        print(f"Review: {review}")
        if isinstance(review, dict) and 'drugName' in review:
            if isinstance(review['drugName'], str):
                if composition in review['drugName']:
                    reviews.append(review)
            else:
                print(f"Warning: 'drugName' is not a string: {review['drugName']}")
        else:
            print("Warning: review is not a dictionary or missing 'drugName'")
    
    return reviews

def find_diseases(terms):
    matched_diseases = []

    for term in terms:
        name_parts = term.split()
        for part in name_parts:
            if part in diseases:
                matched_diseases.append(diseases[part])
        
            for key in diseases.keys():
                if key.lower() in part:
                    matched_diseases.append(diseases[key])

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

combined_data = []
for drug, details in drug_details.items():
    related_diseases = find_diseases(details['Uses'])
    related_side_effects = find_diseases(details['Side_effects'])
    
    #related_reviews = find_reviews(details['Composition'])
    
    company_info = find_company(details['Manufacturer'])
    print(company_info)
    
    combined_entry = {
        "drug": drug,
        "composition": details['Composition'],
        "applicable_diseases": details['Uses'],
        "possible_side_effects": details['Side_effects'],
        "excellent_review_perc": details['Excellent Review %'],
        "average_review_perc": details['Average Review %'],
        "poor_review_perc": details['Poor Review %'],
        #"related_reviews": related_reviews,
        "manufacturer": details['Manufacturer'],
        "manufacturer_desc": company_info['Description'],
        "manufacturer_start": company_info['Year Start'],
        "manufacturer_end": company_info['Year End']
    }
    
    combined_data.append(combined_entry)

with open('../dataset/output/combined_drug_data.json', 'w') as f:
    json.dump(combined_data, f, indent=4)
    
print("Dados combinados criados com sucesso!")
