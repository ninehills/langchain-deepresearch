# Repository Guidelines

## Project Structure & Module Organization
This repo bundles three LangGraph research agents plus a reusable UI. `research_agent_v1`, `research_agent_v2`, and `research_agent_v3` each contain an `env.example`, `langgraph.json`, prompts, and a Python entry point; keep new tools beside `tools.py` or under `prompts/`. `deepagents/libs/deepagents` holds the vendored LangChain DeepAgents library installed in editable mode, while `deep-agents-ui/src` stores the Next.js dashboard (shared config in `tailwind.config.js`, assets in `public/`).

## Build, Test, and Development Commands
Run `git submodule update --init --recursive` after cloning to sync DeepAgents. Create a backend environment with `uv venv --python 3.12 && source .venv/bin/activate`, then install dependencies via `uv pip install -r research_agent_v3/requirements.txt` (swap the folder as needed). Start a graph locally with `uv run langgraph dev --config research_agent_v3/langgraph.json --watch` to hot-reload tools. The UI requires Node 18+: `cd deep-agents-ui && npm install`, `npm run dev` for local work, `npm run build` before releases, and `npm run lint` before pushing.

## Coding Style & Naming Conventions
Python files use 4-space indentation, snake_case module names (`research_agent.py`, `tools.py`), and typed LangChain callbacks; surface prompts as markdown named for the scenario (e.g., `prompts/report-outline.md`). The UI enforces ESLint/Prettier via `eslint.config.js` and `prettier.config.cjs`, so rely on `npm run lint` and `npm run format:check` instead of manual styling. React components stay PascalCase, hooks camelCase, and shared Tailwind tokens belong inside `tailwind.config.js`.

## Testing Guidelines
Backends currently lack automated tests, so add pytest suites under `research_agent_v*/tests/` when touching reasoning or tool wiring and run them with `uv run pytest`. Before opening a PR, run `uv run langgraph dev` end-to-end with a realistic `.env` and capture any agent transcript in `reports/` for reproducibility. The UI must pass `npm run lint`; when adding complex interactions, consider React Testing Library co-located under `src/__tests__`.

## Commit & Pull Request Guidelines
History uses concise, imperative subjects (`add research_agent_v2`), so continue that format and keep each commit narrowly scoped. Pull requests must state the scenario, reference issues or reports, and list the commands executed (backend setup, UI builds, tests). Include screenshots or terminal snippets for UI or agent behavior changes, and confirm `.env` files stay ignored.

## Security & Configuration Tips
Duplicate `env.example` to `.env` inside each agent folder and provide provider keys (OpenAI, Gemini, Tavily) locally only. Document any new secret or callback URL in both the relevant `env.example` and README, and scrub reports before sharing to ensure logs never reveal tokens or proprietary data.
