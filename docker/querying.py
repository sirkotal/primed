from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

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
    query_params = {
        'q': user_query,
        'q.op': "AND",
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
    embedding = text_to_embedding(user_query)

    # f"{user_query}{embedding}",
    query_params = {
        'q': f"{{!knn f=vector topK=10}}{embedding}",
        'q.op': "AND",
        'start': 0,
        'rows': 100,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        #'defType': "edismax",
        #'qf': "diseases_info^3 reviews^4 manufacturer_desc",
        #'pf': "reviews^3",
        #'bf': "excellent_review_perc^1.5 poor_review_perc^0.5",
    }
    return query_params

def generate_mixed_query(user_query):
    embedding = text_to_embedding(user_query)

    lexical_query = f"{{!type=edismax qf=text_field}}{user_query}"
    vector_query = f"{{!knn f=vector topK=10}}{embedding}"
    q = f"{{!bool should=}}{lexical_query}{{ should=}}{vector_query}"
    q2 = {
        "bool": {
            "should": [
               f"{{!type=edismax qf=text_field}}{user_query}",
               f"{{!knn f=vector topK=10}}{embedding}"
            ]
        }
    }

    query_params = {
        'q': q,
        'q.op': "AND",
        'start': 0,
        'rows': 100,
        'fl': "id, drug, composition, applicable_diseases, diseases_info, possible_side_effects, excellent_review_perc, average_review_perc, poor_review_perc, reviews_average_rating, reviews_useful_count, reviews, manufacturer, manufacturer_desc, manufacturer_start, manufacturer_end, score",
        #'defType': "edismax",
        #'qf': "diseases_info^3 reviews^4 manufacturer_desc",
        #'pf': "reviews^3",
        #'bf': "excellent_review_perc^1.5 poor_review_perc^0.5",
    }
    return query_params
