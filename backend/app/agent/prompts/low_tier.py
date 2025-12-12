from app.agent.prompts.factory import IPromptStrategy
from app.models.schemas import TestCase
import json

class LowTierStrategy(IPromptStrategy):
    """
    低级模型策略 (例如 Qwen 32B)。
    使用更严格的结构化输出和 Few-Shot 示例来防止幻觉。
    """

    def plan_tests_prompt(self, spec_summary: str) -> str:
        return f"""
任务：生成 API 测试用例列表。
必须严格输出 JSON 格式。

API 定义:
{spec_summary}

请列出所有端点的测试用例 (正向、逆向、边界)。

输出 JSON 格式模版:
[
  {{
    "id": "如果API是 /users, ID可以是 test_users_success",
    "name": "用例名称",
    "description": "简短描述",
    "endpoint": "/path",
    "method": "GET",
    "type": "positive",
    "expected_status": 200,
    "data_requirements": "无"
  }}
]
"""

    def generate_code_prompt(self, case: TestCase, spec_summary: str, language: str) -> str:
        # 简单模型可能需要更明确的代码结构指引
        requirements = ""
        if language == "go":
            requirements = "使用 Go标准库 `net/http` 和 `testing` 包。函数必须以 `Test` 开头。"
        elif language == "java":
            requirements = "使用 RestAssured。类名必须以 `Test` 结尾。"
        
        return f"""
任务：编写 {language} 测试代码。

API 上下文:
{spec_summary}

当前测试用例:
{json.dumps(case.dict(), ensure_ascii=False)}

要求:
1. {requirements}
2. 即使是简单的 GET 请求，也要写完整的函数。
3. 断言 HTTP 状态码是否为 {case.expected_status}。
4. 仅输出代码文本。

代码:
"""
