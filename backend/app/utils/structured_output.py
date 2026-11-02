"""
Opt-in OpenAI Structured Outputs support.

When LLM_STRUCTURED_OUTPUTS is enabled, callers send a strict JSON Schema
instead of the plain ``json_object`` mode. The existing parsers stay in place
as the fallback, so refusals, truncation and providers without schema support
are still handled by the old path.
"""

from typing import Any, Dict

from ..config import Config

JSON_OBJECT_FORMAT: Dict[str, str] = {"type": "json_object"}

PERSONA_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "bio": {"type": "string"},
        "persona": {"type": "string"},
        "age": {"type": "integer"},
        "gender": {"type": "string", "enum": ["male", "female", "other"]},
        "mbti": {"type": "string"},
        "country": {"type": "string"},
        "profession": {"type": "string"},
        "interested_topics": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "bio", "persona", "age", "gender", "mbti",
        "country", "profession", "interested_topics",
    ],
    "additionalProperties": False,
}


def json_response_format(name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    """Return a strict json_schema response_format when enabled, else JSON mode."""

    if not Config.LLM_STRUCTURED_OUTPUTS:
        return dict(JSON_OBJECT_FORMAT)

    return {
        "type": "json_schema",
        "json_schema": {"name": name, "strict": True, "schema": schema},
    }
