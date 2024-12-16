import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

def get_string_from_list(list):
    return " ".join(list)

if __name__ == "__main__":
    with open('docker/data/combined_drug_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for document in data:
        applicable_diseases = get_string_from_list(document.get("applicable_diseases", ""))
        possible_side_effects = get_string_from_list(document.get("possible_side_effects", ""))
        reviews = get_string_from_list(document.get("reviews", ""))

        combined_text = "Diseases: " + applicable_diseases + " Side effects: " + possible_side_effects + " Reviews: " + reviews
        document["vector"] = get_embedding(combined_text)

    with open('docker/data/semantic_primed_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
