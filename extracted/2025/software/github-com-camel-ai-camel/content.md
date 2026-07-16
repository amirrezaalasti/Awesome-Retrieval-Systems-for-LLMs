Banner

<!-- image -->

[Documentation](https://camel-ai.github.io/camel/index) [Discord](https://discord.camel-ai.org/) [X](https://x.com/CamelAIOrg) [Reddit](https://www.reddit.com/r/CamelAI/) [Wechat](https://ghli.org/camel/wechat.png) [Hugging Face](https://huggingface.co/camel-ai) [Star](https://github.com/camel-ai/camel/stargazers) [Package License](https://github.com/camel-ai/camel/blob/master/licenses/LICENSE) [PyPI Download](https://pypi.org/project/camel-ai) [English](README.md)

#### [Community](https://github.com/camel-ai/camel#community)

🐫 CAMEL is an open-source community dedicated to finding the scaling laws of agents. We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks. To facilitate research in this field, we implement and support various types of agents, tasks, prompts, models, and simulated environments.

Join us ( [*Discord*](https://discord.camel-ai.org/) or [*WeChat*](https://ghli.org/camel/wechat.png) ) in pushing the boundaries of finding the scaling laws of agents.

🌟 Star CAMEL on GitHub and be instantly notified of new releases.

Star

<!-- image -->

```
Table of contents
```

- [CAMEL Framework Design Principles](#camel-framework-design-principles)
- [Why Use CAMEL for Your Research?](#why-use-camel-for-your-research)
- [What Can You Build With CAMEL?](#what-can-you-build-with-camel)
    - [Data Generation](#1-data-generation)
    - [Task Automation](#2-task-automation)
    - [World Simulation](#3-world-simulation)
- [Quick Start](#quick-start)
    - [Starting with ChatAgent](#starting-with-chatagent)
    - [Seeking Help](#seeking-help)
- [Tech Stack](#tech-stack)
- [Research](#research)
- [Synthetic Datasets](#synthetic-datasets)
- [Cookbooks (Usecases)](#cookbooks-usecases)
    - [Basic Concepts](#1-basic-concepts)
    - [Advanced Features](#2-advanced-features)
    - [Model Training &amp; Data Generation](#3-model-training--data-generation)
    - [Multi-Agent Systems &amp; Applications](#4-multi-agent-systems--applications)
    - [Data Processing](#5-data-processing)
- [Real-World Usecases](#real-world-usecases)
- [🧱 Built with CAMEL (Real-world Producs &amp; Research)](#-built-with-camel-real-world-producs--research)
    - [Research Projects](#research-projects)
    - [Product Projects](#product-projects)
- [🗓️ Events](#️-events)
- [Contributing to CAMEL](#contributing-to-camel)
- [Community &amp; Contact](#community--contact)
- [Citation](#citation)
- [Acknowledgment](#acknowledgment)
- [License](#license)

## CAMEL Framework Design Principles

### 🧬 Evolvability

The framework enables multi-agent systems to continuously evolve by generating data and interacting with environments. This evolution can be driven by reinforcement learning with verifiable rewards or supervised learning.

### 📈 Scalability

The framework is designed to support systems with millions of agents, ensuring efficient coordination, communication, and resource management at scale.

### 💾 Statefulness

Agents maintain stateful memory, enabling them to perform multi-step interactions with environments and efficiently tackle sophisticated tasks.

### 📖 Code-as-Prompt

Every line of code and comment serves as a prompt for agents. Code should be written clearly and readably, ensuring both humans and agents can interpret it effectively.

## Why Use CAMEL for Your Research?

We are a community-driven research collective comprising over 100 researchers dedicated to advancing frontier research in Multi-Agent Systems. Researchers worldwide choose CAMEL for their studies based on the following reasons.

|    |                                      |                                                                                                                                                                            |
|----|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ✅  | Large-Scale Agent System             | Simulate up to 1M agents to study emergent behaviors and scaling laws in complex, multi-agent environments.                                                                |
| ✅  | Dynamic Communication                | Enable real-time interactions among agents, fostering seamless collaboration for tackling intricate tasks.                                                                 |
| ✅  | Stateful Memory                      | Equip agents with the ability to retain and leverage historical context, improving decision-making over extended interactions.                                             |
| ✅  | Support for Multiple Benchmarks      | Utilize standardized benchmarks to rigorously evaluate agent performance, ensuring reproducibility and reliable comparisons.                                               |
| ✅  | Support for Different Agent Types    | Work with a variety of agent roles, tasks, models, and environments, supporting interdisciplinary experiments and diverse research applications.                           |
| ✅  | Data Generation and Tool Integration | Automate the creation of large-scale, structured datasets while seamlessly integrating with multiple tools, streamlining synthetic data generation and research workflows. |

## What Can You Build With CAMEL?

### 1. Data Generation

CoT Data Generation

<!-- image -->

Self-Instruct Data Generation

<!-- image -->

Source2Synth Data Generation

<!-- image -->

Self-Improving Data Generation

<!-- image -->

### 2. Task Automation

Role Playing

<!-- image -->

Workforce

<!-- image -->

RAG Pipeline

<!-- image -->

### 3. World Simulation

Oasis Case

<!-- image -->

## Quick Start

Installing CAMEL is a breeze thanks to its availability on PyPI. Simply open your terminal and run:

```
pip install camel-ai
```

### Starting with ChatAgent

This example demonstrates how to create a `ChatAgent` using the CAMEL framework and perform a search query using DuckDuckGo.

1. **Install the tools package:**

```
pip install 'camel-ai[web_tools]'
```

1. **Set up your OpenAI API key:**

```
export OPENAI_API_KEY='your_openai_api_key'
```

Alternatively, use a `.env` file:

```
cp .env.example .env
# then edit .env and add your keys
```

1. **Run the following Python code:**

```
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.agents import ChatAgent
from camel.toolkits import SearchToolkit

model = ModelFactory.create(
  model_platform=ModelPlatformType.OPENAI,
  model_type=ModelType.GPT_4O,
  model_config_dict={"temperature": 0.0},
)

search_tool = SearchToolkit().search_duckduckgo

agent = ChatAgent(model=model, tools=[search_tool])

response_1 = agent.step("What is CAMEL-AI?")
print(response_1.msgs[0].content)
# CAMEL-AI is the first LLM (Large Language Model) multi-agent framework
# and an open-source community focused on finding the scaling laws of agents.
# ...

response_2 = agent.step("What is the Github link to CAMEL framework?")
print(response_2.msgs[0].content)
# The GitHub link to the CAMEL framework is
# [https://github.com/camel-ai/camel](https://github.com/camel-ai/camel).
```

1. **(Optional) Enable model request/response logs:**

```
export CAMEL_MODEL_LOG_ENABLED=true
export CAMEL_MODEL_LOG_MODEL_CONFIG_ENABLED=true
export CAMEL_LOG_DIR=camel_logs
```

- `CAMEL_MODEL_LOG_ENABLED` : Enables request/response JSON logs.
- `CAMEL_MODEL_LOG_MODEL_CONFIG_ENABLED` : Controls whether `model_config_dict` is logged under `request.model_config_dict` . When unset, it defaults to the same value as `CAMEL_MODEL_LOG_ENABLED` .
- `CAMEL_LOG_DIR` : Directory for generated log files (default: `camel_logs` ).
- Logs are written as UTF-8 JSON with multilingual text preserved (for example Chinese, Japanese, Arabic) without Unicode escape noise.

For more detailed instructions and additional configuration options, check out the [installation section](https://github.com/camel-ai/camel/blob/master/docs/get_started/installation.md) . After running, you can explore our CAMEL Tech Stack and Cookbooks at [docs.camel-ai.org](https://docs.camel-ai.org/) to build powerful multi-agent systems. We provide a [Google Colab](https://colab.research.google.com/drive/1AzP33O8rnMW__7ocWJhVBXjKziJXPtim?usp=sharing) demo showcasing a conversation between two ChatGPT agents playing roles as a python programmer and a stock trader collaborating on developing a trading bot for stock market.

Explore different types of agents, their roles, and their applications.

- [**Creating Your First Agent**](https://docs.camel-ai.org/cookbooks/basic_concepts/create_your_first_agent)
- [**Creating Your First Agent Society**](https://docs.camel-ai.org/cookbooks/basic_concepts/create_your_first_agents_society)
- [**Critic Agents**](https://docs.camel-ai.org/cookbooks/advanced_features/critic_agents_and_tree_search)

### Seeking Help

Please reach out to us on [CAMEL discord](https://discord.camel-ai.org/) if you encounter any issue set up CAMEL.

## Tech Stack

TechStack

<!-- image -->

### Key Modules

Core components and utilities to build, operate, and enhance CAMEL-AI agents and societies.

## 

| Module            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| Agents            | Core agent architectures and behaviors for autonomous operation.            |
| Agent Societies   | Components for building and managing multi-agent systems and collaboration. |
| Data Generation   | Tools and methods for synthetic data creation and augmentation.             |
| Models            | Model architectures and customization options for agent intelligence.       |
| Tools             | Tools integration for specialized agent tasks.                              |
| Memory            | Memory storage and retrieval mechanisms for agent state management.         |
| Storage           | Persistent storage solutions for agent data and states.                     |
| Benchmarks        | Performance evaluation and testing frameworks.                              |
| Interpreters      | Code and command interpretation capabilities.                               |
| Data Loaders      | Data ingestion and preprocessing tools.                                     |
| Retrievers        | Knowledge retrieval and RAG components.                                     |
| Runtime           | Execution environment and process management.                               |
| Human-in-the-Loop | Interactive components for human oversight and intervention.                |

## Research

We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks.

**Explore our research projects:**

OWL

<!-- image -->

OASIS

<!-- image -->

CRAB

<!-- image -->

Loong

<!-- image -->

Agent Trust

<!-- image -->

Emos

<!-- image -->

### Research with US

We warmly invite you to use CAMEL for your impactful research.

Rigorous research takes time and resources. We are a community-driven research collective with 100+ researchers exploring the frontier research of Multi-agent Systems. Join our ongoing projects or test new ideas with us, [reach out via email](mailto:camel-ai@eigent.ai) for more information.

Partners

<!-- image -->

## Synthetic Datasets

### 1. Utilize Various LLMs as Backends

For more details, please see our [`Models Documentation`](https://docs.camel-ai.org/key_modules/models#) .

**Data (Hosted on Hugging Face)**

| Dataset    | Chat format   | Instruction format   | Chat format (translated)   |
|------------|---------------|----------------------|----------------------------|
| AI Society | Chat format   | Instruction format   | Chat format (translated)   |
| Code       | Chat format   | Instruction format   | x                          |
| Math       | Chat format   | x                    | x                          |
| Physics    | Chat format   | x                    | x                          |
| Chemistry  | Chat format   | x                    | x                          |
| Biology    | Chat format   | x                    | x                          |

### 2. Visualizations of Instructions and Tasks

| Dataset      | Instructions   | Tasks   |
|--------------|----------------|---------|
| AI Society   | Instructions   | Tasks   |
| Code         | Instructions   | Tasks   |
| Misalignment | Instructions   | Tasks   |

## Cookbooks (Usecases)

Practical guides and tutorials for implementing specific functionalities in CAMEL-AI agents and societies.

### 1. Basic Concepts

| Cookbook                          | Description                                        |
|-----------------------------------|----------------------------------------------------|
| Creating Your First Agent         | A step-by-step guide to building your first agent. |
| Creating Your First Agent Society | Learn to build a collaborative society of agents.  |
| Message Cookbook                  | Best practices for message handling in agents.     |

### 2. Advanced Features

| Cookbook                         | Description                                           |
|----------------------------------|-------------------------------------------------------|
| Tools Cookbook                   | Integrating tools for enhanced functionality.         |
| Memory Cookbook                  | Implementing memory systems in agents.                |
| RAG Cookbook                     | Recipes for Retrieval-Augmented Generation.           |
| Graph RAG Cookbook               | Leveraging knowledge graphs with RAG.                 |
| Track CAMEL Agents with AgentOps | Tools for tracking and managing agents in operations. |

### 3. Model Training &amp; Data Generation

| Cookbook                                               | Description                                                                                                                        |
|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Data Generation with CAMEL and Finetuning with Unsloth | Learn how to generate data with CAMEL and fine-tune models effectively with Unsloth.                                               |
| Data Gen with Real Function Calls and Hermes Format    | Explore how to generate data with real function calls and the Hermes format.                                                       |
| CoT Data Generation and Upload Data to Huggingface     | Uncover how to generate CoT data with CAMEL and seamlessly upload it to Huggingface.                                               |
| CoT Data Generation and SFT Qwen with Unsolth          | Discover how to generate CoT data using CAMEL and SFT Qwen with Unsolth, and seamlessly upload your data and model to Huggingface. |

### 4. Multi-Agent Systems &amp; Applications

| Cookbook                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                             |
|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Role-Playing Scraper for Report & Knowledge Graph Generation                                             | Create role-playing agents for data scraping and reporting.                                                                                                                                                                                                                                                                                                                                                                             |
| Create A Hackathon Judge Committee with Workforce                                                        | Building a team of agents for collaborative judging.                                                                                                                                                                                                                                                                                                                                                                                    |
| Dynamic Knowledge Graph Role-Playing: Multi-Agent System with dynamic, temporally-aware knowledge graphs | Builds dynamic, temporally-aware knowledge graphs for financial applications using a multi-agent system. It processes financial reports, news articles, and research papers to help traders analyze data, identify relationships, and uncover market insights. The system also utilizes diverse and optional element node deduplication techniques to ensure data integrity and optimize graph structure for financial decision-making. |
| Customer Service Discord Bot with Agentic RAG                                                            | Learn how to build a robust customer service bot for Discord using Agentic RAG.                                                                                                                                                                                                                                                                                                                                                         |
| Customer Service Discord Bot with Local Model                                                            | Learn how to build a robust customer service bot for Discord using Agentic RAG which supports local deployment.                                                                                                                                                                                                                                                                                                                         |

### 5. Data Processing

| Cookbook                                           | Description                                                                             |
|----------------------------------------------------|-----------------------------------------------------------------------------------------|
| Video Analysis                                     | Techniques for agents in video data analysis.                                           |
| 3 Ways to Ingest Data from Websites with Firecrawl | Explore three methods for extracting and processing data from websites using Firecrawl. |
| Create AI Agents that work with your PDFs          | Learn how to create AI agents that work with your PDFs using Chunkr and Mistral AI.     |

## Real-World Usecases

Real-world usecases demonstrating how CAMEL's multi-agent framework enables real business value across infrastructure automation, productivity workflows, retrieval-augmented conversations, intelligent document/video analysis, and collaborative research.

### 1 Infrastructure Automation

| Usecase              | Description                                                                                                                                                                                                                                                   |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ACI MCP              | Real-world usecases demonstrating how CAMEL's multi-agent framework enables real business value across infrastructure automation, productivity workflows, retrieval-augmented conversations, intelligent document/video analysis, and collaborative research. |
| Cloudflare MCP CAMEL | Intelligent agents manage Cloudflare resources dynamically, enabling scalable and efficient cloud security and performance tuning.                                                                                                                            |

### 2 Productivity &amp; Business Workflows

| Usecase              | Description                                                                                     |
|----------------------|-------------------------------------------------------------------------------------------------|
| Airbnb MCP           | Coordinate agents to optimize and manage Airbnb listings and host operations.                   |
| PPTX Toolkit Usecase | Analyze PowerPoint documents and extract structured insights through multi-agent collaboration. |

### 3 Retrieval-Augmented Multi-Agent Chat

| Usecase           | Description                                                                                                                                           |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Chat with GitHub  | Query and understand GitHub codebases through CAMEL agents leveraging RAG-style workflows, accelerating developer onboarding and codebase navigation. |
| Chat with YouTube | Conversational agents extract and summarize video transcripts, enabling faster content understanding and repurposing.                                 |

### 4 Video &amp; Document Intelligence

| Usecase     | Description                                                                                                         |
|-------------|---------------------------------------------------------------------------------------------------------------------|
| YouTube OCR | Agents perform OCR on video screenshots to summarize visual content, supporting media monitoring and compliance.    |
| Mistral OCR | CAMEL agents use OCR with Mistral to analyze documents, reducing manual effort in document understanding workflows. |

### 5 Research &amp; Collaboration

| Usecase                        | Description                                                                                                                         |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Multi-Agent Research Assistant | Simulates a team of research agents collaborating on literature review, improving efficiency in exploratory analysis and reporting. |

## 🧱 Built with CAMEL (Real-world Producs &amp; Research)

Built with CAMEL

<!-- image -->

### Research Projects

| Name         | Description                                         |
|--------------|-----------------------------------------------------|
| ChatDev      | Communicative Agents for software Development       |
| Paper2Poster | Multimodal poster automation from scientific papers |
| Paper2Video  | Automatic video generation from scientific papers   |

### Product Projects

| Name   | Description                           |
|--------|---------------------------------------|
| Eigent | The World First Multi-agent Workforce |

## 🗓️ Events

We are actively involved in community events including:

- 🎙️ **Community Meetings** - Weekly virtual syncs with the CAMEL team
- 🏆 **Competitions** - Hackathons, Bounty Tasks and coding challenges hosted by CAMEL
- 🤝 **Volunteer Activities** - Contributions, documentation drives, and mentorship
- 🌍 **Ambassador Programs** - Represent CAMEL in your university or local tech groups

Want to host or participate in a CAMEL event? Join our [Discord](https://discord.com/invite/CNcNpquyDc) or want to be part of [Ambassador Program](https://www.camel-ai.org/ambassador) .

## Contributing to CAMEL

For those who'd like to contribute code, we appreciate your interest in contributing to our open-source initiative. Please take a moment to review our [contributing guidelines](https://github.com/camel-ai/camel/blob/master/CONTRIBUTING.md) to get started on a smooth collaboration journey.🚀

We also welcome you to help CAMEL grow by sharing it on social media, at events, or during conferences. Your support makes a big difference!

## Contributors

<!-- image -->

Made with [contrib.rocks](https://contrib.rocks/) .

## Acknowledgment

Special thanks to [Nomic AI](https://home.nomic.ai/) for giving us extended access to their data set exploration tool (Atlas).

We would also like to thank Haya Hammoud for designing the initial logo of our project.

We implemented amazing research ideas from other works for you to build, compare and customize your agents. If you use any of these modules, please kindly cite the original works:

- `TaskCreationAgent` and `TaskPrioritizationAgent` from *Nakajima et al.* : [Task-Driven Autonomous Agent](https://yoheinakajima.com/task-driven-autonomous-agent-utilizing-gpt-4-pinecone-and-langchain-for-diverse-applications/) .
- `PersonaHub` from *Tao Ge et al.* : [Scaling Synthetic Data Creation with 1,000,000,000 Personas](https://arxiv.org/pdf/2406.20094) . [ [Example](https://github.com/camel-ai/camel/blob/master/examples/personas/personas_generation.py) ]
- `Self-Instruct` from *Yizhong Wang et al.* : [SELF-INSTRUCT: Aligning Language Models with Self-Generated Instructions](https://arxiv.org/pdf/2212.10560) . [ [Example](https://github.com/camel-ai/camel/blob/master/examples/datagen/self_instruct/self_instruct.py) ]

## License

The source code is licensed under Apache 2.0.

## Citation

```
@inproceedings{li2023camel,
  title={CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society},
  author={Li, Guohao and Hammoud, Hasan Abed Al Kader and Itani, Hani and Khizbullin, Dmitrii and Ghanem, Bernard},
  booktitle={Thirty-seventh Conference on Neural Information Processing Systems},
  year={2023}
}
```

Here is an example of how to cite our work:

```
We use the CAMEL framework \cite{li2023camel} to develop the agents used in our experiments.
```

## Community &amp; Contact

For more information please contact camel-ai@eigent.ai

- **GitHub Issues:** Report bugs, request features, and track development. [Submit an issue](https://github.com/camel-ai/camel/issues)
- **Discord:** Get real-time support, chat with the community, and stay updated. [Join us](https://discord.camel-ai.org/)
- **X (Twitter):** Follow for updates, AI insights, and key announcements. [Follow us](https://x.com/CamelAIOrg)
- **Ambassador Project:** Advocate for CAMEL-AI, host events, and contribute content. [Learn more](https://www.camel-ai.org/community)
- **WeChat Community:** Scan the QR code below to join our WeChat community.
WeChat QR Code

<!-- image -->