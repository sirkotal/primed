import requests
import json
import sys
from querying import generate_simple_query

solr = 'http://localhost:8983/solr/primed-data/select'

query = sys.argv[1]

query_params = generate_simple_query(query)

response = requests.get(solr, params=query_params)

if response.status_code == 200:
    print(f"Successful query.")
    print(f"SOLR Response: {response.json()}")

    with open("solr_simple_response.json", "w") as file:
        json.dump(response.json(), file, indent=4) 
else:
    print(f"Error: {response.status_code}")
