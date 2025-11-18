# langchain-deepresearch

一个多智能体的 LangChain 实验项目，复刻多种深度调研工作流，并配套 UI。

## 仓库结构

- `deep-agents-ui/` – 基于 Next.js 15 的UI，用于监控和操控智能体。
- `deepagents/` – 引入的 LangChain DeepAgents 库（子模块）。
- `research_agent_v1/` – 来自 LangChain deep research 示例的基线流程。
- `research_agent_v2/` – 受 Claude Agent SDK 启发的流程。
- `research_agent_v3/` – 重新设计的流水线，增加分阶段子代理、外部工具以及确定性的文件传递。
- `reports/` – 不同配置生成的示例输出。

后续改进思路： 
1. 对WebFetch 增加 AI Summary，避免长上下文引入带来的问题。
2. 长文写作的前后一致性以及写作风格，需要进行优化。
3. 深度研究的部分过于简单，应该拆分为进一步的子 Agent 来进行深度搜索和调研。
4. 研究大纲目前为静态，应该根据研究结果动态更新研究大纲。

## 先决条件

- Python 3.12，并使用 [uv](https://github.com/astral-sh/uv) 管理依赖。
- Node.js 18+（或 Bun）运行前端。
- API Key：兼容 Anthropic 的模型端点、Tavily 搜索，以及你额外接入的工具。

克隆仓库并拉取子模块：

```bash
git clone <repo>
cd langchain-deepresearch
git submodule update --init --recursive
```

## 运行 Research Agent v1

```bash
uv venv --python 3.12
source .venv/bin/activate
cd research_agent_v1/
uv pip install -r requirements.txt
cp env.example .env  # 填入密钥
uv run langgraph dev --config langgraph.json
```

该智能体会生成 todo 计划、调用专职研究与评审子代理，并在本地输出最终 Markdown 报告。

## 运行 Research Agent v2

基于 Anthropics 的 Claude Agent SDK 示例构建，结构类似 v1，但为总控、研究员、写手分别提供独立提示词。

```bash
source .venv/bin/activate  # 复用虚拟环境
cd research_agent_v2/
uv pip install -r requirements.txt
cp env.example .env  # 填入密钥
uv run langgraph dev --config langgraph.json
```

前端中将 `AGENT_ID` 设置为 `research_v2` 指向该后端。

## 运行 Research Agent v3

第三版围绕“初步侦察、计划、深度搜索、写大纲、逐段撰写、合并成稿”等阶段重构，并依赖 `research_assets/` 下的结构化文件。工具位于 `research_agent_v3/tools.py`，包含 `WebSearch`、`WebFetch`、`GetCurrentDate`。

```bash
source .venv/bin/activate
cd research_agent_v3/
uv pip install -r requirements.txt
cp env.example .env
uv run langgraph dev --config langgraph.json
```

## 前端（deep-agents-ui）

```bash
cd deep-agents-ui
npm install  # 或 yarn install / bun install
npm run dev  # http://localhost:3000
```

通过环境变量配置仪表盘：

1. `DEPLOYMENT_URL="http://127.0.0.1:2024"`
2. `AGENT_ID` 可设为 `research`、`research_v2` 或 `research_v3`

在提交前执行 `npm run build` 与 `npm run lint`。

## 示例提示词与报告

提示词：针对 GraphRAG 主题，找到2025年的全部最新学术论文、开源项目，深入读取论文内容，整理出完整综述。搜索关键词使用英文，但是最终的报告为中文。

实验过程中生成的报告保存在 `reports/`：

1. `gemini_deepresearch.docx` – Gemini 2.5 Pro 运行（2025-11-17）
2. `openai_deepresearch.docx` – OpenAI GPT-5.1 Thinking 运行（2025-11-17）
3. `research_agent_v1_glm46.md` – LangChain DeepAgents 基线结果
4. `research_agent_v2_glm46.txt` – Claude SDK Demo 流程，表现最弱
5. `research_agent_v3_glm46.md` – 完整流水线结合外部工具，质量明显提升

## 故障排查提示

- Tavily 搜索失败时，确认运行 `uv run` 的环境中已设置 `TAVILY_API_KEY`。
- 请勿将 `.env` 与 API Key 提交到仓库，仅提交 `env.example` 模板。
