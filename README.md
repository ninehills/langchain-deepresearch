# langchain-deepresearch

Langchain deep research demo with UI.

```bash
# Update submodules
git submodule update --init --recursive
```

Test Prompt:

> 针对 GraphRAG 主题，找到2025年的全部最新学术论文、开源项目，深入读取论文内容，整理出完整综述。搜索关键词使用英文，但是最终的报告为中文。

Reports:

1. [Gemini DeepResearch with Gemini 2.5 Pro @ 20251117](reports/gemini_deepresearch.docx)
2. [OpenAI DeepResearch with GPT-5.1 thinking @ 20251117](reports/openai_deepresearch.docx)
3. [Research Agent v1 with GLM-4.6 @ 20251117](reports/research_agent_v1_glm46.md)
4. [Research Agent v2 with GLM-4.6 @ 20251117](reports/research_agent_v2_glm46.md)

## research_agent_v1

From: https://github.com/langchain-ai/deepagents/tree/master/examples/research

Start backend server:

```bash
uv venv --python 3.12
source .venv/bin/activate
cd research_agent_v1
uv pip install -r requirements.txt

# set env
cp env.example .env
# edit .env to add your own keys

# start langgraph dev server
uv run langgraph dev
```

Start the frontend server:

```bash
cd deep-agents-ui/
npm install

# run frontend server
npm run dev
```

Visit http://localhost:3000 to see the frontend.

1. DEPLOYMENT_URL="http://127.0.0.1:2024"
2. AGENT_ID="research"

## research_agent_v2

From: https://github.com/anthropics/claude-agent-sdk-demos/tree/main/research-agent

Start backend server:

```bash
source .venv/bin/activate
cd research_agent_v2
uv pip install -r requirements.txt

# set env
cp env.example .env
# edit .env to add your own keys

# start langgraph dev server
uv run langgraph dev
```

Start the frontend server:

```bash
cd deep-agents-ui/
npm install

# run frontend server
npm run dev
```

Visit http://localhost:3000 to see the frontend.

1. DEPLOYMENT_URL="http://127.0.0.1:2024"
2. AGENT_ID="research_v2"
