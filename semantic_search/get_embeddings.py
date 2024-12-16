import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    with open('docker/data/combined_drug_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for document in data:
        diseases_with_vectors = []
        for disease in document.get("applicable_diseases", []):
            diseases_with_vectors.append({"text": disease, "vector": get_embedding(disease)})
        document["applicable_diseases"] = diseases_with_vectors

        side_effects_with_vectors = []
        for side_effect in document.get("possible_side_effects", []):
            side_effects_with_vectors.append({"text": side_effect, "vector": get_embedding(side_effect)})
        document["possible_side_effects"] = side_effects_with_vectors
        
        reviews_with_vectors = []
        for review in document.get("reviews", []):
            reviews_with_vectors.append({"text": review, "vector": get_embedding(review)})
        document["reviews"] = reviews_with_vectors

    with open('docker/data/semantic_primed_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
