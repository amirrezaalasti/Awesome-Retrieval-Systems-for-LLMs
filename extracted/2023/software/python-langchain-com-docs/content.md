### Get started

- [Install](/oss/python/langchain/install)
- [Quickstart](/oss/python/langchain/quickstart)
- [Changelog](https://docs.langchain.com/oss/python/releases/changelog)
- [Philosophy](/oss/python/langchain/philosophy)

### Core components

- [Agents](/oss/python/langchain/agents)
- [Models](/oss/python/langchain/models)
- [Messages](/oss/python/langchain/messages)
- [Tools](/oss/python/langchain/tools)
- [Short-term memory](/oss/python/langchain/short-term-memory)
- [Event streaming](/oss/python/langchain/event-streaming)
- [Streaming](/oss/python/langchain/streaming)
- [Structured output](/oss/python/langchain/structured-output)

### Middleware

- [Overview](/oss/python/langchain/middleware/overview)
- [Prebuilt middleware](/oss/python/langchain/middleware/built-in)
- [Custom middleware](/oss/python/langchain/middleware/custom)

### Frontend

- [Overview](/oss/python/langchain/frontend/overview)
- Patterns
- Integrations

### Advanced usage

- [Guardrails](/oss/python/langchain/guardrails)
- [Runtime](/oss/python/langchain/runtime)
- [Context engineering](/oss/python/langchain/context-engineering)
- [Model Context Protocol (MCP)](/oss/python/langchain/mcp)
- [Human-in-the-loop](/oss/python/langchain/human-in-the-loop)
- Multi-agent
- [Retrieval](/oss/python/langchain/retrieval)
- [Long-term memory](/oss/python/langchain/long-term-memory)

### Agent development

- [LangSmith Studio](/oss/python/langchain/studio)
- Test
- [Agent Chat UI](/oss/python/langchain/ui)

### Production

- [Deployment](/oss/python/langchain/deploy)
- [Observability](/oss/python/langchain/observability)

## On this page

- [Create an agent](#create-an-agent)
- [Core benefits](#core-benefits)

# LangChain overview

Copy page

LangChain provides create\_agent: a minimal, highly configurable agent harness. Compose exactly the agent your use case needs from model, tools, prompt, and middleware.

Copy page

**Agent = Model + Harness.** LangChain provides `create_agent` : a minimal, highly configurable harness. The harness is everything around the model loop: the prompt, the tools, and any middleware that shapes behavior. Start with the primitives and compose exactly what your use case needs. Supports [OpenAI, Anthropic, Google, and more](/oss/python/integrations/providers/overview) .

**LangChain vs. LangGraph vs. Deep Agents** Start with [Deep Agents](/oss/python/deepagents/overview) for a "batteries-included" agent with features like automatic context compression, a virtual filesystem, and subagent-spawning. Deep Agents are built on LangChain [agents](/oss/python/langchain/agents) which you can also use directly. Use [LangChain](/oss/python/langchain/agents) ( `create_agent` ) for a highly customizable harness, easily tailored to your use case and data. Use [LangGraph](/oss/python/langgraph/overview) , our low-level orchestration framework, for advanced needs combining deterministic and agentic workflows. Use [LangSmith](/langsmith/observability) to trace, debug, and evaluate agents built with any of these frameworks. Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up. We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## [ Create an agent](#create-an-agent)

This example demonstrates how to create a simple LangChain agent with a custom tool:

OpenAI

Google Gemini

Claude (Anthropic)

OpenRouter

Fireworks

Baseten

Ollama

Azure

AWS Bedrock

HuggingFace

```
# pip install -qU langchain "langchain[openai]"
from langchain . agents import create_agent

def get_weather ( city : str ) -> str :
"""Get weather for a given city."""
return f "It's always sunny in { city } !"

agent = create_agent (
model = "openai:gpt-5.5" ,
tools = [ get_weather ],
system_prompt = "You are a helpful assistant" ,
)

result = agent . invoke (
{ "messages" : [{ "role" : "user" , "content" : "What's the weather in San Francisco?" }]}
)
print ( result [ " messages " ][ - 1 ]. content_blocks )
```

See the [Installation instructions](/oss/python/langchain/install) and [Quickstart guide](/oss/python/langchain/quickstart) to get started building your own agents and applications with LangChain.

Use [LangSmith](/langsmith/observability) to trace requests, debug agent behavior, and evaluate outputs. Set `LANGSMITH_TRACING=true` and your API key to get started.

## [ Core benefits](#core-benefits)

## Standard model interface

Use one interface for chat models, embeddings, and more across providers. Switch models with minimal code changes and keep your application portable as requirements evolve.

Learn more

## Highly configurable harness

Start with `create_agent` as a minimal harness and add capabilities incrementally through middleware. Compose only what your use case needs, from guardrails and retries to routing and custom tool policies.

Learn more

https://mintcdn.com/langchain-5e9cc07a/nQm-sjd\_MByLhgeW/images/brand/langgraph-icon.png?fit=max&amp;auto=format&amp;n=nQm-sjd\_MByLhgeW&amp;q=85&amp;s=b997e1a7487d507a36556eedbfd99f81

<!-- image -->

## Built on top of LangGraph

LangChain's agents are built on top of LangGraph. This allows us to take advantage of LangGraph's durable execution, human-in-the-loop support, persistence, and more.

Learn more

https://mintcdn.com/langchain-5e9cc07a/nQm-sjd\_MByLhgeW/images/brand/observability-icon-dark.png?fit=max&amp;auto=format&amp;n=nQm-sjd\_MByLhgeW&amp;q=85&amp;s=ccbc183bca2a5e4ca78d30149e3836cc

<!-- image -->

## Debug with LangSmith

Inspect traces, tool calls, state transitions, and latency in one place. Find failure modes, evaluate quality, and improve agent behavior with execution data.

Learn more

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose) .

Was this page helpful?

Yes

No

[Install LangChain Next](/oss/python/langchain/install)