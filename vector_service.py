import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple

class VectorService:
    def __init__(self, model_name: str = 'tfidf'):
        """
        Initializes the VectorService using TfidfVectorizer for lightweight matching.
        Avoids heavy neural network dependencies like PyTorch and FAISS.
        """
        print("Initializing lightweight TF-IDF VectorService...")
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.documents = [] # List of dicts
        self.texts = []
        self.tfidf_matrix = None
        self.is_fitted = False

    def add_documents(self, documents: List[dict]):
        if not documents:
            return

        for doc in documents:
            self.documents.append(doc)
            self.texts.append(doc['text'])
            
        # Fit the vectorizer
        self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)
        self.is_fitted = True

    def search(self, query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        if not self.is_fitted or not self.documents:
            return []
            
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        # Sort indices by similarity descending
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append((self.documents[idx], float(similarities[idx])))
            
        return results

    def get_all_embeddings(self) -> Tuple[np.ndarray, List[dict]]:
        if not self.is_fitted:
            return np.array([]), []
            
        # For PCA, we need dense arrays. TFIDF returns sparse arrays.
        dense_matrix = self.tfidf_matrix.toarray()
        return dense_matrix, self.documents
        
    # We also need a way to encode the query for the PCA plot in app.py
    class ModelMock:
        def __init__(self, vectorizer):
            self.vectorizer = vectorizer
        def encode(self, texts, convert_to_numpy=True):
            if not getattr(self.vectorizer, 'vocabulary_', None):
                # If vectorizer is empty, return zeros
                return np.zeros((len(texts), 2))
            return self.vectorizer.transform(texts).toarray()
            
    @property
    def model(self):
        return self.ModelMock(self.vectorizer)

    def reset(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.documents = []
        self.texts = []
        self.tfidf_matrix = None
        self.is_fitted = False
