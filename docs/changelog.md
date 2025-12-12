# Changelog

## [Unreleased] - 2025-05-23

### Added

- **Backend Architecture**:
  - 初始化基于 FastAPI 和 Python 3.10+ 的后端项目。
  - 集成 `LangGraph` 实现智能体工作流编排。
  - 实现 OpenAPI 解析服务 (`ParserService`)。
  - 实现提示词策略工厂 (`PromptFactory`)，支持 High Tier (CoT) 和 Low Tier (Structured) 策略。
  - 实现 `Parser`, `Planner`, `Generator` 节点逻辑。
  - 使用 `uv` 进行依赖管理。
- **Frontend Architecture**:
  - 初始化基于 React, TypeScript, Vite 的前端项目。
  - 切换构建工具为 `Bun`。
  - 集成 `Shadcn-ui` 和 `Tailwind CSS` 进行 UI 开发。
  - 实现文件上传组件 (`UploadSection`)。
  - 实现配置面板组件 (`ConfigPanel`)。
  - 实现结果展示与代码编辑器组件 (`ResultEditor`)。
- **Documentation**:
  - 创建 `docs/project.md` 项目主文档。
  - 创建 `docs/agent_architecture.md` 架构详解文档。
  - 翻译 `docs/.wiki.md` 和 `docs/system_design.md` 为中文。
- **Configuration & UI Overhaul (2025-12-12)**:
  - **Backend**: 新增 `/settings` API 及持久化服务，支持保存 LLM 配置。
  - **Backend**: 移除硬编码 Provider，全面转向通用 OpenAI 兼容接口。
  - **Frontend**: 全新重构 `ConfigPanel`，支持隐藏式配置和玻璃拟态 UI。
  - **Frontend**: 修复 `tailwindcss-animate` 依赖缺失导致的动画失效问题。
  - **Frontend**: 修复侧边栏配置遮挡问题及 Settings Modal 定位异常。
  - **Backend**: 将默认目标语言调整为 `cURL`。
  - **Backend**: 修复工作流调用错误 (`StateGraph` object has no attribute 'invoke')，正确使用编译后的 `agent_app`。
  - **Backend**: 修复 LLM 调用时 Base URL 路径处理问题 (404 Error)，增加对 input URL 的自动清理逻辑。
  - **Backend**: 优化 Planner 及 Generator 节点的错误提示，明确指示配置错误原因。
  - **Backend**: 优化请求日志输出，支持 JSON 格式化打印 (Pretty Print) 且移除冗余的 UUID，提升开发体验。
  - **Backend**: 增强 Planner 节点的 JSON 解析鲁棒性，使用 Regex 提取 JSON 内容，防止因 Markdown 包裹或额外文本导致的解析失败。
  - **Backend**: 引入 `PyYAML` 作为 JSON 解析的容错方案，自动修复常见的 LLM 输出格式错误（如缺少逗号、尾部逗号等）。
  - **Backend (2025-12-12)**: 补全 `LangGraph` 逻辑，新增 `Aggregator` 节点，实现完整的 `Parser -> Planner -> Generator -> Aggregator` 工作流。
  - **Backend**: 修复 `batch_generator_node` 状态更新丢失的问题，确保代码聚合正常工作。
  - **Backend**: 引入 `json_repair` 库并实现 `robust_json_parse` 工具，彻底解决 LLM 生成 Python/JS 风格代码 (string multiplication) 导致的 JSON 解析错误。
  - **Backend**: 新增 LangGraph Debug 模式，支持通过 `config.toml` 配置 `debug_mode` 和 `debug_log_path`。
  - **Backend**: 增强请求日志功能，支持 **递归解包** 嵌套的 JSON 字符串，确保日志以结构化、易读的形式输出。
  - **Backend**: 重构配置管理，将配置文件格式从 `settings.json` 迁移至 `config.toml`，并实现自动迁移逻辑。
  - **Verification**: 完成后端 Agent 逻辑的 POC 验证，成功生成 Go 语言测试代码。
