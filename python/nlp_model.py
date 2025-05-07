from preprocess_data import preprocess
from pysentimiento import create_analyzer

# Load sentiment and emotion analyzers
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
emotion_analyzer = create_analyzer(task="emotion", lang="en")

def analyze_posts(posts):
    """Analyze sentiment and emotion for each post."""
    processed_posts = []
    
    for post in posts:
        sentiment_result = sentiment_analyzer.predict(post["body"])  # Analyze body sentiment
        emotion_result = emotion_analyzer.predict(post["body"])  # Analyze body emotion
        
        # Append results to processed posts
        processed_posts.append({
            "title": post["title"],
            "body": post["body"],
            "sentiment": sentiment_result.output,  # POSITIVE, NEGATIVE, NEUTRAL
            "emotion": emotion_result.output  # JOY, ANGER, FEAR, etc.
        })
    
    return processed_posts

posts, tokenized_posts = preprocess()

analyzed_posts = analyze_posts(posts)
print(analyzed_posts[0])  # Prints analyzed posts with sentiment & emotion
