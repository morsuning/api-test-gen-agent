# 产品需求文档 (PRD): API 测试用例生成智能体 (API Test Gen Agent)

## 1. 项目基本信息

* **项目名称** : `api_test_gen_agent`
* **文档语言** : 中文
* **编程语言** : TypeScript (Frontend), Python (Backend/Agent)
* **前端框架** : Shadcn-ui, Tailwind CSS
* **后端服务** : Supabase (用于存储历史记录和用户配置), Python FastAPI (用于承载 LangGraph Agent)
* **核心技术** : LangGraph, LangChain, OpenAPI Parser

### 原始需求回顾

用户希望创建一个基于 LangGraph的Agent，通过解析 OpenAPI 文档自动生成 API 测试用例及断言。 关键特性：

1. **多模型适配** : 在高级模型 (Gemini 3 Pro, Kimi k2, Deepseek V3.2) 和初级模型 (Qwen3-32b) 上均有良好表现。
2. **LangGraph 编排** : 使用 LangGraph 构建 Agent 工作流。
3. **全面覆盖** : 覆盖正向、逆向及边界测试场景。
4. **多语言导出** : 支持生成 cURL, Java (RestAssured), Go (testing + net/http/httptest) 代码。
5. **输入支持** : 上传或输入 OpenAPI (Swagger) JSON/YAML。

## 2. 产品定义

### 2.1 产品目标

1. **自动化与标准化** : 通过解析 OpenAPI 文档，自动化生成覆盖率高（正向/逆向/边界）的标准化测试用例，减少人工编写成本。
2. **模型鲁棒性适配** : 设计分层提示词策略 (Prompt Strategy)，确保 Agent 在不同能力的大模型（从 Qwen3-32b 到 Gemini 3 Pro）下都能输出可用的测试代码。
3. **灵活的工作流编排** : 利用 LangGraph 实现可观测、可干预的测试生成流水线（解析->规划->生成->审查）。

### 2.2 用户故事 (User Stories)

* **作为测试工程师** ，我希望上传 OpenAPI JSON 文件，以便 Agent 自动分析接口定义并生成测试计划。
* **作为开发人员** ，我希望选择生成的代码语言（如 Go 或 Java），以便直接将测试代码集成到现有的 CI/CD 流水线中。
* **作为项目经理** ，我希望能够配置使用不同的底层大模型（如成本较低的 Qwen 或能力较强的 Gemini），以便在成本和质量之间取得平衡。
* **作为测试工程师** ，我希望 Agent 能自动识别边界条件（如最大长度、空值），并生成对应的断言代码，以确保接口的健壮性。

### 2.3 竞品分析

| 竞品名称             | 优势                                         | 劣势                                                          | 我们的差异化策略                                                                                       |
| -------------------- | -------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Apidog**     | 一体化协作，生成用例功能成熟，可视化强。     | 商业软件，深度定制 AI 逻辑较难，主要依赖其内置逻辑。          | 专注于**Agentic Workflow** ，允许用户通过 LangGraph 自定义生成逻辑，且支持本地/私有模型 (Qwen)。 |
| **Postman AI** | 用户基数大，生态完善，支持自然语言生成测试。 | AI 功能主要作为辅助，缺乏针对复杂场景的自动规划和多模型适配。 | 强调**多模型适配** 和 **代码导出** 的灵活性，特别是针对 Go/Java 的原生代码生成。           |
| **Keploy**     | 流量录制回放，零代码生成测试。               | 依赖真实流量，对于新开发的无流量接口支持较弱。                | 基于**文档驱动 (Spec-Driven)** ，无需流量即可在开发阶段生成测试，支持 TDD。                      |
| **TestSprite** | 全自动自主测试，闭环反馈。                   | 较为复杂，主要面向企业级全流程。                              | 轻量级工具，专注于**测试代码生成** 这一具体环节，易于集成。                                      |

### 2.4 竞品四象限图

## 3. 技术规格

### 3.1 核心功能需求分析

#### 3.1.1 OpenAPI 解析与预处理

* **输入** : 支持文件上传 (.json, .yaml) 和 URL 导入。
* **解析** : 提取 Paths, Methods, Parameters (Query, Path, Body), Responses, Schemas。
* **验证** : 简单的格式校验，确保文档符合 OpenAPI 3.0/2.0 标准。

#### 3.1.2 LangGraph Agent 工作流

采用 **StateGraph** 架构，包含以下节点：

1. **Parser Node** : 解析 OpenAPI 文档，提取关键元数据。
2. **Planner Node** : 根据接口定义，规划测试场景（Happy Path, Negative Path, Boundary Case）。
3. **Generator Node** :

* 根据规划生成具体的测试数据。
* 根据目标语言（cURL/Java/Go）生成测试代码。
* **策略** : 针对不同模型应用不同的 Prompt 模板。

1. **Reviewer Node (Optional)** : 检查生成的代码语法和断言逻辑（可利用 LLM 自查）。

#### 3.1.3 多模型适配策略 (Prompt Engineering)

