DeepEval.

<!-- image -->

# The LLM Evaluation Framework

confident-ai%2Fdeepeval | Trendshift

<!-- image -->

discord-invite

<!-- image -->

reddit-community

<!-- image -->

#### [Documentation | Metrics and Features | Getting Started | Integrations | Confident AI](https://deepeval.com/docs/getting-started?utm_source=GitHub)

GitHub release

<!-- image -->

Try Quickstart in Colab

<!-- image -->

License

<!-- image -->

Twitter Follow

<!-- image -->

[Deutsch](https://www.readme-i18n.com/confident-ai/deepeval?lang=de) | [Español](https://www.readme-i18n.com/confident-ai/deepeval?lang=es) | [français](https://www.readme-i18n.com/confident-ai/deepeval?lang=fr) | [日本語](https://www.readme-i18n.com/confident-ai/deepeval?lang=ja) | [한국어](https://www.readme-i18n.com/confident-ai/deepeval?lang=ko) | [Português](https://www.readme-i18n.com/confident-ai/deepeval?lang=pt) | [Русский](https://www.readme-i18n.com/confident-ai/deepeval?lang=ru) | [中文](https://www.readme-i18n.com/confident-ai/deepeval?lang=zh)

**DeepEval** is a simple-to-use, open-source LLM evaluation framework, for evaluating large-language model systems. It is similar to Pytest but specialized for unit testing LLM apps. DeepEval incorporates the latest research to run evals via metrics such as G-Eval, task completion, answer relevancy, hallucination, etc., which uses LLM-as-a-judge and other NLP models that run **locally on your machine** .

Whether you're building AI agents, RAG pipelines, or chatbots, implemented via LangChain or OpenAI, DeepEval has you covered. With it, you can easily determine the optimal models, prompts, and architecture to improve your AI quality, prevent prompt drifting, or even transition from OpenAI to Claude with confidence.

[!IMPORTANT] Need a place for your DeepEval testing data to live 🏡❤️? [Sign up to Confident AI](https://www.confident-ai.com/?utm_source=deepeval&utm_medium=github&utm_content=signup_callout) to compare iterations of your LLM app, generate &amp; share testing reports, and more.

Demo GIF

Want to talk LLM evaluation, need help picking metrics, or just to say hi? [Come join our discord.](https://discord.com/invite/3SEyvpgu2f)

# 🔥 Metrics and Features

- 📐 Large variety of ready-to-use LLM eval metrics (all with explanations) powered by **ANY** LLM of your choice, statistical methods, or NLP models that run **locally on your machine** covering all use cases:
    - **Custom, All-Purpose Metrics:**
        - [G-Eval](https://deepeval.com/docs/metrics-llm-evals) - a research-backed LLM-as-a-judge metric for evaluating on any custom criteria with human-like accuracy
        - [DAG](https://deepeval.com/docs/metrics-dag) - DeepEval's graph-based deterministic LLM-as-a-judge metric builder
        - [Task Completion](https://deepeval.com/docs/metrics-task-completion) - evaluate whether an agent accomplished its goal
        - [Tool Correctness](https://deepeval.com/docs/metrics-tool-correctness) - check if the right tools were called with the right arguments
        - [Goal Accuracy](https://deepeval.com/docs/metrics-goal-accuracy) - measure how accurately the agent achieved the intended goal
        - [Step Efficiency](https://deepeval.com/docs/metrics-step-efficiency) - evaluate whether the agent took unnecessary steps
        - [Plan Adherence](https://deepeval.com/docs/metrics-plan-adherence) - check if the agent followed the expected plan
        - [Plan Quality](https://deepeval.com/docs/metrics-plan-quality) - evaluate the quality of the agent's plan
        - [Tool Use](https://deepeval.com/docs/metrics-tool-use) - measure quality of tool usage
        - [Argument Correctness](https://deepeval.com/docs/metrics-argument-correctness) - validate tool call arguments
        - [Answer Relevancy](https://deepeval.com/docs/metrics-answer-relevancy) - measure how relevant the RAG pipeline's output is to the input
        - [Faithfulness](https://deepeval.com/docs/metrics-faithfulness) - evaluate whether the RAG pipeline's output factually aligns with the retrieval context
        - [Contextual Recall](https://deepeval.com/docs/metrics-contextual-recall) - measure how well the RAG pipeline's retrieval context aligns with the expected output
        - [Contextual Precision](https://deepeval.com/docs/metrics-contextual-precision) - evaluate whether relevant nodes in the RAG pipeline's retrieval context are ranked higher
        - [Contextual Relevancy](https://deepeval.com/docs/metrics-contextual-relevancy) - measure the overall relevance of the RAG pipeline's retrieval context to the input
        - [RAGAS](https://deepeval.com/docs/metrics-ragas) - average of answer relevancy, faithfulness, contextual precision, and contextual recall
        - [Knowledge Retention](https://deepeval.com/docs/metrics-knowledge-retention) - evaluate whether the chatbot retains factual information throughout a conversation
        - [Conversation Completeness](https://deepeval.com/docs/metrics-conversation-completeness) - measure whether the chatbot satisfies user needs throughout a conversation
        - [Turn Relevancy](https://deepeval.com/docs/metrics-turn-relevancy) - evaluate whether the chatbot generates consistently relevant responses throughout a conversation
        - [Turn Faithfulness](https://deepeval.com/docs/metrics-turn-faithfulness) - check if the chatbot's responses are factually grounded in retrieval context across turns
        - [Role Adherence](https://deepeval.com/docs/metrics-role-adherence) - evaluate whether the chatbot adheres to its assigned role throughout a conversation
        - [MCP Task Completion](https://deepeval.com/docs/metrics-mcp-task-completion) - evaluate how effectively an MCP-based agent accomplishes a task
        - [MCP Use](https://deepeval.com/docs/metrics-mcp-use) - measure how effectively an agent uses its available MCP servers
        - [Multi-Turn MCP Use](https://deepeval.com/docs/metrics-multi-turn-mcp-use) - evaluate MCP server usage across conversation turns
        - [Text to Image](https://deepeval.com/docs/multimodal-metrics-text-to-image) - evaluate image generation quality based on semantic consistency and perceptual quality
        - [Image Editing](https://deepeval.com/docs/multimodal-metrics-image-editing) - evaluate image editing quality based on semantic consistency and perceptual quality
        - [Image Coherence](https://deepeval.com/docs/multimodal-metrics-image-coherence) - measure how well images align with their accompanying text
        - [Image Helpfulness](https://deepeval.com/docs/multimodal-metrics-image-helpfulness) - evaluate how effectively images contribute to user comprehension of the text
        - [Image Reference](https://deepeval.com/docs/multimodal-metrics-image-reference) - evaluate how accurately images are referred to or explained by accompanying text
        - [Hallucination](https://deepeval.com/docs/metrics-hallucination) - check whether the LLM generates factually correct information against provided context
        - [Summarization](https://deepeval.com/docs/metrics-summarization) - evaluate whether summaries are factually correct and include necessary details
        - [Bias](https://deepeval.com/docs/metrics-bias) - detect gender, racial, or political bias in LLM outputs
        - [Toxicity](https://deepeval.com/docs/metrics-toxicity) - evaluate toxicity in LLM outputs
        - [JSON Correctness](https://deepeval.com/docs/metrics-json-correctness) - check whether the output matches an expected JSON schema
        - [Prompt Alignment](https://deepeval.com/docs/metrics-prompt-alignment) - measure whether the output aligns with instructions in the prompt template
- 🎯 Supports both end-to-end and component-level LLM evaluation.
- 🧩 Build your own custom metrics that are automatically integrated with DeepEval's ecosystem.
- 🔮 Generate both single and multi-turn synthetic datasets for evaluation.
- 🔗 Integrates seamlessly with **ANY** CI/CD environment.
- 🧬 Optimize prompts automatically based on evaluation results.
- 🏆 Easily benchmark **ANY** LLM on popular LLM benchmarks in [under 10 lines of code.](https://deepeval.com/docs/benchmarks-introduction?utm_source=GitHub) , including MMLU, HellaSwag, DROP, BIG-Bench Hard, TruthfulQA, HumanEval, GSM8K.

# 🔌 Integrations

DeepEval plugs into any LLM framework - OpenAI Agents, LangChain, CrewAI, and more. To scale evals across your team - or let anyone run them without writing code - **Confident AI** gives you a native platform integration.

## Frameworks

- [OpenAI](https://www.deepeval.com/integrations/frameworks/openai?utm_source=GitHub) - evaluate and trace OpenAI applications via a client wrapper
- [OpenAI Agents](https://www.deepeval.com/integrations/frameworks/openai-agents?utm_source=GitHub) - evaluate OpenAI Agents end-to-end in under a minute
- [LangChain](https://www.deepeval.com/integrations/frameworks/langchain?utm_source=GitHub) - evaluate LangChain applications with a callback handler
- [LangGraph](https://www.deepeval.com/integrations/frameworks/langgraph?utm_source=GitHub) - evaluate LangGraph agents with a callback handler
- [Pydantic AI](https://www.deepeval.com/integrations/frameworks/pydanticai?utm_source=GitHub) - evaluate Pydantic AI agents with type-safe validation
- [CrewAI](https://www.deepeval.com/integrations/frameworks/crewai?utm_source=GitHub) - evaluate CrewAI multi-agent systems
- [Anthropic](https://www.deepeval.com/integrations/frameworks/anthropic?utm_source=GitHub) - evaluate and trace Claude applications via a client wrapper
- [AWS AgentCore](https://www.deepeval.com/integrations/frameworks/agentcore?utm_source=GitHub) - evaluate agents deployed on Amazon AgentCore
- [LlamaIndex](https://www.deepeval.com/integrations/frameworks/llamaindex?utm_source=GitHub) - evaluate RAG applications built with LlamaIndex

## ☁️ Platform + Ecosystem

[Confident AI](https://www.confident-ai.com/?utm_source=deepeval&utm_medium=github&utm_content=platform_section) is an all-in-one platform that integrates natively with DeepEval.

- Manage datasets, trace LLM applications, run evaluations, and monitor responses in production - all from one platform.
- Don't need a UI? Confident AI can also be your data persistent layer - run evals, pull datasets, and inspect traces straight from claude code, cursor, via Confident AI's [MCP server](https://github.com/confident-ai/confident-mcp-server) .

Confident AI MCP Architecture

<!-- image -->

# 🤖 Vibe-Coder QuickStart

Want your coding agent to add evals and fix failures for you? Install the DeepEval skill, point it at your agent, RAG pipeline, or chatbot, and ask it to generate a dataset, write the eval suite, run `deepeval test run` , and iterate on the failing metrics. [Start with the 5-minute vibe-coder guide](https://deepeval.com/docs/vibe-coder-quickstart?utm_source=GitHub) .

# 🚀 Human QuickStart

Let's pretend your LLM application is a RAG based customer support chatbot; here's how DeepEval can help test what you've built.

## Installation

Deepeval works with **Python&gt;=3.9+** .

```
pip install -U deepeval
```

## Create an account (highly recommended)

Using the `deepeval` platform will allow you to generate sharable testing reports on the cloud. It is free, takes no additional code to setup, and we highly recommend giving it a try.

To login, run:

```
deepeval login
```

Follow the instructions in the CLI to create an account, copy your API key, and paste it into the CLI. All test cases will automatically be logged (find more information on data privacy [here](https://deepeval.com/docs/data-privacy?utm_source=GitHub) ).

## Write your first test case

Create a test file:

```
touch test_chatbot.py
```

Open `test_chatbot.py` and write your first test case to run an **end-to-end** evaluation using DeepEval, which treats your LLM app as a black-box:

```
import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

def test_case():
    correctness_metric = GEval(
        name="Correctness",
        criteria="Determine if the 'actual output' is correct based on the 'expected output'.",
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        threshold=0.5
    )
    test_case = LLMTestCase(
        input="What if these shoes don't fit?",
        # Replace this with the actual output from your LLM application
        actual_output="You have 30 days to get a full refund at no extra cost.",
        expected_output="We offer a 30-day full refund at no extra costs.",
        retrieval_context=["All customers are eligible for a 30 day full refund at no extra costs."]
    )
    assert_test(test_case, [correctness_metric])
```

Set your `OPENAI_API_KEY` as an environment variable (you can also evaluate using your own custom model, for more details visit [this part of our docs](https://deepeval.com/docs/metrics-introduction#using-a-custom-llm?utm_source=GitHub) ):

```
export OPENAI_API_KEY="..."
```

And finally, run `test_chatbot.py` in the CLI:

```
deepeval test run test_chatbot.py
```

**Congratulations! Your test case should have passed ✅** Let's break down what happened.

- The variable `input` mimics a user input, and `actual_output` is a placeholder for what your application's supposed to output based on this input.
- The variable `expected_output` represents the ideal answer for a given `input` , and [`GEval`](https://deepeval.com/docs/metrics-llm-evals) is a research-backed metric provided by `deepeval` for you to evaluate your LLM outputs on any custom with human-like accuracy.
- In this example, the metric `criteria` is correctness of the `actual_output` based on the provided `expected_output` .
- All metric scores range from 0 - 1, which the `threshold=0.5` threshold ultimately determines if your test has passed or not.

[Read our documentation](https://deepeval.com/docs/getting-started?utm_source=GitHub) for more information!

## Evals With Full Traceability

Use `evals_iterator()` to run the same dataset through your app, whether you instrument it manually or through one of DeepEval's framework integrations.

Here's an example of manual instrumentation:

```
from deepeval.tracing import observe, update_current_span
from deepeval.test_case import LLMTestCase
from deepeval.metrics import TaskCompletionMetric

@observe()
def inner_component(input: str):
    output = "result"
    update_current_span(test_case=LLMTestCase(input=input, actual_output=output))
    return output

@observe()
def app(input: str):
    return inner_component(input)

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(metrics=[TaskCompletionMetric()]):
    app(golden.input)
```

**OpenAI**

```
from deepeval.openai import OpenAI
from deepeval.tracing import trace
from deepeval.metrics import TaskCompletionMetric

client = OpenAI()

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator():
    with trace(metrics=[TaskCompletionMetric()]):
        client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": golden.input}],
        )
```

**OpenAI Agents**

```
from agents import Runner
from deepeval.metrics import TaskCompletionMetric

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(metrics=[TaskCompletionMetric()]):
    Runner.run_sync(agent, golden.input)
```

**Anthropic**

```
from deepeval.anthropic import Anthropic
from deepeval.tracing import trace
from deepeval.metrics import TaskCompletionMetric

client = Anthropic()

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator():
    with trace(metrics=[TaskCompletionMetric()]):
        client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": golden.input}],
        )
```

**LangChain**

```
from deepeval.integrations.langchain import CallbackHandler
from deepeval.metrics import TaskCompletionMetric

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator():
    llm.invoke(
        golden.input,
        config={"callbacks": [CallbackHandler(metrics=[TaskCompletionMetric()])]},
    )
```

**LangGraph**

```
from deepeval.integrations.langchain import CallbackHandler
from deepeval.metrics import TaskCompletionMetric

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator():
    agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={"callbacks": [CallbackHandler(metrics=[TaskCompletionMetric()])]},
    )
```

**Pydantic AI**

```
from deepeval.metrics import TaskCompletionMetric

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(metrics=[TaskCompletionMetric()]):
    agent.run_sync(golden.input)
```

**CrewAI**

```
from deepeval.integrations.crewai import instrument_crewai
from deepeval.metrics import TaskCompletionMetric

instrument_crewai()

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(metrics=[TaskCompletionMetric()]):
    crew.kickoff({"input": golden.input})
```

**AWS AgentCore**

```
from deepeval.integrations.agentcore import instrument_agentcore
from deepeval.metrics import TaskCompletionMetric

instrument_agentcore()

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(metrics=[TaskCompletionMetric()]):
    invoke({"prompt": golden.input})
```

**LlamaIndex**

```
import asyncio
from deepeval.evaluate.configs import AsyncConfig
from deepeval.metrics import TaskCompletionMetric

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(
    async_config=AsyncConfig(run_async=True),
    metrics=[TaskCompletionMetric()],
):
    task = asyncio.create_task(agent.run(golden.input))
    dataset.evaluate(task)
```

**Google ADK**

```
import asyncio
from deepeval.evaluate.configs import AsyncConfig
from deepeval.integrations.google_adk import instrument_google_adk
from deepeval.metrics import TaskCompletionMetric

instrument_google_adk()

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(
    async_config=AsyncConfig(run_async=True),
    metrics=[TaskCompletionMetric()],
):
    task = asyncio.create_task(run_agent(golden.input))
    dataset.evaluate(task)
```

**Strands**

```
from deepeval.integrations.strands import instrument_strands
from deepeval.metrics import TaskCompletionMetric

instrument_strands()

# This metric will be run on your trace end to end.
for golden in dataset.evals_iterator(metrics=[TaskCompletionMetric()]):
    agent(golden.input)
```

Learn more about component-level evaluations [here.](https://www.deepeval.com/docs/evaluation-component-level-llm-evals)

## Evaluate Without Pytest Integration

Alternatively, you can evaluate without Pytest, which is more suited for a notebook environment.

```
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    # Replace this with the actual output from your LLM application
    actual_output="We offer a 30-day full refund at no extra costs.",
    retrieval_context=["All customers are eligible for a 30 day full refund at no extra costs."]
)
evaluate([test_case], [answer_relevancy_metric])
```

## Using Standalone Metrics

DeepEval is extremely modular, making it easy for anyone to use any of our metrics. Continuing from the previous example:

```
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    # Replace this with the actual output from your LLM application
    actual_output="We offer a 30-day full refund at no extra costs.",
    retrieval_context=["All customers are eligible for a 30 day full refund at no extra costs."]
)

answer_relevancy_metric.measure(test_case)
print(answer_relevancy_metric.score)
# All metrics also offer an explanation
print(answer_relevancy_metric.reason)
```

Note that some metrics are for RAG pipelines, while others are for fine-tuning. Make sure to use our docs to pick the right one for your use case.

## A Note on Env Variables (.env / .env.local)

DeepEval auto-loads `.env.local` then `.env` from the current working directory **at import time** . **Precedence:** process env -&gt; `.env.local` -&gt; `.env` . Opt out with `DEEPEVAL_DISABLE_DOTENV=1` .

```
cp .env.example .env.local
# then edit .env.local (ignored by git)
```

# DeepEval With Confident AI

[Confident AI](https://www.confident-ai.com/?utm_source=deepeval&utm_medium=github&utm_content=cli_login_section) is an all-in-one platform to manage datasets, trace LLM applications, and run evaluations in production. Log in from the CLI to get started:

```
deepeval login
```

Then run your tests as usual - results are automatically synced to the platform:

```
deepeval test run test_chatbot.py
```

Demo GIF

Prefer to stay in your IDE? Use DeepEval via [Confident AI's MCP server](https://github.com/confident-ai/confident-mcp-server) as the persistent layer to run evals, pull datasets, and inspect traces without leaving your editor.

Confident AI MCP Architecture

<!-- image -->

Everything on Confident AI is available [here](https://www.confident-ai.com/docs?utm_source=deepeval&utm_medium=github&utm_content=cloud_docs) .

# Contributing

Please read [CONTRIBUTING.md](https://github.com/confident-ai/deepeval/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

# Roadmap

Features:

- [x] Integration with Confident AI
- [x] Implement G-Eval
- [x] Implement RAG metrics
- [x] Implement Conversational metrics
- [x] Evaluation Dataset Creation
- [x] Red-Teaming
- [ ] DAG custom metrics
- [ ] Guardrails

# Authors

Built by the founders of Confident AI. Contact jeffreyip@confident-ai.com for all enquiries.

# License

DeepEval is licensed under Apache 2.0 - see the [LICENSE.md](https://github.com/confident-ai/deepeval/blob/main/LICENSE.md) file for details.