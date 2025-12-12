import pytest
from app.services.parser_service import ParserService
from fastapi import HTTPException

def test_parse_json():
    content = '{"openapi": "3.0.0", "paths": {}}'
    parsed = ParserService.parse_spec_content(content)
    assert parsed["openapi"] == "3.0.0"

def test_parse_yaml():
    content = """
openapi: 3.0.0
paths: {}
"""
    parsed = ParserService.parse_spec_content(content)
    assert parsed["openapi"] == "3.0.0"

def test_validate_spec_valid():
    spec = {"openapi": "3.0.0", "paths": {}}
    assert ParserService.validate_spec(spec) is True

def test_validate_spec_invalid():
    spec = {"invalid": "field"}
    with pytest.raises(HTTPException):
        ParserService.validate_spec(spec)

def test_simplify_spec():
    spec = {
        "openapi": "3.0.0",
        "paths": {
            "/test": {
                "get": {
                    "summary": "Test Endpoint",
                    "parameters": [{"name": "id", "in": "query"}]
                }
            }
        }
    }
    summary = ParserService.simplify_spec(spec)
    assert "/test" in summary
    assert "GET" in summary
    assert "id" in summary
