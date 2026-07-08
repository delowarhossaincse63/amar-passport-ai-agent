from __future__ import annotations

import re

from src.schemas.models import EligibilityResult
from src.rag.retriever import SimpleRAGRetriever


class EligibilityAgent:
    MINOR_PATTERN = re.compile(
        r"\b(?:minor|under\s*18|below\s*(?:18|eighteen)|age\s*(?:1[0-7]|[0-9])|(?:i\s*am|i\s*'m|i'm|im)\s*(?:a\s*)?(?:1[0-7]|[0-9])(?:\s*years?)?)\b",
        re.I,
    )

    def __init__(self, retriever: SimpleRAGRetriever | None = None) -> None:
        self.retriever = retriever or SimpleRAGRetriever()

    def run(self, message: str) -> EligibilityResult:
        matches = self.retriever.search(message)
        query_lower = message.lower()

        if "renew" in query_lower or "renewal" in query_lower:
            case_type = "renewal"
            required_documents = ["Old passport", "NID", "2 copies passport-size photo"]
        elif "lost" in query_lower or "police report" in query_lower:
            case_type = "lost"
            required_documents = ["Police report", "NID", "Recent passport-size photo"]
        elif self.MINOR_PATTERN.search(message):
            case_type = "minor"
            required_documents = [
                "Birth certificate",
                "NID",
                "Guardian NID",
                "Consent form (signed by guardian)",
                "Recent passport-size photo",
            ]
        else:
            case_type = "new"
            required_documents = ["Birth certificate", "NID", "Recent passport-size photo"]

        source_clause = matches[0]["source_clause"] if matches else "src/rag/data/rules.txt"
        return EligibilityResult(
            case_type=case_type,
            required_documents=required_documents,
            source_clause=source_clause,
        )
