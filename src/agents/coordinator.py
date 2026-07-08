from __future__ import annotations

import re

from src.agents.document_verification_agent import DocumentVerificationAgent
from src.agents.eligibility_agent import EligibilityAgent
from src.agents.fee_appointment_agent import FeeAppointmentAgent
from src.agents.form_filling_agent import FormFillingAgent
from src.schemas.models import CrewResponse


class CoordinatorAgent:
    def __init__(self) -> None:
        self.eligibility_agent = EligibilityAgent()
        self.document_verification_agent = DocumentVerificationAgent()
        self.fee_appointment_agent = FeeAppointmentAgent()
        self.form_filling_agent = FormFillingAgent()

    def run(self, message: str, session_id: str) -> CrewResponse:
        eligibility = self.eligibility_agent.run(message)
        verification = self.document_verification_agent.run(
            {"document_type": "photo", "status": "valid"}
        )
        fee_appointment = self.fee_appointment_agent.run(
            case_type=eligibility.case_type,
            service_level="regular",
        )
        # Try to extract name and NID from the user's message. Do not fabricate values.
        applicant_data: dict = {
            "case_type": eligibility.case_type,
            "page_count": 36,
            "required_documents": eligibility.required_documents,
        }

        nid_match = re.search(r"\b(\d{10})\b", message)
        if nid_match:
            applicant_data["nid"] = nid_match.group(1)

        # Simple name extraction: look for patterns like 'my name is X' or "I'm X".
        name_match = re.search(r"(?:my name is|i am|i'm)\s+([A-Za-z][A-Za-z ]{1,80})", message, re.I)
        if name_match:
            applicant_data["name"] = name_match.group(1).strip()

        form_draft = self.form_filling_agent.run(applicant_data)

        next_steps = [
            "Verify your eligibility and required documents",
            "Upload the verified documents",
            "Review the drafted application before submission",
            "Confirm the fee and select an appointment slot",
        ]

        # If the case is a minor applicant, explicitly surface guardian requirements
        if eligibility.case_type == "minor":
            guardian_notes = [
                "Provide guardian NID",
                "Upload signed consent form from guardian",
            ]
            # insert guardian-specific steps after eligibility verification
            next_steps[1:1] = guardian_notes

        base_response = (
            f"I classified your case as {eligibility.case_type}. "
            f"Required documents: {', '.join(eligibility.required_documents)}. "
            f"Document verification status: {verification.status}. "
            f"Estimated fee is {fee_appointment['fee']['amount']} {fee_appointment['fee']['currency']}. "
        )

        # If form_draft indicates missing fields, ask the user to provide them instead of fabricating.
        if isinstance(form_draft, dict) and form_draft.get("missing_fields"):
            missing = form_draft["missing_fields"]
            for m in missing:
                if m == "name":
                    next_steps.insert(1, "Provide your full name (as on NID)")
                if m == "nid":
                    next_steps.insert(1, "Provide your NID number")

            response = (
                base_response
                + "I need your name and NID number to draft the form — I cannot fabricate them."
            )
        else:
            response = (
                base_response
                + f"Draft form is ready with name {form_draft['full_name']} and NID {form_draft['nid_number']}."
            )

        if eligibility.case_type == "minor":
            response += " Please note: guardian NID and a consent form signed by the guardian are required for minor applicants."

        return CrewResponse(
            status="ok",
            case_type=eligibility.case_type,
            next_steps=next_steps,
            response=response,
            source_clause=eligibility.source_clause,
        )
