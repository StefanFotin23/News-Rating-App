import spacy
import gensim
import json
import os
import gensim.corpora as corpora
from preprocess_data import preprocess_post
from pysentimiento import create_analyzer
from textstat import (
    flesch_reading_ease,
    smog_index,
    coleman_liau_index,
    automated_readability_index
)
from collections import Counter
from textblob import TextBlob

# Load sentiment and emotion analyzers
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = create_analyzer(task="sentiment", lang="en", from_tf=True)
emotion_analyzer = create_analyzer(task="emotion", lang="en", from_tf=True)

dir_path = "/mnt/data"
news_data_file = "/mnt/data/news_data.json"

def analyze_single_post(post):
    # Lexical Diversity (using pre-tokenized text)
    words = post["tokenized_body"]  # Assuming 'tokens' is the pre-tokenized list of words
    body_text = post["body"]

    # Sentiment & Emotion
    sentiment_result = sentiment_analyzer.predict(post["body"])
    emotion_result = emotion_analyzer.predict(post["body"])

    # Named Entity Recognition (NER) using spaCy (only for named entities, no extra tokenization)
    doc = nlp(post["body"])
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    entity_counts = dict(Counter([ent.label_ for ent in doc.ents]))
    pos_counts = dict(Counter([token.pos_ for token in doc]))

    # Readability Metrics
    readability_scores = {
        "flesch": flesch_reading_ease(body_text),
        "smog_index": smog_index(body_text),
        "coleman_liau_index": coleman_liau_index(body_text),
        "automated_readability_index": automated_readability_index(body_text)
    }
    
    # Subjectivity
    subjectivity = TextBlob(body_text).sentiment.subjectivity
    lexical_diversity = len(set(words)) / len(words) if words else 0

    # Topic Modeling (LDA)
    dictionary = corpora.Dictionary([words])
    corpus = [dictionary.doc2bow(words)]
    lda_model = gensim.models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=10)
    topics = lda_model.print_topics()

    # Attach all results
    post.update({
        "sentiment": sentiment_result.output,
        "sentiment_probs": sentiment_result.probas,
        "emotion": emotion_result.output,
        "emotion_probs": emotion_result.probas,
        "entities": entities,
        "entity_counts": entity_counts,
        "pos_counts": pos_counts,
        "readability_scores": readability_scores,
        "subjectivity": subjectivity,
        "lexical_diversity": lexical_diversity,
        "topics": topics,
    })

    # Load existing posts from JSON
    if os.path.exists(news_data_file):
        with open(news_data_file, "r", encoding="utf-8") as f:
            try:
                all_posts = json.load(f)
            except json.JSONDecodeError:
                all_posts = {}
    else:
        all_posts = {}

    # Use post ID as key, or fallback to string id
    post_id = str(post.get("id", len(all_posts) + 1))
    all_posts[post_id] = post

    # Write updated posts back to JSON file
    with open(news_data_file, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=4, ensure_ascii=False)

    return post

def analyze_post(post):
    post = preprocess_post(post)
    return analyze_single_post(post)
