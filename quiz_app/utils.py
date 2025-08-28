from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import re

nlp = spacy.load('en_core_web_sm')

def preprocess(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

def compare_answers(user_answer, ideal_answer):
    processed_user = preprocess(user_answer)
    processed_ideal = preprocess(ideal_answer)
    
    if not processed_user or not processed_ideal:
        return 0, "Insufficient text for comparison"
    
    vectorizer = TfidfVectorizer()
    try:
        tfidf = vectorizer.fit_transform([processed_user, processed_ideal])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    except ValueError:
        return 0, "Could not compare answers"
    
    feedback = get_feedback(similarity)
    return similarity, feedback

def get_feedback(similarity):
    if similarity >= 0.8:
        return "Excellent match with the ideal answer!"
    elif similarity >= 0.6:
        return "Good answer, covers most key points."
    elif similarity >= 0.4:
        return "Partial match, some key points missing."
    return "Low similarity to expected answer. Review the topic."