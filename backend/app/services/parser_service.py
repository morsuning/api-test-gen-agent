import json
import yaml
from typing import Dict, Any, List
from fastapi import HTTPException

class ParserService:
    """OpenAPI 规范解析服务"""

    @staticmethod
    def parse_spec_content(content: str) -> Dict[str, Any]:
        """
        解析 OpenAPI 内容字符串 (JSON 或 YAML) 为字典。
        """
        try:
            # 尝试作为 JSON 解析
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                # 尝试作为 YAML 解析
                return yaml.safe_load(content)
            except yaml.YAMLError as e:
                raise HTTPException(status_code=400, detail=f"Invalid OpenAPI format. Must be JSON or YAML. Error: {str(e)}")

    @staticmethod
    def simplify_spec(spec: Dict[str, Any]) -> str:
        """
        简化 OpenAPI 规范以供 LLM 使用。
        仅提取关键信息 (path, method, summary, parameters, responses) 以减少 Token 消耗。
        返回简化后的 JSON 字符串。
        """
        simplified = {
            "openapi": spec.get("openapi", "3.0.0"),
            "info": spec.get("info", {}),
            "paths": {}
        }

        paths = spec.get("paths", {})
        for path, methods in paths.items():
            simplified["paths"][path] = {}
            for method, details in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    continue
                
                method_data = {
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "operationId": details.get("operationId", ""),
                    "parameters": details.get("parameters", []),
                    "requestBody": details.get("requestBody", {}),
                    "responses": list(details.get("responses", {}).keys()) # 仅保留状态码
                }
                simplified["paths"][path][method.upper()] = method_data

        return json.dumps(simplified, ensure_ascii=False, indent=2)

    @staticmethod
    def validate_spec(spec: Dict[str, Any]) -> bool:
        """
        简单的 OpenAPI 规范验证。
        """
        if "openapi" not in spec and "swagger" not in spec:
            raise HTTPException(status_code=400, detail="Missing 'openapi' or 'swagger' version field.")
        if "paths" not in spec:
            raise HTTPException(status_code=400, detail="Missing 'paths' field.")
        return True
