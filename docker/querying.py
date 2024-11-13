def generate_simple_query(user_query):
    query_params = {
        'q': user_query,
        "start": 0,
        "rows": 30,
        'defType': 'edismax',
        'qf': "drug composition applicable_diseases diseases_info possible_side_effects reviews manufacturer manufacturer_desc"
    }
    return query_params

def generate_boosted_query(user_query):
    boosted_terms = {"cure": 3.0, "progress": 3.0, "effective": 2.5, "hope": 1.5, "side effects": 3.0, "risk": 2.5, "concern": 1.5}
    boosted_query = []
    for term in user_query.split():
        if term in boosted_terms:
            boosted_query.append(f"{term}^{boosted_terms[term]}")
        else:
            boosted_query.append(term)
    
    boosted_query = " ".join(boosted_query)
    query_params = {
        'q': boosted_query,
        "sort": "reviews_average_rating desc",
        "start": 0,
        "rows": 30,
        'defType': 'edismax',
        'qf': "drug^4 composition^2 applicable_diseases^2 diseases_info^6 possible_side_effects reviews^7 manufacturer manufacturer_desc^3",
        'bf': "excellent_review_perc^1.5 poor_review_perc^0.5"
    }
    return query_params
