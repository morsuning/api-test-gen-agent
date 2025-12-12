# 系统设计：API 测试用例生成代理

## 1. 实施方法

系统设计为一个**单页应用程序 (SPA)**，由 **FastAPI** 后端驱动，使用 **LangGraph** 编排 AI 代理。核心差异化在于 **多模型适应性 (Multi-model Adaptability)**，通过动态切换提示词策略，确保代理在高端（Gemini/Kimi）和低端（Qwen）模型上都能达到最佳性能。

### 核心技术

*   **前端**：React, TypeScript, Vite, Shadcn-ui, Tailwind CSS。
*   **后端**：Python 3.10+, FastAPI。
*   **代理编排**：LangGraph (StateGraph)。
*   **数据解析**：PyYAML, Pydantic。
*   **LLM 集成**：LangChain (ChatOpenAI/ChatGoogleGenerativeAI 包装器)。

### 关键架构决策

1.  **无状态与有状态 (Stateless vs Stateful)**：从 API 调用者的角度来看，后端将每个生成请求视为无状态运行，但在内部，LangGraph 维护生成过程的状态（规划 -> 生成 -> 审查）。
2.  **提示词策略模式 (Strategy Pattern for Prompts)**：为了处理“多模型适应性”需求，我们实现了一个 `PromptFactory`，它根据用户选择的模型返回不同的提示词模板。

    *   **高级 (High-Tier)**：使用思维链 (CoT) 和抽象指令。
    *   **低级 (Low-Tier)**：使用严格的结构化输出（JSON 模式）和少样本示例以防止幻觉。

3.  **模块化代码生成 (Modular Code Generation)**：代理不是生成一个巨大的文件，而是为每个测试用例生成代码片段，然后由最终的聚合器组装。这减少了上下文窗口的压力。

## 2. 用户与 UI 交互行为

1.  **上传阶段 (Upload Phase)**：

    *   用户拖放 JSON/YAML 文件。
    *   系统验证格式并显示可用 API 路径的树状视图。

2.  **配置阶段 (Configuration Phase)**：

    *   用户选择目标路径（默认：全部）。
    *   用户选择目标语言（cURL, Java, Go）。
    *   用户选择模型层级（高级/低级）。

3.  **生成阶段 (Generation Phase)**：

    *   用户点击“生成”。
    *   进度条显示当前代理步骤（规划 -> 生成 -> 审查）。
    *   实时日志（可选）显示代理的“思维过程”。

4.  **结果阶段 (Result Phase)**：

    *   分屏视图：左侧为测试用例列表，右侧为代码编辑器。
    *   用户可以复制代码或下载项目 ZIP 包。

## 3. 数据结构与接口

### 代理状态

```python
class AgentState(TypedDict):
    spec_summary: str          # 压缩后的 OpenAPI 规范
    raw_spec: dict             # 完整解析后的 JSON
    preferences: UserConfig    # 语言、模型等偏好设置
    test_plan: List[TestCase]  # 测试场景列表
    generated_code: Dict[str, str] # test_id -> 代码的映射
    final_output: str          # 组装后的文件内容
```

### 提示词策略接口

```python
class IPromptStrategy(ABC):
    @abstractmethod
    def plan_tests(self, spec: str) -> str: ...
  
    @abstractmethod
    def generate_code(self, case: TestCase, lang: str) -> str: ...
```

## 4. 程序调用流程

流程是线性的，但由图编排：

1.  **解析器 (Parser)**：从上传的文件中提取 `paths`、`methods` 和 `schemas`。
2.  **规划器节点 (Planner Node)**：

    *   输入：压缩后的规范。
    *   动作：要求 LLM 列出测试场景（正常路径、400 错误请求、边界检查）。
    *   输出：测试用例的 JSON 列表。

3.  **生成器节点 (Generator Node)** (Map/Reduce 风格)：
    *   输入：单个测试用例 + Schema。
    *   动作：要求 LLM 用目标语言为该特定用例编写代码。
    *   输出：代码字符串。
4.  **聚合器 (Aggregator)**：将代码片段组合成有效文件（添加导入、主函数）。

## 5. 不明确方面与假设

*   **认证 (Auth)**：我们假设生成的代码将包含用于认证的占位符（例如 `YOUR_TOKEN_HERE`）。代理在生成过程中不会处理真实的登录流程。
*   **依赖项 (Dependencies)**：对于 MVP，我们假设 API 调用是独立的。复杂的链式调用（创建 ID -> 使用 ID）是未来的增强功能。
*   **模拟 (Mocking)**：对于 Go/Java，我们假设使用标准库。除非特别要求，否则我们不会生成复杂的模拟服务器设置。
