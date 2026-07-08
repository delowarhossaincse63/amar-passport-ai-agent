from __future__ import annotations

import json
import os
import re
from typing import Any, Protocol

import httpx
from pydantic import BaseModel, Field, ValidationError

OPENAI_CHAT_COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo-0613"


class ApplicantExtractionResult(BaseModel):
    name: str | None = Field(None, description="Applicant full name")
    nid: str | None = Field(None, description="Applicant NID number")
    age: int | None = Field(None, description="Applicant age in years")

    @classmethod
    def normalize(cls, data: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}

        if name := data.get("name"):
            normalized["name"] = str(name).strip()

        nid = data.get("nid")
        if nid is not None:
            nid_digits = re.sub(r"\D", "", str(nid))
            if nid_digits:
                normalized["nid"] = nid_digits

        age = data.get("age")
        if isinstance(age, str) and age.isdigit():
            normalized["age"] = int(age)
        elif isinstance(age, int):
            normalized["age"] = age

        return normalized


class ApplicantExtractor(Protocol):
    def extract(self, text: str) -> ApplicantExtractionResult:
        ...


class RegexApplicantExtractor:
    NAME_PATTERN = re.compile(
        r"\b(?:name|nam)\b[^A-Za-z0-9\n\r,]{0,10}([A-Za-z][A-Za-z ]{1,80})",
        re.I,
    )
    AGE_PATTERN = re.compile(
        r"\b(?:age|boyosh)\b[^0-9]{0,5}(\d{1,3})\b|\b(\d{1,3})\s*(?:years|yrs|years old|boyosh)\b",
        re.I,
    )
    NID_PATTERN = re.compile(r"\b(\d{10})\b")

    def extract(self, text: str) -> ApplicantExtractionResult:
        name = None
        nid = None
        age = None

        name_match = self.NAME_PATTERN.search(text)
        if name_match:
            name = name_match.group(1).strip()

        nid_match = self.NID_PATTERN.search(text)
        if nid_match:
            nid = nid_match.group(1)

        age_match = self.AGE_PATTERN.search(text)
        if age_match:
            age_str = age_match.group(1) or age_match.group(2)
            if age_str and age_str.isdigit():
                age = int(age_str)

        return ApplicantExtractionResult(name=name, nid=nid, age=age)


class OpenAIApplicantExtractor:
    def __init__(self, api_key: str | None = None, model: str = DEFAULT_OPENAI_MODEL) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI applicant extraction")

    def extract(self, text: str) -> ApplicantExtractionResult:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a strict data extractor. Extract applicant information from free text, "
                        "and return it only through the provided function schema."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Extract the applicant's full name, NID number, and age from this text. "
                        "If a field is not present, omit it from the JSON output. "
                        "Do not invent values.\n\n"
                        f"Text: {text}"
                    ),
                },
            ],
            "functions": [
                {
                    "name": "extract_applicant_data",
                    "description": "Extract structured applicant details from a textual passport application request.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The applicant's full name.",
                                "minLength": 1,
                            },
                            "nid": {
                                "type": "string",
                                "description": "The applicant's 10-digit NID number.",
                                "pattern": "^\\d{10}$",
                            },
                            "age": {
                                "type": "integer",
                                "description": "The applicant's age in completed years.",
                                "minimum": 0,
                            },
                        },
                        "required": [],
                    },
                }
            ],
            "function_call": {"name": "extract_applicant_data"},
        }

        response = httpx.post(
            OPENAI_CHAT_COMPLETION_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        choice = data["choices"][0]
        function_call = choice["message"].get("function_call")
        if not function_call or "arguments" not in function_call:
            raise RuntimeError("OpenAI did not return structured applicant extraction data")

        try:
            arguments = json.loads(function_call["arguments"])
        except json.JSONDecodeError as exc:
            raise RuntimeError("Unable to decode OpenAI extraction output") from exc

        normalized = ApplicantExtractionResult.normalize(arguments)
        try:
            return ApplicantExtractionResult(**normalized)
        except ValidationError as exc:
            raise RuntimeError("OpenAI extraction result failed validation") from exc
