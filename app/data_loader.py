from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_context_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_chunks(text, chunk_size=500):
    paragraphs = text.split('\n\n')
    chunks = [p.strip() for p in paragraphs if len(p.strip()) > 20]
    if not chunks:
        chunks = [text]
    return chunks

def find_best_context(question, chunks):
    vectorizer = TfidfVectorizer().fit([question] + chunks)
    vectors = vectorizer.transform([question] + chunks)
    similarity = cosine_similarity(vectors[0:1], vectors[1:])
    best_index = similarity.argmax()
    return chunks[best_index]
