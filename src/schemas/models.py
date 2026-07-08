from pydantic import BaseModel, Field
from typing import List


class EligibilityResult(BaseModel):
    case_type: str = Field(..., description="Type of passport case")
    required_documents: List[str] = Field(default_factory=list)
    source_clause: str = Field(..., description="Source clause from the rules corpus")


class DocumentVerificationResult(BaseModel):
    document: str = Field(..., description="Document name")
    status: str = Field(..., description="Verification outcome")
    issues: List[str] = Field(default_factory=list)


class CrewResponse(BaseModel):
    status: str
    case_type: str
    next_steps: List[str]
    response: str
    source_clause: str
