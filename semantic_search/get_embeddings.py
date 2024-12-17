import sys
import json
from threading import Thread
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

def process_data(start_idx, end_idx, input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(start_idx, end_idx):
        document = data[i]

        diseases_with_vectors = []
        for disease in document.get("applicable_diseases", []):
            diseases_with_vectors.append({"text": disease, "vector": get_embedding(disease)})
            print("disease")
        document["applicable_diseases"] = diseases_with_vectors

        side_effects_with_vectors = []
        for side_effect in document.get("possible_side_effects", []):
            side_effects_with_vectors.append({"text": side_effect, "vector": get_embedding(side_effect)})
            print("side effect")
        document["possible_side_effects"] = side_effects_with_vectors

        #reviews_with_vectors = []
        #for review in document.get("reviews", []):
        #    reviews_with_vectors.append({"text": review, "vector": get_embedding(review)})
        #    print("review")
        #document["reviews"] = reviews_with_vectors

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data[start_idx:end_idx], f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_file = 'docker/data/combined_drug_data.json'
    output_file_1 = 'docker/data/semantic_primed_data.json'
    #output_file_2 = 'docker/data/semantic_primed_data_part2.json'
    #output_file_3 = 'docker/data/semantic_primed_data_part3.json'
    #output_file_4 = 'docker/data/semantic_primed_data_part4.json'

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_docs = len(data)
    quarter_point = total_docs // 4

    thread1 = Thread(target=process_data, args=(0, total_docs, input_file, output_file_1))
    #thread2 = Thread(target=process_data, args=(quarter_point, quarter_point * 2, input_file, output_file_2))
    #thread3 = Thread(target=process_data, args=(quarter_point * 2, quarter_point * 3, input_file, output_file_3))
    #thread4 = Thread(target=process_data, args=(quarter_point * 3, total_docs, input_file, output_file_4))

    thread1.start()
    #thread2.start()
    #thread3.start()
    #thread4.start()

    thread1.join()
    #thread2.join()
    #thread3.join()
    #thread4.join()

    print("Processing completed. Results saved to:")
    print(f"  - {output_file_1}")
    #print(f"  - {output_file_2}")
    #print(f"  - {output_file_3}")
    #print(f"  - {output_file_4}")
