from app.agent.prompts.factory import IPromptStrategy
from app.models.schemas import TestCase

class HighTierStrategy(IPromptStrategy):
    """
    高级模型策略 (例如 Gemini Pro, GPT-4)。
    利用思维链 (CoT) 和更抽象的指令。
    """

    def plan_tests_prompt(self, spec_summary: str) -> str:
        return f"""
你是一名资深的 QA 自动化专家。你的任务是根据提供的 OpenAPI 接口定义，设计一份全面的测试计划。

**输入数据：**
OpenAPI 摘要:
```json
{spec_summary}
```

**任务要求：**
1. 仔细分析每个 API 端点的功能、参数和约束。
2. 为每个端点设计测试用例，覆盖以下场景：
   - **Happy Path (正向)**: 正常的请求，预期 200 OK。
   - **Negative Path (逆向)**: 无效的输入，预期 400 Bad Request (如必填项缺失、类型错误)。
   - **Boundary Case (边界)**: 边界值测试 (如最大长度、最大数值)。
3. 请只输出 JSON 格式的测试计划列表，不要包含任何 Markdown 代码块外的解释。

**输出格式示例：**
[
  {{
    "id": "test_get_users_001",
    "name": "获取用户列表成功",
    "description": "验证使用合法参数调用 /users 能返回 200",
    "endpoint": "/users",
    "method": "GET",
    "type": "positive",
    "expected_status": 200,
    "data_requirements": "无需特殊数据"
  }}
]

**开始分析并生成计划：**
"""

    def generate_code_prompt(self, case: TestCase, spec_summary: str, language: str) -> str:
        return f"""
你是一名精通 {language} 的代码生成专家。请根据以下测试用例和 API 定义生成可执行的测试代码。

**OpenAPI 定义：**
```json
{spec_summary}
```

**测试用例详情：**
- 名称: {case.name}
- 描述: {case.description}
- 端点: {case.endpoint} [{case.method}]
- 类型: {case.type}
- 预期状态码: {case.expected_status}

**生成要求：**
1. 生成完整的、独立的 {language} 测试函数或脚本。
2. 包含必要的导入语句。
3. 请使用标准库或主流库 (Java: RestAssured, Go: net/http/httptest 或标准库)。
4. 代码必须包含对响应状态码的断言。
5. 请添加清晰的中文注释解释代码逻辑。
6. 只输出代码，不要包含 Markdown 格式标记。

**开始生成代码：**
"""
