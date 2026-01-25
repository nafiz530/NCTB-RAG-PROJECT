# index_store.py
import numpy as np
from collections import Counter
import re

class LexicalIndex:
    def __init__(self, lines):
        self.lines = lines
        self.texts = [self._preprocess(l["text"]) for l in lines if "text" in l]
        
        self.vocab = sorted(set(word for text in self.texts for word in text))
        self.vocab_size = len(self.vocab)
        self.word_to_idx = {w: i for i, w in enumerate(self.vocab)}
        
        self.tfidf_matrix = self._compute_tfidf()

    def _preprocess(self, text):
        if not text or not isinstance(text, str):
            return []
        text = text.lower()
        text = re.sub(r'[^\u0980-\u09FF\s]', ' ', text)
        words = [w for w in text.split() if w.strip()]
        return words

    def _compute_tfidf(self):
        n_docs = len(self.texts)
        if n_docs == 0:
            return np.array([])
        
        tf_matrix = np.zeros((n_docs, self.vocab_size))
        for i, words in enumerate(self.texts):
            word_count = Counter(words)
            total = len(words) if words else 1
            for word, cnt in word_count.items():
                if word in self.word_to_idx:
                    tf_matrix[i, self.word_to_idx[word]] = cnt / total
        
        doc_freq = np.sum(tf_matrix > 0, axis=0) + 1e-10
        idf = np.log(n_docs / doc_freq) + 1
        
        tfidf = tf_matrix * idf
        norms = np.sqrt(np.sum(tfidf**2, axis=1, keepdims=True))
        norms[norms == 0] = 1
        tfidf /= norms
        
        return tfidf

    def retrieve(self, query, top_k=5, use_exact=False):
        if use_exact:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            matches = []
            scores = []
            for i, words in enumerate(self.texts):
                full_text = ' '.join(words)
                if pattern.search(full_text):
                    matches.append(self.lines[i])
                    scores.append(1.0)
            if matches:
                return matches[:top_k], scores[:top_k]
            return [], []

        query_clean = self._preprocess(query)
        if not query_clean:
            return [], []
        
        query_vec = np.zeros(self.vocab_size)
        word_count = Counter(query_clean)
        total = len(query_clean)
        for word, cnt in word_count.items():
            if word in self.word_to_idx:
                query_vec[self.word_to_idx[word]] = cnt / total
        
        scores = np.dot(self.tfidf_matrix, query_vec)
        ranked_idx = scores.argsort()[::-1][:top_k]
        return [self.lines[i] for i in ranked_idx], [scores[i] for i in ranked_idx]