* **高级模型 (Gemini 3 Pro, Kimi k2)** :
* 使用  **Chain-of-Thought (CoT)** : “先分析接口约束，再列出测试点，最后编写代码”。
* 允许更复杂的逻辑推理，如依赖参数的关联生成。
* **初级模型 (Qwen3-32b)** :
* 使用  **Structured Few-Shot** : 提供明确的 JSON 结构或代码模板。
* 拆分任务：将“生成测试数据”和“生成代码”拆分为两个步骤，避免上下文丢失。
* 强制约束：在 System Prompt 中明确禁止由 AI 自由发挥的注释或无关文本。

#### 3.1.4 代码生成与导出

* **cURL** : 标准命令行格式。
* **Java** : 使用 RestAssured 库，包含 `@Test` 注解 (JUnit/TestNG 风格)。
* **Go** : 使用标准库 `testing` 配合 `net/http` 或 `httptest`，包含 `t.Run` 子测试结构。

### 3.2 需求池 (Requirements Pool)

| ID   | 需求描述                                            | 优先级 | 备注       |
| ---- | --------------------------------------------------- | ------ | ---------- |
| P0-1 | 支持 OpenAPI JSON/YAML 文件上传与解析               | P0     | 核心入口   |
| P0-2 | 基于 LangGraph 的基础生成工作流 (Parse->Generate)   | P0     | 核心架构   |
| P0-3 | 支持 cURL, Java (RestAssured), Go 代码生成          | P0     | 核心输出   |
| P0-4 | 覆盖正向 (200 OK) 和基础逆向 (400 Bad Request) 场景 | P0     | 基础质量   |
| P1-1 | 多模型差异化 Prompt 策略 (High/Low Tier)            | P1     | 性能优化   |
| P1-2 | 边界测试场景生成 (如最大长度、空值)                 | P1     | 质量提升   |
| P1-3 | 简单的 Web UI (Shadcn-ui) 用于交互和展示结果        | P1     | 用户体验   |
| P2-1 | 批量导出与下载功能                                  | P2     | 效率工具   |
| P2-2 | 对接 Supabase 存储历史生成记录                      | P2     | 数据持久化 |

### 3.3 UI 设计草图 (Web Interface)

1. **首页/配置页** :

* 左侧: 文件上传区域 (Drag & Drop)，URL 输入框。
* 右侧: 配置面板
  * **目标语言** : 下拉选择 [cURL, Java, Go]。
  * **模型选择** : 下拉选择 [Gemini 3 Pro, Kimi k2, Qwen3-32b]。
  * **生成策略** : 复选框 [包含边界测试, 包含逆向测试]。
* 底部: “开始生成” 按钮。

1. **结果预览页** :

* 左侧: 接口列表 (Tree View)。
* 右侧: 代码编辑器 (Read-only)，展示生成的测试代码。
* 功能区: “复制”, “下载文件”, “重新生成”。

### 3.4 待确认问题 (Open Questions)

1. **鉴权处理** : 用户上传的 OpenAPI 文档中是否包含鉴权信息？Agent 是否需要支持用户输入 Bearer Token 或 API Key 并在生成代码中自动填充？(目前假设用户需手动填充或提供占位符)。
2. **依赖接口** : 是否需要处理接口间的依赖关系（如先登录获取 Token，再调用查询接口）？(P0 阶段暂不处理复杂依赖，仅针对单接口生成)。

### 3.5 API 接口定义示例 (API Interface Examples)

#### 3.5.1 生成请求 (Request)

```json
{
  "openapi_content": "{\"openapi\": \"3.0.0\", \"info\": {\"title\": \"Sample API\", \"version\": \"1.0.0\"}, \"paths\": {\"/users\": {\"get\": {\"summary\": \"List users\", \"responses\": {\"200\": {\"description\": \"OK\"}}}}}}",
  "target_language": "go",
  "llm_config": {
    "provider": "openai",
    "model_name": "gpt-4o",
    "tier": "high"
  }
}
```

#### 3.5.2 生成响应 (Response)

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "generated_code": "package main\n\nimport (\n\t\"net/http\"\n\t\"net/http/httptest\"\n\t\"testing\"\n)\n\nfunc TestListUsers(t *testing.T) {\n\treq, err := http.NewRequest(\"GET\", \"/users\", nil)\n\tif err != nil {\n\t\tt.Fatal(err)\n\t}\n\n\trr := httptest.NewRecorder()\n\thandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {\n\t\tw.WriteHeader(http.StatusOK)\n\t})\n\n\thandler.ServeHTTP(rr, req)\n\n\tif status := rr.Code; status != http.StatusOK {\n\t\tt.Errorf(\"handler returned wrong status code: got %v want %v\",\n\t\t\tstatus, http.StatusOK)\n\t}\n}",
    "plan": [
      {
        "name": "Test List Users Success",
        "description": "Verify that the endpoint returns 200 OK",
        "type": "positive",
        "expected_status": 200
      }
    ]
  }
}
```

## 4. 附录

* **LangGraph 状态定义示例** :

```python
  class AgentState(TypedDict):
      openapi_spec: dict
      test_plan: List[str]
      target_language: str
      generated_code: str
      model_tier: Literal["high", "low"]
```
