# API 测试用例生成智能体 (API Test Case Generation Agent)

## 1. 项目简介

本项目是一个基于 LangGraph 和 AI 大模型的智能代理系统，旨在自动化分析 OpenAPI (Swagger) 文档，并生成高质量的 API 测试用例及执行代码。系统结合了 React 前端和 FastAPI 后端，提供友好的用户交互体验。

## 2. 核心功能特性

* **智能解析**: 自动解析 JSON/YAML 格式的 OpenAPI 规范，提取关键接口信息。
* **自动化规划**: 基于接口定义，智能规划测试场景，覆盖正向 (Happy Path)、逆向 (Negative Path) 和边界条件 (Boundary Case)。
* **多语言代码生成**: 支持生成多种语言的测试代码：
  * **Go**: 使用 `testing` 和 `net/http`。
  * **Java**: 使用 RestAssured。
  * **cURL**: 命令行测试脚本。
* **鲁棒性增强**: 内置 `Robust JSON Parser`，能够自动修复 LLM 返回的非标准 JSON (如 Python 风格的字符串乘法 `"A" * 1000` 或 JS 风格的 `.repeat()` 方法)，大幅降低生成失败率。
* **多模型适应性**: 内置分层提示词策略 (Prompt Strategy)：
  * **High Tier**: 针对 GPT-4/Gemini Pro 等强模型，使用思维链 (CoT) 推理。
  * **Low Tier**: 针对 Qwen 等轻量模型，使用结构化 Few-Shot 引导。
* **配置管理**: 支持在前端设置 Base URL、API Key 和模型名称，且配置自动持久化。
* **可视化交互**: 提供全新的现代化 Web 界面进行文件上传、配置调整和结果预览。
* **可视化交互**: 提供全新的现代化 Web 界面进行文件上传、配置调整和ূল果预览。
* **可观测性**: 后端集成 Debug 日志中间件，实时记录所有 API 请求与响应详情。支持 **递归 JSON 格式化**，即使是嵌套在字符串中的 JSON 数据也会被展开显示，极大提升日志可读性。
* **LangGraph Debug 模式**: 支持在配置文件中开启 Debug 模式，自动将每个节点的输入输出状态记录到日志文件，便于调试智能体逻辑。
* **LangGraph Debug 模式**: 支持在配置文件中开启 Debug 模式，自动将每个节点的输入输出状态记录到日志文件，便于调试智能体逻辑。

## 3. 系统架构

系统采用前后端分离架构：

* **前端**: React, TypeScript, Vite, Tailwind CSS, Shadcn-ui。
* **后端**: Python FastAPI。
* **AI 编排**: LangGraph (StateGraph), LangChain。
* **包管理**: `uv` (Python), `bun` (Node.js)。

### 工作流 (LangGraph)

1. **Parser Node**: 解析并简化 OpenAPI 文档。
2. **Planner Node**: 生成测试计划列表。
3. **Generator Node**: 为每个计划生成具体代码。
4. **Aggregator Node**: 聚合所有代码片段，生成最终可执行文件。

## 4. 快速开始

### 环境要求

* Python 3.10+ (推荐使用 `uv` 管理)
* Node.js / Bun
* OpenAI API Key (或其他兼容 LLM Key)

### 后端启动

1. 进入后端目录：

   ```bash
   cd backend
   ```
2. 初始化环境并安装依赖：

   ```bash
   uv sync
   ```
3. 设置环境变量 (推荐在 `.env` 或 export)：

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
4. 启动服务器：

   ```bash
   uv run uvicorn app.main:app --reload
   ```

   API 文档地址: http://127.0.0.1:8000/docs

### 前端启动

1. 进入前端目录：

   ```bash
   cd frontend
   ```
2. 安装依赖：

   ```bash
   bun install
   ```
3. 启动开发服务器：

   ```bash
   bun dev
   ```

   访问地址: http://localhost:5173

## 5. 使用指南

1. 打开 Web 界面。
2. 将 OpenAPI JSON/YAML 文件拖入上传区域。
3. 点击右上角齿轮图标，配置 LLM (Base URL, API Key, Model Name)。
4. 在配置面板选择目标语言 (如 Go) 和 处理策略 (Deep/Fast)。
5. 勾选需要的测试类型 (如包含边界测试)。
6. 点击 "开始生成"。
7. 等待生成完成后，在右侧查看代码，左侧列表切换不同用例。

## 6. 常见问题与故障排除 (FAQ)

### LLM 连接错误 (404 Not Found)

如果遇到 `Planner Error: ... 404 - url.not_found` 错误，通常是因为 Base URL 配置不匹配。

* **解决方案**: 请检查 `backend/config.toml` 中的 **Base URL**，或通过前端设置面板调整。
* 系统支持自动修正：您可以直接填入服务商提供的完整 Endpoint，系统会自动识别并调整。
* 确保您的 API 服务提供商支持标准的 OpenAI 协议 (`/chat/completions` 路径)。
