import spacy
import gensim
import gensim.corpora as corpora
from preprocess_data import preprocess_post, get_news_data, load_posts
from pysentimiento import create_analyzer
from textstat import flesch_reading_ease

news_data_file = "/app/model/news_data.json"

# Load sentiment and emotion analyzers
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
emotion_analyzer = create_analyzer(task="emotion", lang="en")

def analyze_single_post(post):
    print(post)
    # Sentiment & Emotion
    sentiment_result = sentiment_analyzer.predict(post["body"])
    emotion_result = emotion_analyzer.predict(post["body"])

    # Named Entity Recognition (NER) using spaCy (only for named entities, no extra tokenization)
    doc = nlp(post["body"])
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Readability Score
    readability = flesch_reading_ease(post["body"])

    # Lexical Diversity (using pre-tokenized text)
    words = post["tokenized_body"]  # Assuming 'tokens' is the pre-tokenized list of words
    lexical_diversity = len(set(words)) / len(words) if words else 0

    # Topic Modeling (LDA)
    dictionary = corpora.Dictionary([words])
    corpus = [dictionary.doc2bow(words)]
    lda_model = gensim.models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=10)
    topics = lda_model.print_topics()

    # Attach results
    post.update({
        "sentiment": sentiment_result.output,  # POSITIVE, NEGATIVE, NEUTRAL
        "emotion": emotion_result.output,
        "entities": entities,
        "readability": readability,
        "lexical_diversity": lexical_diversity,
        "topics": topics
    })

    return post

# Run preprocessing
get_news_data()
posts = load_posts(news_data_file)

post = posts[0]

post = preprocess_post(post)
analyzed_post = analyze_single_post(post)
print(analyzed_post)