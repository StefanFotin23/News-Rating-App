import os
import json
import requests
import spacy
from bs4 import BeautifulSoup
from transformers import AutoTokenizer

# Step 1: Define API Key & URL
API_KEY = "7bc719a0-6dc4-465d-a800-583af38ccdaa"
BASE_URL = "https://content.guardianapis.com/search"

dir_path = "/mnt/data"
news_data_file = "/mnt/data/news_data.json"

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load RoBERTa tokenizer (same one used by PySentimiento)
bert_tokenizer = AutoTokenizer.from_pretrained("roberta-base")

def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ")  # Extract plain text

def tokenize_post(post, tokenizer="spacy"):
    if tokenizer == "spacy":
        tokenized_post_body = spacy_tokenize(post)
    elif tokenizer == "bert":
        tokenized_post_body = bert_tokenize(post)
    return tokenized_post_body

def spacy_tokenize(post):
    """Tokenizes, removes stopwords, and applies lemmatization."""
    doc = nlp(post["body"])  # Tokenize only the body
    return [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]

def bert_tokenize(post):
    return bert_tokenizer(post["body"], truncation=True, padding=True, return_tensors="pt")

def get_news_posts(file_path=news_data_file):
    """Reads a JSON file and returns a dictionary of posts indexed by ID."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            posts = json.load(file)  # Load JSON data
            return posts  # Returns a dictionary for efficient lookup
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error: {e}")
        return {}

def fetch_news_data(topic=None, no_of_news=50):
    # Step 2: Set up request parameters
    if topic:
        params = {
            "q": topic,  # Change this to any topic you're interested in
            "api-key": API_KEY,
            "show-fields": "headline,body",
            "page": 1,  # Modify for pagination if needed
            "page-size": no_of_news
        }
    else:
        params = {
            "api-key": API_KEY,
            "show-fields": "headline,body",
            "page": 1,  # Modify for pagination if needed
            "page-size": no_of_news
        }

    # Step 3: Make the API request
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Step 4: Extract and format the results as a dictionary
    articles = {}
    if "response" in data and "results" in data["response"]:
        for index, article in enumerate(data["response"]["results"], start=1):
            clean_body = parse_html(article["fields"]["body"])
            articles[index] = {  # Store each article with a unique ID as the dictionary key
                "title": article["fields"]["headline"],
                "body": clean_body,
            }

    # Step 5: Save results to a JSON file
    if os.path.exists(dir_path):
        print(f"✅ Directory exists: {dir_path}")
    else:
        print(f"❌ Directory does NOT exist, creating it now...")
        os.makedirs(dir_path, exist_ok=True)

    # Check write permissions
    if os.access(dir_path, os.W_OK):
        print(f"✅ You have write permissions for {dir_path}")
    else:
        print(f"❌ No write permissions for {dir_path}. Try changing permissions.")

    # Now attempt to create the file
    try:
        with open(news_data_file, "w", encoding="utf-8") as file:
            json.dump(articles, file, indent=4, ensure_ascii=False)
        print(f"✅ File saved successfully at {news_data_file}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

    return articles

def preprocess_post(post):
    post["body"] = parse_html(post["body"])
    post["tokenized_body"] = tokenize_post(post, "spacy")
    return post