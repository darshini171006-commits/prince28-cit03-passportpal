import json

import pytest

from passportpal.llm.extract import extract_fields
from passportpal.llm.gateway import FakeLLM, LLMGateway


@pytest.fixture
def prompt_file(tmp_path):
    prompt = tmp_path / "extract_v1.md"
    prompt.write_text("Extract passport information.", encoding="utf-8")
    return prompt


async def test_extract_fields_returns_all_five_fields(prompt_file):
    response = {
        "case_type": "new_passport",
        "document": "Aadhaar card",
        "annexure": "Annexure E",
        "fee": "1500",
        "condition": "Applicant must be present",
    }

    gateway = LLMGateway([FakeLLM(script=[json.dumps(response)])])

    result = await extract_fields(
        "I need a new passport.",
        gateway,
        prompt_path=prompt_file,
    )

    assert result == response
    assert len(result) == 5


async def test_missing_fields_are_returned_as_none(prompt_file):
    gateway = LLMGateway([FakeLLM(script=['{"case_type": "renewal"}'])])

    result = await extract_fields(
        "I want to renew my passport.",
        gateway,
        prompt_path=prompt_file,
    )

    assert result == {
        "case_type": "renewal",
        "document": None,
        "annexure": None,
        "fee": None,
        "condition": None,
    }


async def test_unknown_values_are_normalized_to_none(prompt_file):
    gateway = LLMGateway(
        [FakeLLM(script=['{"case_type": "unknown", "document": "", "annexure": "Unknown"}'])]
    )

    result = await extract_fields(
        "Passport application details.",
        gateway,
        prompt_path=prompt_file,
    )

    assert result == {
        "case_type": None,
        "document": None,
        "annexure": None,
        "fee": None,
        "condition": None,
    }


async def test_empty_input_is_rejected(prompt_file):
    gateway = LLMGateway([FakeLLM()])

    with pytest.raises(ValueError, match="cannot be empty"):
        await extract_fields(
            "   ",
            gateway,
            prompt_path=prompt_file,
        )


def test_invalid_json_is_rejected():
    from passportpal.llm.extract import _parse_json

    with pytest.raises(ValueError, match="invalid JSON"):
        _parse_json("{invalid json}")
