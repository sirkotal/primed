import requests
import json
from querying import generate_simple_query

solr = 'http://localhost:8983/solr/primed-data/select'

query = input("Enter your query: ")

query_params = generate_simple_query(query)

response = requests.get(solr, params=query_params)

if response.status_code == 200:
    print(f"Successful query.")
    print(f"SOLR Response: {response.json()}")

    with open("solr_simple_response.txt", "w") as file:
        json.dump(response.json(), file, indent=4) 
else:
    print(f"Error: {response.status_code}")
