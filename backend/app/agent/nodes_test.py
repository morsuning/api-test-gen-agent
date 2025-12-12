import pytest
from app.utils.json_parser import robust_json_parse

def test_robust_json_parsing_string_multiplication():
    # Extracted from error.log (Python style)
    invalid_json = """
    [
      {
        "id": "test_create_pet_009",
        "name": "创建宠物边界测试-name为超长字符串",
        "description": "验证name字段为256字符超长字符串时返回400 Bad Request",
        "expected_status": 400,
        "request_body": {
          "name": "a" * 256
        }
      }
    ]
    """
    data = robust_json_parse(invalid_json)
    assert isinstance(data, list)
    assert len(data) == 1
    assert len(data[0]["request_body"]["name"]) == 256
    assert data[0]["request_body"]["name"] == "a" * 256

def test_robust_json_parsing_js_repeat():
    # Simulated JS style
    invalid_json = """
    [
      {
        "id": "test_create_pet_009",
        "request_body": {
          "name": "b".repeat(10)
        }
      }
    ]
    """
    data = robust_json_parse(invalid_json)
    assert isinstance(data, list)
    assert data[0]["request_body"]["name"] == "bbbbbbbbbb"

def test_robust_json_parsing_missing_comma():
    # Common error: missing comma between objects
    invalid_json = """
    [
      {"id": "1"}
      {"id": "2"}
    ]
    """
    # json_repair usually handles this well
    data = robust_json_parse(invalid_json)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "1"
    assert data[1]["id"] == "2"

def test_robust_json_parsing_real_error_log_content():
    # The content from error.log (lines 535-796)
    # It contained "A" * 1000
    
    real_log_content = """
[
  {
    "id": "test_create_pet_006",
    "name": "Create pet - name with max length",
    "description": "POST /pets with a very long 'name' (e.g., 1000 chars) should return 201 if accepted",
    "endpoint": "/pets",
    "method": "POST",
    "type": "boundary",
    "expected_status": 201,
    "payload": { "name": "A" * 1000 },
    "data_requirements": "None"
  }
]
    """
    data = robust_json_parse(real_log_content)
    assert isinstance(data, list)
    assert len(data[0]["payload"]["name"]) == 1000
