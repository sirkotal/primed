from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    final_str = f"{{!knn f=vector topK=20}}{embedding_str}"
    print(final_str)
    return final_str

def generate_simple_query(user_query):
    query_params = {
        'q': user_query,
        'q.op': "AND",
        'sort': "score desc",
        'start': 0,
        'rows': 100,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        'defType': "edismax",
        'qf': "diseases_info reviews manufacturer_desc"
    }
    return query_params

def generate_boosted_query(user_query):
    boosted_query = []

    for term in user_query.split():
        if len(term) > 5:
            term = f"{term}~1"
        boosted_query.append(term)

    user_query = ' '.join(boosted_query)

    query_params = {
        'q': user_query,
        'q.op': "AND",
        'sort': "score desc",
        'start': 0,
        'rows': 100,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        'defType': "edismax",
        'qf': "diseases_info^3 reviews^4 manufacturer_desc",
        'pf': "reviews^3",
        'ps': 2,
        'bf': f"excellent_review_perc^1.5 poor_review_perc^0.5"
    }
    return query_params

def generate_semantic_boosted_query(user_query):
    # embedding = text_to_embedding(user_query)

    query_params = {
        'q': user_query, # f"{user_query}{embedding}",
        'q.op': "AND",
        'sort': "score desc",
        'start': 0,
        'rows': 100,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        'defType': "edismax",
        'qf': "diseases_info^3 reviews^4 manufacturer_desc",
        'pf': "reviews^3",
        'ps': 2,
        # 'bf': f"excellent_review_perc^1.5 poor_review_perc^0.5 query({{!v='side_effects:{user_query}'}})^1.5"
        'bf': "excellent_review_perc^1.5 poor_review_perc^0.5",
        'rq': "{!rerank reRankQuery=$rqq reRankDocs=30 reRankWeight=2.0}",
        'rqq': "{!func}sum(product(reviews_average_rating, 4), product(polarity_rating, 2))"
    }
    return query_params