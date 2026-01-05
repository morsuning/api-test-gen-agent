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

## 7. 私有环境部署指南 (Private Environment Deployment)

如果您的运行环境无法连接互联网，但可以通过 Artifactory 等私有制品库获取依赖，请按照以下指南进行配置。

### 7.1 前置准备

请确保您拥有以下信息：
* **私有 PyPI 源地址**: 例如 `https://artifactory.example.com/artifactory/api/pypi/pypi-local/simple`
* **私有 NPM 源地址**: 例如 `https://artifactory.example.com/artifactory/api/npm/npm-local/`
* **认证信息**: 用户名/密码 或 Auth Token。

### 7.2 后端配置 (Python/uv)

本项目使用 `uv` 进行包管理。您可以通过设置环境变量来指定私有源，无需修改代码。

1. **配置环境变量**

   在终端中执行以下命令 (临时生效) 或写入 `~/.bashrc` / `.zshrc` (永久生效)：

   ```bash
   # 替换为您的私有源地址和认证信息
   export UV_INDEX_URL="https://<username>:<password>@artifactory.example.com/artifactory/api/pypi/pypi-local/simple"
   
   # 如果私有源使用自签名证书，可能还需要跳过 SSL 验证 (生产环境请谨慎使用)
   # export UV_NATIVE_TLS=1 
   ```

   或者，如果您的私有源不需要认证，或者您希望显式配置，可以修改 `backend/pyproject.toml` (不推荐，会污染源码) 或创建一个 `uv.toml` 文件：

   ```toml
   # backend/uv.toml
   [[index]]
   url = "https://artifactory.example.com/artifactory/api/pypi/pypi-local/simple"
   default = true
   ```

2. **安装依赖**

   ```bash
   cd backend
   uv sync
   ```

### 7.3 前端配置 (Frontend/Bun)

前端使用 `bun` 作为运行时和包管理器。由于 `bun` 兼容 `npm` 的配置，我们可以通过 `.npmrc` 文件配置私有源。

1. **创建配置文件**

   在 `frontend` 目录下创建一个名为 `.npmrc` 的文件：

   ```ini
   # frontend/.npmrc
   registry=https://artifactory.example.com/artifactory/api/npm/npm-local/
   
   # 如果需要认证 (Auth Token 方式)
   //artifactory.example.com/artifactory/api/npm/npm-local/:_authToken=YOUR_AUTH_TOKEN
   
   # 或者 (用户名/密码 Base64 方式)
   # _auth=BASE64_ENCODED_USER_PASS
   # always-auth=true
   ```

2. **安装依赖**

   ```bash
   cd frontend
   bun install
   ```

   *注意：如果遇到 `bun` 安装某些二进制包 (如 esbuild) 失败，可能需要手动下载对应平台的二进制文件并配置路径，或者请求网络权限放行 `github.com`。*

### 7.4 启动服务

配置完成后，启动步骤与常规流程一致：

1. **启动后端**
   ```bash
   cd backend
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **启动前端**
   ```bash
   cd frontend
   bun dev --host
   ```
   
   若需部署到生产环境 (构建静态资源)：
   ```bash
   cd frontend
   bun run build
   # 构建产物位于 dist 目录，可使用 nginx 托管
   ```

