from src.agents.coordinator import CoordinatorAgent
from src.agents.eligibility_agent import EligibilityAgent
from src.agents.document_verification_agent import DocumentVerificationAgent
from src.agents.fee_appointment_agent import FeeAppointmentAgent
from src.agents.form_filling_agent import FormFillingAgent
from src.crew import run_crew


def test_eligibility_agent_classifies_renewal_case():
    agent = EligibilityAgent()
    result = agent.run("I want to renew my passport")

    assert result.case_type == "renewal"
    assert "Old passport" in result.required_documents
    assert result.source_clause


def test_document_verification_agent_flags_missing_photo():
    agent = DocumentVerificationAgent()
    result = agent.run({"document_type": "photo", "status": "missing"})

    assert result.status == "missing"
    assert result.issues


def test_fee_appointment_agent_returns_fee_and_slots():
    agent = FeeAppointmentAgent()
    result = agent.run(case_type="renewal", service_level="express")

    assert result["fee"]["amount"] == 1800
    assert result["appointment_slots"]


def test_form_filling_agent_creates_draft_application():
    agent = FormFillingAgent()
    result = agent.run(
        {
            "name": "Delowar Hossain",
            "nid": "1234567890",
            "case_type": "renewal",
            "page_count": 36,
            "required_documents": ["NID", "Old passport"],
        }
    )

    assert result["full_name"] == "Delowar Hossain"
    assert result["case_type"] == "renewal"
    assert "NID" in result["supporting_documents"]


def test_eligibility_agent_minor_requires_guardian_documents():
    agent = EligibilityAgent()
    result = agent.run("I am under 18 and need a passport")

    assert result.case_type == "minor"
    assert "Guardian NID" in result.required_documents
    assert any("consent" in doc.lower() for doc in result.required_documents)


def test_eligibility_agent_minor_matches_numeric_age():
    agent = EligibilityAgent()
    result = agent.run("I am 17 and need a passport")

    assert result.case_type == "minor"
    assert "Guardian NID" in result.required_documents


def test_coordinator_surfaces_guardian_requirements_for_minors():
    agent = CoordinatorAgent()
    result = agent.run("I am under 18 and need a passport", session_id="s1")

    assert result.status == "ok"
    assert result.case_type == "minor"
    assert any("guardian nid" in step.lower() for step in result.next_steps)
    assert any("consent" in step.lower() for step in result.next_steps)
    assert "guardian" in result.response.lower()


def test_coordinator_agent_routes_workflow():
    agent = CoordinatorAgent()
    result = agent.run(
        "My name is Delowar Hossain and my NID is 1234567890. I want to renew my passport",
        session_id="test-session",
    )

    assert result.status == "ok"
    assert result.case_type == "renewal"
    assert "Draft form is ready" in result.response
    assert result.source_clause


def test_run_crew_returns_structured_response():
    result = run_crew(
        "My name is Delowar Hossain and my NID is 1234567890. I want to renew my passport",
        session_id="test-session",
    )

    assert result["status"] == "ok"
    assert result["case_type"] == "renewal"
    assert result["next_steps"]
    assert result["source_clause"]
