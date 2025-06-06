from preprocess_data import fetch_news_data, get_news_posts
from nlp_model import analyze_post
from flask import Flask, jsonify

news_rating_app = Flask(__name__)

# Setup of posts at start time
posts = get_news_posts()
if posts == {}:
    posts = fetch_news_data()

@news_rating_app.route("/news/fetch", methods=["GET"])
def fetch_all_news():
    posts = fetch_news_data()
    return jsonify(posts)

@news_rating_app.route("/news/load", methods=["GET"])
def load_all_news():
    posts = get_news_posts()
    return jsonify(posts)

@news_rating_app.route("/news/all", methods=["GET"])
def get_all_news():
    return jsonify(posts)

@news_rating_app.route("/news/<int:post_id>", methods=["GET"])
def get_news_post(post_id):
    post = next((p for p in posts if p.get("id") == post_id), None)
    return jsonify(post) if post else jsonify({"error": "Not found"}), 404

@news_rating_app.route("/news/analyze/<int:post_id>", methods=["GET"])
def analyze_news_post(post_id):
    """Analyze sentiment of a news article."""
    post = next((p for p in posts if p.get("id") == post_id), None)
    if not post:
        return jsonify({"error": "Not found"}), 404
    
    sentiment_result = analyze_post(post["body"])
    post["sentiment"] = sentiment_result.output
    
    return jsonify(post)

if __name__ == "__main__":
    news_rating_app.run(host="0.0.0.0", port=5000)