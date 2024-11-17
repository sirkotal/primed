def generate_simple_query(user_query):
    query_params = {
        'q': user_query,
        'q.op': "AND",
        'sort': "reviews_average_rating desc",
        'start': 0,
        'rows': 30,
        'defType': "edismax",
        'qf': "diseases_info reviews manufacturer_desc"
    }
    return query_params

def generate_boosted_query(user_query):
    boosted_terms = {"cure": 4.0, "progress": 3.0, "prevent": 2.75, "effective": 2.5, "safe": 2.5, "hope": 1.5, "side effects": 3.0, 
                     "risk": 2.5, "concern": 1.5, "reliable": 1.5, "aggressive": 1.5, "death": 2, "prestigious": 1.1}
    boosted_query = []
    for term in user_query.split():
        if len(term) > 5:
            term = f"{term}~1"
        
        if term in boosted_terms:
            boosted_query.append(f"{term}^{boosted_terms[term]}")
        else:
            boosted_query.append(term)
    
    boosted_query = " ".join(boosted_query)
    query_params = {
        'q': boosted_query,
        'q.op': "AND",
        'sort': "reviews_average_rating desc",
        'start': 0,
        'rows': 30,
        'defType': "edismax",
        'qf': "diseases_info^3 reviews^4 manufacturer_desc",
        'pf': "reviews^3",
        'ps': 2,
        'bf': "excellent_review_perc^1.5 poor_review_perc^0.5"
    }
    return query_params
