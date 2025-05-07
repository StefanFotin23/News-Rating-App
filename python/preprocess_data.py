import os
import json
import requests
import spacy
from bs4 import BeautifulSoup

# Step 1: Define API Key & URL
API_KEY = "7bc719a0-6dc4-465d-a800-583af38ccdaa"
BASE_URL = "https://content.guardianapis.com/search"

model_path = "/app/model"
news_data_file = "/app/model/news_data.json"

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ")  # Extract plain text

def tokenize_dataset(posts):
    return [preprocess_text(post["body"]) for post in posts]

def preprocess_text(text):
    """Tokenizes, removes stopwords, and applies lemmatization."""
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]

def load_posts(file_path):
    """Reads a JSON file and returns a list of posts."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            posts = json.load(file)  # Load JSON data
            return posts  # Return the list of posts
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found!")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: Failed to decode JSON in '{file_path}'!")
        return []

def get_news_data(topic=None, no_of_news=50):
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

    # Step 4: Extract and format the results
    articles = []
    if "response" in data and "results" in data["response"]:
        for article in data["response"]["results"]:
            articles.append({
                "title": article["fields"]["headline"],
                "body": article["fields"]["body"]
            })

    # Step 5: Save results to a JSON file
    if os.path.exists(model_path):
        print(f"✅ Directory exists: {model_path}")
    else:
        print(f"❌ Directory does NOT exist, creating it now...")
        os.makedirs(model_path, exist_ok=True)

    # Check write permissions
    if os.access(model_path, os.W_OK):
        print(f"✅ You have write permissions for {model_path}")
    else:
        print(f"❌ No write permissions for {model_path}. Try changing permissions.")

    # Now attempt to create the file
    try:
        with open(news_data_file, "w", encoding="utf-8") as file:
            json.dump(articles, file, indent=4, ensure_ascii=False)
        print(f"✅ File saved successfully at {news_data_file}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def preprocess():
    # Run preprocessing
    get_news_data()
    posts = load_posts(news_data_file)
    # Process each post and clean its body
    for post in posts:
        post["body"] = parse_html(post["body"])
    tokenized_posts = tokenize_dataset(posts)
    return posts, tokenized_posts
