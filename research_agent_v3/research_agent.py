import os
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    InterruptOnConfig,
    TodoListMiddleware,
)
from langchain.agents.middleware.summarization import SummarizationMiddleware
from langchain.agents.middleware.types import AgentMiddleware
from langchain.agents.structured_output import ResponseFormat
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import AnthropicPromptCachingMiddleware
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.cache.base import BaseCache
from langgraph.graph.state import CompiledStateGraph
from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer

from deepagents.backends.protocol import BackendFactory, BackendProtocol
from deepagents.middleware.filesystem import FilesystemMiddleware
from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.subagents import (
    CompiledSubAgent,
    SubAgent,
    SubAgentMiddleware,
)

from tools import WebSearch, WebFetch, GetCurrentDate

load_dotenv()


def get_default_model() -> ChatAnthropic:
    """返回默认的对话模型。"""

    return ChatAnthropic(
        model_name=os.environ["ANTHROPIC_DEFAULT_SONNET_MODEL"],
        max_tokens=20000,
    )


BASE_AGENT_PROMPT = "为了完成研究目标，你可以调度子代理、使用可用工具并通过文件系统同步信息。"


def create_deep_agent(
    model: str | BaseChatModel | None = None,
    tools: Sequence[BaseTool | Callable | dict[str, Any]] | None = None,
    *,
    system_prompt: str | None = None,
    middleware: Sequence[AgentMiddleware] = (),
    subagents: list[SubAgent | CompiledSubAgent] | None = None,
    response_format: ResponseFormat | None = None,
    context_schema: type[Any] | None = None,
    checkpointer: Checkpointer | None = None,
    store: BaseStore | None = None,
    backend: BackendProtocol | BackendFactory | None = None,
    interrupt_on: dict[str, bool | InterruptOnConfig] | None = None,
    debug: bool = False,
    name: str | None = None,
    cache: BaseCache | None = None,
) -> CompiledStateGraph:
    """构建 Deep Agent 并注入子代理。"""

    if model is None:
        model = get_default_model()

    deepagent_middleware = [
        TodoListMiddleware(),
        FilesystemMiddleware(backend=backend),
        SubAgentMiddleware(
            default_model=model,
            default_tools=tools,
            subagents=subagents if subagents is not None else [],
            default_middleware=[
                TodoListMiddleware(),
                FilesystemMiddleware(backend=backend),
                SummarizationMiddleware(
                    model=model,
                    max_tokens_before_summary=170000,
                    messages_to_keep=6,
                ),
                AnthropicPromptCachingMiddleware(unsupported_model_behavior="ignore"),
                PatchToolCallsMiddleware(),
            ],
            default_interrupt_on=interrupt_on,
            general_purpose_agent=True,
        ),
        SummarizationMiddleware(
            model=model,
            max_tokens_before_summary=170000,
            messages_to_keep=6,
        ),
        AnthropicPromptCachingMiddleware(unsupported_model_behavior="ignore"),
        PatchToolCallsMiddleware(),
    ]
    if middleware:
        deepagent_middleware.extend(middleware)
    if interrupt_on is not None:
        deepagent_middleware.append(HumanInTheLoopMiddleware(interrupt_on=interrupt_on))

    prompt = (
        f"{system_prompt}\n\n{BASE_AGENT_PROMPT}" if system_prompt else BASE_AGENT_PROMPT
    )

    return (
        create_agent(
            model,
            system_prompt=prompt,
            tools=tools,
            middleware=deepagent_middleware,
            response_format=response_format,
            context_schema=context_schema,
            checkpointer=checkpointer,
            store=store,
            debug=debug,
            name=name,
            cache=cache,
        )
        .with_config({"recursion_limit": 1000})
    )


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


initial_scout_sub_agent = {
    "name": "initial-scout",
    "description": "执行初步搜索并生成情报摘要，输出到 research_assets/01_initial_search/overview.md。",
    "system_prompt": load_prompt("initial_search_agent.md"),
    "tools": [WebSearch, GetCurrentDate],
}

plan_strategist_sub_agent = {
    "name": "plan-strategist",
    "description": "根据简报和初搜结果制定研究计划，输出 research_assets/02_plan/research_plan.md。",
    "system_prompt": load_prompt("plan_agent.md"),
    "tools": [],
}

deep_researcher_sub_agent = {
    "name": "deep-researcher",
    "description": "执行深度检索并整理证据，维护 research_assets/03_deep_search/。",
    "system_prompt": load_prompt("deep_research_agent.md"),
    "tools": [WebSearch, WebFetch, GetCurrentDate],
}

outline_architect_sub_agent = {
    "name": "outline-architect",
    "description": "根据证据写出报告大纲，输出 research_assets/04_outline/outline.md。",
    "system_prompt": load_prompt("outline_agent.md"),
    "tools": [],
}

section_writer_sub_agent = {
    "name": "section-writer",
    "description": "逐段撰写报告内容，生成 research_assets/05_sections/*.md。",
    "system_prompt": load_prompt("section_writer_agent.md"),
    "tools": [],
}

report_merger_sub_agent = {
    "name": "report-merger",
    "description": "整合段落并输出 final_report.md 与 sources.md。",
    "system_prompt": load_prompt("report_merger_agent.md"),
    "tools": [],
}


agent = create_deep_agent(
    model=get_default_model(),
    tools=[WebSearch, WebFetch, GetCurrentDate],
    system_prompt=load_prompt("lead_agent.md"),
    subagents=[
        initial_scout_sub_agent,
        plan_strategist_sub_agent,
        deep_researcher_sub_agent,
        outline_architect_sub_agent,
        section_writer_sub_agent,
        report_merger_sub_agent,
    ],
)
