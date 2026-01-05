# Frontend - API Test Gen Agent

## 简介
API Test Gen Agent 的前端界面，基于 React、TypeScript 和 Vite 构建，使用 Bun 作为包管理器。

## 环境要求
- **Bun**: >= 1.0.0 (推荐最新版)
- **Node.js**: 虽然主要使用 Bun，但某些工具链可能仍依赖 Node 环境。

## 快速开始

### 1. 安装依赖
在 `frontend` 目录下执行：
```bash
bun install
```
此命令会根据 `package.json` 和 `bun.lock` 安装所有前端依赖。

### 2. 启动开发服务器
启动开发环境：
```bash
bun run dev
```
默认访问地址为：`http://localhost:5173`

### 3. 构建生产版本
构建用于生产环境的静态文件：
```bash
bun run build
```
构建产物将位于 `dist` 目录。

## 项目结构
- `src/`: 源代码
- `vite.config.ts`: Vite 配置文件
- `tailwind.config.js`: Tailwind CSS 配置
- `bun.lock`: Bun 的依赖锁定文件

---
# React + TypeScript + Vite (原生模板说明)

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh
