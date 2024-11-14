import requests
from querying import generate_boosted_query

solr = 'http://localhost:8983/solr/primed-data/select'

query = input("Enter your query: ")

query_params = generate_boosted_query(query)

response = requests.get(solr, params=query_params)

if response.status_code == 200:
    print(f"Successful query.")
else:
    print(f"Error: {response.status_code}")
