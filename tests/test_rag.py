from src.rag.retriever import SimpleRAGRetriever


def test_rag_retriever_returns_relevant_rules():
    retriever = SimpleRAGRetriever()
    matches = retriever.search("renew passport requirements")

    assert matches
    assert any("renewal" in match["content"].lower() for match in matches)

def test_rag_retriever_loads_corpus():
    retriever = SimpleRAGRetriever()
    assert retriever.documents
    assert retriever.tfidf_matrix is not None
