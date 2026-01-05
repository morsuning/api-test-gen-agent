# Backend - API Test Gen Agent

## 简介
API Test Gen Agent 的后端服务，基于 Python 和 FastAPI 构建，负责核心的测试生成逻辑和 Agent 编排。

## 环境要求
- **Python**: >= 3.13
- **uv**: 这是一个极速的 Python 包管理和项目管理工具，用于管理本项目依赖。

## 快速开始

### 1. 安装依赖
在 `backend` 目录下执行：
```bash
uv sync
```
此命令会根据 `pyproject.toml` 和 `uv.lock` 安装所有必要的运行时依赖。

### 2. 启动服务
使用 `uv run` 启动 uvicorn 开发服务器：
```bash
uv run uvicorn app.main:app --reload
```
服务启动后，默认访问地址为：`http://127.0.0.1:8000`

### 3. API 文档
启动服务后，可以在浏览器中访问交互式 API 文档：
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 项目结构
- `app/`: 应用源码
  - `agent/`: Agent 编排逻辑 (LangGraph)
  - `api/`: API 路由定义
  - `core/`: 核心配置和工具
- `pyproject.toml`: 项目配置和依赖定义
