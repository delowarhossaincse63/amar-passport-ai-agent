from __future__ import annotations


class FormFillingAgent:
    def run(self, applicant_data: dict) -> dict:
        case_type = applicant_data.get("case_type", "new")
        name = applicant_data.get("name")
        nid = applicant_data.get("nid")
        page_count = applicant_data.get("page_count", 36)

        missing = []
        if not name:
            missing.append("name")
        if not nid:
            missing.append("nid")

        if missing:
            return {"missing_fields": missing}

        passport_type = "Regular"

        return {
            "full_name": name,
            "case_type": case_type,
            "nid_number": nid,
            "passport_type": passport_type,
            "page_count": page_count,
            "photo_requirements": "Light background, recent, passport size",
            "supporting_documents": applicant_data.get("required_documents", []),
        }
