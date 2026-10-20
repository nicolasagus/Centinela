import json
import math
import os
import re
from typing import Dict, List, Tuple

class LocalVectorMemory:
    def __init__(self):
        self.documents: List[Dict[str, str]] = []
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.tfidf_matrix: List[List[float]] = []

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b[a-zA-Z0-9_]{2,}\b", text.lower())

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, str] = None):
        self.documents.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata or {}
        })

    def build_index(self):
        doc_count = len(self.documents)
        if doc_count == 0:
            return

        doc_tokens = [self._tokenize(doc["content"]) for doc in self.documents]
        df = {}

        # 1. Vocabulario y Document Frequency
        for tokens in doc_tokens:
            unique_terms = set(tokens)
            for term in unique_terms:
                df[term] = df.get(term, 0) + 1

        self.vocabulary = {term: idx for idx, term in enumerate(sorted(df.keys()))}
        vocab_size = len(self.vocabulary)

        # 2. Inverse Document Frequency (IDF)
        self.idf = {
            term: math.log((doc_count + 1.0) / (df[term] + 1.0)) + 1.0
            for term in self.vocabulary
        }

        # 3. Vectores TF-IDF normalizados L2
        self.tfidf_matrix = []
        for tokens in doc_tokens:
            vec = [0.0] * vocab_size
            for term in tokens:
                if term in self.vocabulary:
                    vec[self.vocabulary[term]] += 1.0

            norm = 0.0
            for term, idx in self.vocabulary.items():
                vec[idx] *= self.idf[term]
                norm += vec[idx] ** 2

            norm = math.sqrt(norm)
            if norm > 0.0:
                vec = [val / norm for val in vec]
            self.tfidf_matrix.append(vec)

    def search(self, query: str, top_k: int = 2) -> List[Tuple[str, float]]:
        if not self.tfidf_matrix:
            return []

        tokens = self._tokenize(query)
        q_vec = [0.0] * len(self.vocabulary)
        for term in tokens:
            if term in self.vocabulary:
                q_vec[self.vocabulary[term]] += 1.0

        norm = 0.0
        for term, idx in self.vocabulary.items():
            q_vec[idx] *= self.idf[term]
            norm += q_vec[idx] ** 2

        norm = math.sqrt(norm)
        if norm > 0.0:
            q_vec = [val / norm for val in q_vec]

        scores = []
        for idx, doc_vec in enumerate(self.tfidf_matrix):
            sim = sum(q_vec[i] * doc_vec[i] for i in range(len(self.vocabulary)))
            scores.append((self.documents[idx]["id"], round(sim, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

if __name__ == "__main__":
    memory = LocalVectorMemory()
    memory.add_document("errors.ts", "Network timeout and token bucket rate limit exceeded errors.")
    memory.add_document("bucket.ts", "TokenBucket class implementation with capacity and refill rate in TypeScript.")
    memory.add_document("circuit_breaker.py", "Circuit breaker state machine monitor stopping infinite loops.")
    memory.build_index()

    query = "rate limiting bucket logic"
    results = memory.search(query)
    print(f"[VectorMemory] Busqueda para '{query}':")
    for doc_id, score in results:
        print(f"  -> {doc_id} (Similitud Coseno: {score})")