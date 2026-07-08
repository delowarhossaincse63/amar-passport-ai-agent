from __future__ import annotations

from pathlib import Path
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimpleRAGRetriever:
    def __init__(self, data_dir: str = "src/rag/data") -> None:
        self.documents: List[Dict[str, str]] = []
        self.corpus: List[str] = []
        self.ids: List[str] = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self._load_documents(data_dir)

    def _load_documents(self, data_dir: str) -> None:
        root = Path(data_dir)
        for file_path in root.glob("*.txt"):
            content = file_path.read_text(encoding="utf-8")
            self.documents.append(
                {
                    "id": file_path.stem,
                    "content": content,
                    "source_clause": file_path.name,
                }
            )
            self.corpus.append(content)
            self.ids.append(file_path.stem)

        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        else:
            self.tfidf_matrix = None

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, str]]:
        if not self.corpus or self.tfidf_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        ranked_indices = similarities.argsort()[::-1][:top_k]
        results = [self.documents[idx] for idx in ranked_indices if similarities[idx] > 0]
        return results
