import os
import json
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def read_text_file(file_path):
    """Reads news articles from a text file."""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return []
    
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def preprocess_text(text):
    """Tokenizes, removes stopwords, and applies lemmatization."""
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]

def process_dataset(input_file, output_file):
    """Reads and preprocesses dataset, then saves to JSON."""
    raw_data = read_text_file(input_file)
    processed_data = [preprocess_text(article) for article in raw_data]
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)
    
    print(f"Processed data saved to {output_file}")

def preprocess():
    # Run preprocessing
    process_dataset("dataset/unlabeled_data.txt", "dataset/processed_unlabeled.json")
    process_dataset("dataset/labeled_data.txt", "dataset/processed_labeled.json")
