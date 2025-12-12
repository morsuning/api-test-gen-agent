from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field

class LLMConfig(BaseModel):
    """LLM 配置模型 (Generic OpenAI)"""
    base_url: str = Field(..., description="API Base URL")
    api_key: str = Field(..., description="API Key")
    model_name: str = Field(..., description="模型名称")
    tier: Literal["high", "low"] = Field(..., description="模型层级: high (复杂) 或 low (简单)")

class GenerateRequest(BaseModel):
    """生成测试用例的请求体"""
    openapi_content: str = Field(..., description="OpenAPI 规范内容的字符串 (JSON 或 YAML)")
    target_language: Literal["curl", "java", "go"] = Field(..., description="目标编程语言")
    llm_config: LLMConfig = Field(..., description="LLM 配置")
    include_boundary: bool = Field(False, description="是否包含边界测试")
    include_negative: bool = Field(True, description="是否包含逆向测试 (400 Bad Request)")

class TestScenario(BaseModel):
    """单个测试场景的定义"""
    id: str = Field(..., description="测试用例唯一 ID")
    name: str = Field(..., description="测试用例名称")
    description: str = Field(..., description="测试用例描述")
    endpoint: str = Field(..., description="测试的 API 端点路径")
    method: str = Field(..., description="HTTP 方法")
    type: Literal["positive", "negative", "boundary"] = Field(..., description="测试类型")
    expected_status: int = Field(..., description="预期的 HTTP 状态码")
    data_requirements: Optional[str] = Field(None, description="对测试数据的要求描述")

class TestCase(TestScenario):
    """包含生成代码的测试用例"""
    code: Optional[str] = Field(None, description="生成的测试代码片段")

class GenerateResponse(BaseModel):
    """生成操作的响应体"""
    task_id: str = Field(..., description="任务 ID")
    status: Literal["processing", "completed", "failed"] = Field(..., description="任务状态")
    result: Optional[Dict[str, Any]] = Field(None, description="结果数据，包含生成的代码和计划")
    error: Optional[str] = Field(None, description="错误信息")
