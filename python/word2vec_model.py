import os
from time import sleep
import gensim
from gensim.models import Word2Vec
import re

# Define paths
DATASET_PATH = "/app/dataset/dataset.txt"
MODEL_PATH = "/app/models/word2vec.model"

# Preprocessing function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.split()

# Load dataset
def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        text_data = file.readlines()
    return [preprocess_text(sentence) for sentence in text_data]

# Train the Word2Vec model
def train_word2vec():
    sentences = load_dataset()
    model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
    
    # Ensure models directory exists
    os.makedirs("/app/models", exist_ok=True)

    # Save model
    model.save(MODEL_PATH)
    print(f"✅ Word2Vec model trained and saved at {MODEL_PATH}")

if __name__ == "__main__":
    train_word2vec()
