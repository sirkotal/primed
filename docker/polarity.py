import nltk
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def get_review_polarity(review):
    sentiment = sia.polarity_scores(review)
    return sentiment['compound']

def normalize_average_rating(rating):
    return (rating - 5) / 5

def combine_rating_and_polarity(average_rating, reviews):
    normalized_reviews_rating = normalize_average_rating(average_rating)
    
    polarity_scores = [get_review_polarity(review) for review in reviews]
    average_polarity = np.mean(polarity_scores)
    
    return (normalized_reviews_rating + average_polarity) / 2

def process_documents():
    with open('./docker/data/combined_drug_data.json', 'r') as f:
        collection = json.load(f)

    for doc in collection:
        reviews_average_rating = float(doc.get('reviews_average_rating', 0))
        reviews = doc.get('reviews', [])
        
        if reviews and reviews_average_rating:
            combined_score = combine_rating_and_polarity(reviews_average_rating, reviews)
            doc['polarity_rating'] = combined_score
        else:
            doc['polarity_rating'] = 0
    
    with open('./docker/data/combined_drug_data.json', 'w') as f:
        json.dump(collection, f, indent=4)

    print("Documents processed and saved with combined scores!")

process_documents()