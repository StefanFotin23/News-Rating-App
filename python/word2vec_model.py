import os
import json
import gensim
import numpy as np
from gensim.models import Word2Vec
from preprocess_data import preprocess

PROCESSED_DATA_PATH = "dataset/processed_unlabeled.json"
MODEL_PATH = "/app/models/word2vec.model"

def load_processed_data(file_path):
    """Loads preprocessed JSON data."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def train_word2vec_model(data, save_path, vector_size=100, window=5, min_count=1):
    """Trains a Word2Vec model on processed text data."""
    print("Training Word2Vec model...")
    
    model = Word2Vec(sentences=data, vector_size=vector_size, window=window, min_count=min_count, workers=4)
    model.save(save_path)
    
    print(f"Model saved to {save_path}")

def test_word_similarity(model, word):
    """Prints words most similar to a given word."""
    if word in model.wv:
        similar_words = model.wv.most_similar(word, topn=10)
        print(f"Words similar to '{word}': {similar_words}")
    else:
        print(f"'{word}' not found in vocabulary.")

def get_article_vector(article_tokens, model):
    """Computes the average word vector for an article."""
    vectors = [model.wv[word] for word in article_tokens if word in model.wv]
    return np.mean(vectors, axis=0) if vectors else None

def rate_news_article(article_tokens, model, reference_count):
    """Rates a news article based on word embeddings and metadata."""
    similarity_scores = [model.wv.similarity(word, source) 
                         for word in article_tokens for source in trusted_sources
                         if word in model.wv and source in model.wv]
    
    avg_similarity = np.mean(similarity_scores) if similarity_scores else 0  # Avg similarity to trusted sources
    credibility_score = (avg_similarity * 7) + (reference_count * 3)  # Weighted scoring

    return round(credibility_score, 2)

trusted_sources = ["reuters", "bbc", "cnn", "nasa", "government"]

if __name__ == "__main__":
    preprocess()  # Run preprocessing

    # Load processed dataset
    processed_unlabeled = load_processed_data(PROCESSED_DATA_PATH)

    # Train and save Word2Vec model
    train_word2vec_model(processed_unlabeled, MODEL_PATH)

    # Load trained model
    model = Word2Vec.load(MODEL_PATH)

    # Test word similarity
    test_word_similarity(model, "ai")

    # Example article rating
    example_article = ["ai", "regulation", "government", "ethics"]
    reference_count = 4
    news_rating = rate_news_article(example_article, model, reference_count)
    print("News Credibility Score:", news_rating)
