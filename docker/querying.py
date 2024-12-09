def generate_simple_query(user_query):
    query_params = {
        'q': user_query,
        'q.op': "AND",
        'sort': "score desc",
        'start': 0,
        'rows': 30,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        'defType': "edismax",
        'qf': "diseases_info reviews manufacturer_desc"
    }
    return query_params

def generate_boosted_query(user_query):
    '''boosted_terms = {"cure": 4.0, "progress": 3.0, "prevent": 2.75, "effective": 2.5, "safe": 2.5, "hope": 1.5, "effects": 3.0, 
                     "risk": 2.5, "concern": 1.5, "reliable": 1.5, "aggressive": 1.5, "death": 2.0, "prestigious": 1.1}

        if term in boosted_terms:
            boosted_query.append(f"{term}^{boosted_terms[term]}")
        else:
            boosted_query.append(term)
    
    boosted_query = " ".join(boosted_query)'''

    boosted_query = []

    for term in user_query.split():
        if len(term) > 5:
            term = f"{term}~1"
        boosted_query.append(term)

    query_params = {
        'q': user_query,
        'q.op': "AND",
        'sort': "score desc",
        'start': 0,
        'rows': 30,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        'defType': "edismax",
        'qf': "diseases_info^3 reviews^4 manufacturer_desc",
        'pf': "reviews^3",
        'ps': 2,
        # 'bf': f"excellent_review_perc^1.5 poor_review_perc^0.5 query({{!v='side_effects:{user_query}'}})^1.5"
        'bf': f"excellent_review_perc^1.5 poor_review_perc^0.5"
    }
    return query_params
