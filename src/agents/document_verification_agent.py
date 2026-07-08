from __future__ import annotations

from src.schemas.models import DocumentVerificationResult


class DocumentVerificationAgent:
    def run(self, payload: dict) -> DocumentVerificationResult:
        document_type = payload.get("document_type", "document")
        status = payload.get("status", "valid")
        issues = []
        if status == "missing":
            issues.append("Required document is missing")
        if document_type == "photo" and status != "valid":
            issues.append("Passport photo must have a light background")

        return DocumentVerificationResult(document=document_type, status=status, issues=issues)
