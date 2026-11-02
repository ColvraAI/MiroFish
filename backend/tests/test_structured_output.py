from app.config import Config
from app.utils.structured_output import PERSONA_SCHEMA, json_response_format


def test_default_keeps_json_object_mode(monkeypatch):
    monkeypatch.setattr(Config, "LLM_STRUCTURED_OUTPUTS", False)

    assert json_response_format("persona", PERSONA_SCHEMA) == {"type": "json_object"}


def test_enabled_sends_strict_schema(monkeypatch):
    monkeypatch.setattr(Config, "LLM_STRUCTURED_OUTPUTS", True)

    fmt = json_response_format("persona", PERSONA_SCHEMA)

    assert fmt["type"] == "json_schema"
    assert fmt["json_schema"]["strict"] is True
    assert fmt["json_schema"]["schema"] is PERSONA_SCHEMA


def test_persona_schema_is_strict_compatible():
    props = set(PERSONA_SCHEMA["properties"])

    assert set(PERSONA_SCHEMA["required"]) == props
    assert PERSONA_SCHEMA["additionalProperties"] is False
