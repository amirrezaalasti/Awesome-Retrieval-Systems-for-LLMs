# 🔍 Awesome Retrieval Systems for LLMs

> 📚 A curated collection of retrieval-centric systems, frameworks, research papers, benchmarks, datasets, vector databases, and infrastructure for building **Retrieval-Augmented Generation (RAG)**, **Knowledge-Augmented Generation (KAG)**, **GraphRAG**, **agentic retrieval**, and reasoning-centric **Large Language Model (LLM)** applications.

<p align="center">

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Cite](https://img.shields.io/badge/Cite-CITATION.cff-blue.svg)](CITATION.cff)
[![Maintenance](https://img.shields.io/badge/Maintained%20%F0%9F%92%9A-Yes-brightgreen.svg)](https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs)

</p>

<p align="center">

**Quick links:** [📑 TOC](#-table-of-contents) · [🎯 Scope](#-repository-scope) · [📅 By Year](#-year-by-year-resources) · [🕸️ GraphRAG](#-knowledge-graph--graphrag--kag) · [🤖 Agentic](#-agentic--reasoning-centric-retrieval-1) · [📊 Evaluation](#-evaluation--analysis-frameworks) · [📖 Cite](#-citation) · [📜 License](#-license)

</p>

---

## 💡 Motivation

Large Language Models (LLMs) possess remarkable reasoning and generation capabilities but remain constrained by:

- Static parametric knowledge
- Hallucinations
- Limited domain expertise
- Context window limitations
- Lack of transparent evidence
- Difficulty incorporating continually changing information

Retrieval systems address these limitations by connecting LLMs with external knowledge sources, including:

- Vector databases
- Search engines
- Knowledge graphs
- Relational databases
- Enterprise documents
- PDFs
- HTML pages
- Scientific literature
- Images and multimodal documents
- APIs and external tools

Since the introduction of **Retrieval-Augmented Generation (RAG)** in 2020, retrieval architectures have rapidly evolved into sophisticated systems featuring:

- Hybrid dense + sparse retrieval
- Multi-hop retrieval
- Knowledge Graph Retrieval
- GraphRAG
- Knowledge-Augmented Generation (KAG)
- Agentic retrieval
- Tool-using agents
- Long-context retrieval
- Multimodal retrieval
- Reasoning-aware retrieval
- Self-improving retrieval
- Retrieval evaluation frameworks

This repository aims to provide a comprehensive, continuously updated resource for researchers and practitioners interested in retrieval-centric systems for LLMs.

### RAG vs. GraphRAG vs. KAG — What's the Difference?

These three terms are often used loosely and interchangeably, but they describe distinct architectural choices:

| Dimension | Classic RAG | GraphRAG | KAG (Knowledge-Augmented Generation) |
|-----------|-------------|----------|----------------------------------------|
| Knowledge unit | Text chunks / passages | Entities, relations, communities | Entities + logical/ontological schema |
| Index structure | Flat vector index | Knowledge graph (+ optional vector index) | Knowledge graph + ontology + rules |
| Retrieval mechanism | Nearest-neighbor similarity search | Graph traversal, community summaries, multi-hop expansion | Logical-form queries, symbolic reasoning, hybrid graph + vector retrieval |
| Best suited for | Fact lookup, single-hop QA, semantic search | Multi-hop reasoning, "global" questions over a whole corpus, entity-centric queries | Domain-specific reasoning requiring precision, auditability, and rule compliance |
| Representative systems | DPR, ColBERT, RAGAS-evaluated pipelines | Microsoft GraphRAG, LightRAG, HippoRAG | OpenSPG/KAG, Neo4j GraphRAG |
| Trade-off | Cheap to build, weak at multi-hop reasoning | Expensive indexing (LLM-driven extraction), strong at "connect-the-dots" questions | Highest precision and explainability, highest engineering/schema-design cost |

In practice, production systems increasingly blend all three: dense/sparse retrieval for recall, graph structure for multi-hop reasoning, and symbolic/ontological constraints where correctness and auditability matter (e.g., legal, medical, financial domains).

---

# 📑 Table of Contents

- [🔍 Awesome Retrieval Systems for LLMs](#-awesome-retrieval-systems-for-llms)
  - [💡 Motivation](#-motivation)
    - [RAG vs. GraphRAG vs. KAG — What's the Difference?](#rag-vs-graphrag-vs-kag--whats-the-difference)
- [📑 Table of Contents](#-table-of-contents)
- [🎯 Repository Scope](#-repository-scope)
  - [🔗 Retrieval-Augmented Generation (RAG)](#-retrieval-augmented-generation-rag)
  - [🧩 Knowledge-Augmented Generation (KAG)](#-knowledge-augmented-generation-kag)
  - [🌐 GraphRAG](#-graphrag)
  - [🖼️ Multimodal Retrieval](#️-multimodal-retrieval)
  - [🤖 Agentic Retrieval](#-agentic-retrieval)
  - [🏗️ Infrastructure](#️-infrastructure)
  - [📏 Evaluation](#-evaluation)
- [🗂️ Taxonomy of Retrieval Systems](#️-taxonomy-of-retrieval-systems)
  - [1. 📚 Knowledge Representation](#1--knowledge-representation)
  - [2. 🔎 Retrieval Mechanism](#2--retrieval-mechanism)
  - [3. 🗃️ Knowledge Source](#3-️-knowledge-source)
  - [4. 🎨 Modality](#4--modality)
  - [5. 🧠 Reasoning Strategy](#5--reasoning-strategy)
- [📖 How to Use This Repository](#-how-to-use-this-repository)
- [📅 Yearly Overview](#-yearly-overview)
- [🏷️ Resource Categories](#️-resource-categories)
- [🧭 Reading Guide](#-reading-guide)
- [📆 Year-by-Year Resources](#-year-by-year-resources)
- [🗓️ 2019](#️-2019)
  - [📚 Surveys](#-surveys)
  - [Dense Retrieval Foundations](#dense-retrieval-foundations)
  - [Knowledge Retrieval](#knowledge-retrieval)
  - [Benchmarks](#benchmarks)
- [🗓️ 2020](#️-2020)
  - [📚 Surveys](#-surveys-1)
  - [RAG Systems \& Frameworks](#rag-systems--frameworks)
  - [Retrieval Models](#retrieval-models)
  - [Knowledge Retrieval](#knowledge-retrieval-1)
  - [Benchmarks](#benchmarks-1)
- [🗓️ 2021](#️-2021)
  - [📚 Surveys](#-surveys-2)
  - [🛠️ Retrieval Frameworks](#️-retrieval-frameworks)
    - [Haystack](#haystack)
    - [ColBERT](#colbert)
    - [Contriever](#contriever)
  - [Search Infrastructure](#search-infrastructure)
    - [Elasticsearch](#elasticsearch)
    - [OpenSearch](#opensearch)
  - [Evaluation](#evaluation)
    - [BEIR](#beir)
- [🗓️ 2022](#️-2022)
  - [📚 Surveys](#-surveys-3)
  - [RAG Frameworks](#rag-frameworks)
    - [LangChain](#langchain)
    - [LlamaIndex (GPT Index)](#llamaindex-gpt-index)
    - [DSP](#dsp)
  - [Vector Databases](#vector-databases)
    - [FAISS](#faiss)
    - [Milvus](#milvus)
    - [Weaviate](#weaviate)
    - [Qdrant](#qdrant)
    - [Pinecone](#pinecone)
    - [Chroma](#chroma)
  - [Document Retrieval](#document-retrieval)
    - [Unstructured](#unstructured)
  - [Knowledge Retrieval](#knowledge-retrieval-2)
    - [HyDE](#hyde)
  - [Retrieval-Augmented Reasoning \& Agents](#retrieval-augmented-reasoning--agents)
    - [Atlas](#atlas)
    - [ReAct](#react)
    - [IRCoT](#ircot)
  - [Evaluation](#evaluation-1)
    - [MTEB](#mteb)
  - [Notable 2022 Trends](#notable-2022-trends)
- [🗓️ 2023](#️-2023)
  - [📚 Surveys](#-surveys-4)
  - [RAG Systems \& Frameworks](#rag-systems--frameworks-1)
    - [LangChain](#langchain-1)
    - [LlamaIndex](#llamaindex)
    - [Haystack 2.0](#haystack-20)
    - [DSPy](#dspy)
  - [Advanced Retrieval](#advanced-retrieval)
    - [Self-RAG](#self-rag)
    - [Rewrite-Retrieve-Read](#rewrite-retrieve-read)
    - [HyDE](#hyde-1)
    - [REPLUG](#replug)
    - [FLARE (Forward-Looking Active Retrieval)](#flare-forward-looking-active-retrieval)
    - [StructGPT](#structgpt)
    - [Think-on-Graph (ToG)](#think-on-graph-tog)
    - [Chain-of-Note](#chain-of-note)
    - [MemGPT](#memgpt)
  - [Document \& Enterprise RAG](#document--enterprise-rag)
    - [Unstructured](#unstructured-1)
    - [LlamaParse](#llamaparse)
    - [Apache Tika](#apache-tika)
    - [Onyx (formerly Danswer)](#onyx-formerly-danswer)
  - [Multimodal Retrieval](#multimodal-retrieval)
    - [CLIP](#clip)
    - [BLIP-2](#blip-2)
    - [LLaVA](#llava)
  - [Agentic Retrieval](#agentic-retrieval)
    - [AutoGen](#autogen)
    - [CrewAI](#crewai)
    - [MetaGPT](#metagpt)
    - [Microsoft Semantic Kernel](#microsoft-semantic-kernel)
  - [Vector Databases](#vector-databases-1)
    - [Milvus](#milvus-1)
    - [Weaviate](#weaviate-1)
    - [Qdrant](#qdrant-1)
    - [Pinecone](#pinecone-1)
    - [Chroma](#chroma-1)
    - [LanceDB](#lancedb)
    - [pgvector](#pgvector)
    - [Redis (Vector Search)](#redis-vector-search)
    - [MongoDB Atlas Vector Search](#mongodb-atlas-vector-search)
    - [txtai](#txtai)
  - [📊 Evaluation \& Benchmarks](#-evaluation--benchmarks)
    - [RAGAS](#ragas)
    - [TruLens](#trulens)
    - [DeepEval](#deepeval)
    - [BEIR](#beir-1)
    - [MTEB](#mteb-1)
    - [RGB (Retrieval-Augmented Generation Benchmark)](#rgb-retrieval-augmented-generation-benchmark)
    - [LongBench](#longbench)
    - [Giskard](#giskard)
    - [Arize Phoenix](#arize-phoenix)
    - [Langfuse](#langfuse)
  - [🔢 Embedding Models](#-embedding-models)
    - [BGE](#bge)
    - [E5](#e5)
    - [Instructor](#instructor)
    - [Voyage AI Embeddings](#voyage-ai-embeddings)
  - [Major Trends in 2023](#major-trends-in-2023)
- [🗓️ 2024](#️-2024)
  - [📚 Surveys](#-surveys-5)
- [🧠 RAG Systems \& Frameworks](#-rag-systems--frameworks)
    - [GraphRAG (Microsoft)](#graphrag-microsoft)
    - [LightRAG](#lightrag)
    - [RAPTOR](#raptor)
    - [FlashRAG](#flashrag)
    - [FastRAG](#fastrag)
    - [Pathway](#pathway)
    - [R2R](#r2r)
    - [RAGFlow](#ragflow)
  - [Advanced Retrieval \& RAG Papers](#advanced-retrieval--rag-papers)
    - [Corrective RAG (CRAG)](#corrective-rag-crag)
    - [Adaptive-RAG](#adaptive-rag)
    - [RQ-RAG](#rq-rag)
    - [RAFT (Retrieval-Augmented Fine-Tuning)](#raft-retrieval-augmented-fine-tuning)
    - [RankRAG](#rankrag)
    - [Speculative RAG](#speculative-rag)
    - [RAGTruth](#ragtruth)
    - [CRUD-RAG](#crud-rag)
    - [MultiHop-RAG](#multihop-rag)
    - [RULER](#ruler)
    - [RAGChecker](#ragchecker)
- [🌐 GraphRAG \& Knowledge Graph Systems](#-graphrag--knowledge-graph-systems)
    - [OpenSPG / KAG](#openspg--kag)
    - [HippoRAG](#hipporag)
    - [KG-RAG](#kg-rag)
    - [G-Retriever](#g-retriever)
    - [nano-graphrag](#nano-graphrag)
    - [GraphRAG-SDK (FalkorDB)](#graphrag-sdk-falkordb)
    - [Cognee](#cognee)
    - [Neo4j LLM Graph Builder](#neo4j-llm-graph-builder)
    - [Kuzu](#kuzu)
- [📄 Multimodal \& Document Analysis RAG](#-multimodal--document-analysis-rag)
    - [Docling](#docling)
    - [MinerU](#mineru)
    - [ColPali](#colpali)
    - [Nougat](#nougat)
    - [LlamaParse](#llamaparse-1)
    - [Unstructured](#unstructured-2)
    - [Marker](#marker)
    - [PyMuPDF4LLM](#pymupdf4llm)
    - [Firecrawl](#firecrawl)
    - [Reducto](#reducto)
- [🤖 Agentic \& Reasoning-Centric Retrieval](#-agentic--reasoning-centric-retrieval)
    - [AutoGen](#autogen-1)
    - [CrewAI](#crewai-1)
    - [LangGraph](#langgraph)
    - [OpenDevin](#opendevin)
    - [CAMEL-AI](#camel-ai)
    - [AG2 (AutoGen community fork)](#ag2-autogen-community-fork)
    - [OpenAI Swarm](#openai-swarm)
- [🗄️ Vector Databases \& Retrieval Infrastructure](#️-vector-databases--retrieval-infrastructure)
    - [Milvus](#milvus-2)
    - [Weaviate](#weaviate-2)
    - [Qdrant](#qdrant-2)
    - [Pinecone](#pinecone-2)
    - [LanceDB](#lancedb-1)
    - [Chroma](#chroma-2)
    - [Vespa](#vespa)
    - [turbopuffer](#turbopuffer)
    - [DuckDB VSS](#duckdb-vss)
- [📊 Evaluation \& Benchmarks](#-evaluation--benchmarks-1)
    - [RAGAS](#ragas-1)
    - [TruLens](#trulens-1)
    - [DeepEval](#deepeval-1)
    - [ARES](#ares)
    - [Comet Opik](#comet-opik)
- [🔢 Embedding Models](#-embedding-models-1)
    - [BGE-M3](#bge-m3)
    - [Nomic Embed](#nomic-embed)
    - [Jina Embeddings v3](#jina-embeddings-v3)
    - [Snowflake Arctic Embed](#snowflake-arctic-embed)
- [📈 Major Trends in 2024](#-major-trends-in-2024)
- [🗓️ 2025](#️-2025)
- [📚 Surveys](#-surveys-6)
    - [RAG vs. GraphRAG](#rag-vs-graphrag)
    - [Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG](#agentic-retrieval-augmented-generation-a-survey-on-agentic-rag)
    - [A Survey of Graph Retrieval-Augmented Generation for Customized Large Language Models](#a-survey-of-graph-retrieval-augmented-generation-for-customized-large-language-models)
- [🔬 Agentic Retrieval \& Deep Research](#-agentic-retrieval--deep-research)
    - [OpenAI Deep Research](#openai-deep-research)
    - [AutoGen](#autogen-2)
    - [CrewAI](#crewai-2)
    - [LangGraph](#langgraph-1)
    - [OpenHands (formerly OpenDevin)](#openhands-formerly-opendevin)
    - [CAMEL-AI](#camel-ai-1)
    - [smolagents](#smolagents)
    - [Agno (formerly Phidata)](#agno-formerly-phidata)
    - [PydanticAI](#pydanticai)
- [🧠 GraphRAG \& Graph Memory](#-graphrag--graph-memory)
    - [Microsoft GraphRAG](#microsoft-graphrag)
    - [LightRAG](#lightrag-1)
    - [HippoRAG](#hipporag-1)
    - [Graphiti](#graphiti)
    - [ArchRAG](#archrag)
    - [Zep](#zep)
    - [Mem0](#mem0)
    - [Letta (formerly MemGPT)](#letta-formerly-memgpt)
- [🧩 Knowledge-Augmented Generation (KAG)](#-knowledge-augmented-generation-kag-1)
    - [OpenSPG/KAG](#openspgkag)
    - [Neo4j GraphRAG](#neo4j-graphrag)
    - [Memgraph GraphRAG](#memgraph-graphrag)
- [🏢 Multimodal \& Enterprise Retrieval](#-multimodal--enterprise-retrieval)
    - [Docling](#docling-1)
    - [MinerU](#mineru-1)
    - [ColPali](#colpali-1)
    - [LlamaParse](#llamaparse-2)
- [🛠️ Retrieval Frameworks](#️-retrieval-frameworks-1)
    - [LlamaIndex](#llamaindex-1)
    - [LangChain](#langchain-2)
    - [Haystack](#haystack-1)
    - [DSPy](#dspy-1)
    - [FlashRAG](#flashrag-1)
- [📡 Evaluation \& Observability](#-evaluation--observability)
    - [RAGAS](#ragas-2)
    - [ARES](#ares-1)
    - [TruLens](#trulens-2)
    - [DeepEval](#deepeval-2)
    - [LangSmith](#langsmith)
- [🗄️ Vector Databases \& Retrieval Infrastructure](#️-vector-databases--retrieval-infrastructure-1)
    - [Qdrant](#qdrant-3)
    - [Weaviate](#weaviate-3)
    - [Milvus](#milvus-3)
    - [Pinecone](#pinecone-3)
    - [LanceDB](#lancedb-2)
    - [Vespa](#vespa-1)
- [📈 Major Trends in 2025](#-major-trends-in-2025)
- [🔮 2026](#-2026)
  - [Emerging Directions](#emerging-directions)
    - [Persistent Agent Memory](#persistent-agent-memory)
    - [Graph-Native Agents](#graph-native-agents)
    - [Continual Retrieval](#continual-retrieval)
    - [Structured Reasoning Retrieval](#structured-reasoning-retrieval)
  - [Representative Systems](#representative-systems)
    - [GraphRAG](#graphrag)
    - [HippoRAG](#hipporag-2)
    - [Graphiti](#graphiti-1)
    - [LangGraph](#langgraph-2)
  - [Research Themes](#research-themes)
- [📄 Document \& Web RAG](#-document--web-rag)
  - [Representative Frameworks](#representative-frameworks)
- [🕸️ Knowledge Graph / GraphRAG / KAG](#️-knowledge-graph--graphrag--kag)
  - [Representative Projects](#representative-projects)
    - [Typical GraphRAG Workflow](#typical-graphrag-workflow)
- [🤖 Agentic \& Reasoning-Centric Retrieval](#-agentic--reasoning-centric-retrieval-1)
  - [Popular Frameworks](#popular-frameworks)
- [🗄️ Vector Stores \& Indexing Infrastructure](#️-vector-stores--indexing-infrastructure)
  - [Vector Databases](#vector-databases-2)
- [📊 Evaluation \& Analysis Frameworks](#-evaluation--analysis-frameworks)
  - [Representative Projects](#representative-projects-1)
- [🤝 Contribution Guidelines](#-contribution-guidelines)
  - [Adding a New Entry](#adding-a-new-entry)
  - [Inclusion Criteria](#inclusion-criteria)
- [📖 Citation](#-citation)
    - [BibTeX](#bibtex)
    - [Citation File Format](#citation-file-format)
    - [APA Style](#apa-style)
- [📜 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)
  - [⭐ Star History](#-star-history)
  - [🤝 Maintainers](#-maintainers)

---

# 🎯 Repository Scope

This repository focuses on **retrieval-centric systems** designed for Large Language Models.

Included resources cover:

## 🔗 Retrieval-Augmented Generation (RAG)

- Classic RAG
- Dense Retrieval
- Sparse Retrieval
- Hybrid Retrieval
- Late Interaction
- Memory-Augmented Retrieval

---

## 🧩 Knowledge-Augmented Generation (KAG)

- Knowledge Graph Retrieval
- Ontology-guided Retrieval
- Logical-form Guided Retrieval
- Symbolic Reasoning
- Graph-based Memory

---

## 🌐 GraphRAG

- Graph Construction
- Graph Retrieval
- Community Detection
- Entity-centric Retrieval
- Multi-hop Reasoning
- Knowledge Graph QA

---

## 🖼️ Multimodal Retrieval

- PDF Understanding
- Tables
- Images
- HTML
- Charts
- Scientific Documents
- OCR Pipelines

---

## 🤖 Agentic Retrieval

- Retrieval Agents
- Tool-Using Agents
- Planner Agents
- Multi-Agent Retrieval
- Self-Reflection
- Query Rewriting
- Retrieval Planning

---

## 🏗️ Infrastructure

- Vector Databases
- Embedding Models
- Search Engines
- Indexing Frameworks
- Chunking
- Document Parsing
- Data Connectors

---

## 📏 Evaluation

- Retrieval Metrics
- Generation Metrics
- Benchmarks
- Hallucination Detection
- Groundedness
- Faithfulness
- Context Precision
- Context Recall

---

# 🗂️ Taxonomy of Retrieval Systems

This repository categorizes systems across several orthogonal dimensions.

## 1. 📚 Knowledge Representation

| Representation | Description |
|---------------|-------------|
| Text Chunks | Fixed-size or semantic chunks stored in vector databases |
| Documents | Entire documents retrieved directly |
| Tables | Structured tabular retrieval |
| Knowledge Graphs | Entity-relation graphs |
| Ontologies | Domain-specific semantic graphs |
| SQL Databases | Structured relational retrieval |
| APIs | Tool-based retrieval |
| Multimodal Documents | PDFs, images, HTML, charts |

---

## 2. 🔎 Retrieval Mechanism

| Mechanism | Examples |
|-----------|----------|
| Dense Retrieval | DPR, Contriever |
| Sparse Retrieval | BM25 |
| Hybrid Retrieval | BM25 + Vector Search, Redis Vector Search |
| Graph Retrieval | GraphRAG, nano-graphrag |
| KG Retrieval | KAG, Think-on-Graph |
| Multi-hop Retrieval | HotpotQA systems, MultiHop-RAG, IRCoT |
| Self-Corrective Retrieval | Corrective RAG (CRAG), Adaptive-RAG |
| Agentic Retrieval | Planner-based retrieval, smolagents |
| Query Rewriting | Rewrite-Retrieve-Read, RQ-RAG |
| Tool Retrieval | Search agents, ReAct |

---

## 3. 🗃️ Knowledge Source

| Source | Typical Systems |
|---------|----------------|
| Vector Database | Milvus, Pinecone, Weaviate, pgvector |
| Search Engine | Elasticsearch, OpenSearch |
| Knowledge Graph | Neo4j, OpenSPG, Kuzu |
| SQL Database | Text-to-SQL systems |
| Web Search | Search APIs, Firecrawl |
| Enterprise Documents | Internal knowledge bases, Onyx |
| Scientific Literature | Semantic Scholar, arXiv |
| Multimodal Corpora | PDFs, images, charts |
| Agent Memory | Zep, Mem0, Letta, Cognee |

---

## 4. 🎨 Modality

| Modality | Examples |
|----------|----------|
| Text | Standard RAG |
| PDF | Document Intelligence |
| HTML | Web RAG |
| Tables | Table RAG |
| Images | Vision-Language Retrieval |
| Video | Multimodal RAG |
| Audio | Speech Retrieval |
| Mixed Documents | Enterprise RAG |

---

## 5. 🧠 Reasoning Strategy

| Strategy | Examples |
|----------|----------|
| Single-hop Retrieval | Classic RAG |
| Multi-hop Retrieval | GraphRAG |
| Logical Retrieval | KAG |
| Symbolic Reasoning | Knowledge Graph QA |
| Agentic Planning | AutoGen, CrewAI |
| Reflection | Self-RAG |
| Tool Use | ReAct-style systems |

---

# 📖 How to Use This Repository

Resources are organized **chronologically** and **by category**.

For each year, entries are grouped into:

- Surveys
- Retrieval Systems & Frameworks
- GraphRAG / Knowledge Graph Systems
- Knowledge-Augmented Generation
- Multimodal & Document Retrieval
- Agentic Retrieval
- Vector Databases & Infrastructure
- Evaluation & Benchmarks

Each entry includes:

- 📄 Paper
- 💻 GitHub repository
- 🌐 Project page (when available)
- 📝 Short description
- 🏷️ Tags

---

# 📅 Yearly Overview

| Year | Surveys | Systems / Frameworks | GraphRAG / KAG | Multimodal | Evaluation | Notable Names |
|------|----------|----------------------|----------------|------------|------------|----------------|
| 2019 | Dense Retrieval Foundations | DPR, REALM (precursors) | — | — | BEIR groundwork | DPR, REALM, ORQA |
| 2020 | RAG Survey Foundations | RAG, FiD | — | — | Natural Questions, KILT | RAG, FiD |
| 2021 | Open-Domain QA Surveys | Haystack, LangChain (early ecosystem), BEIR | KGQA systems | Doc Retrieval | BEIR | Haystack, ColBERT, BEIR |
| 2022 | Retrieval Surveys | LlamaIndex, DSP | Early Graph Retrieval | PDF QA | RAG Evaluation | LlamaIndex, ReAct, Atlas |
| 2023 | RAG Explosion | LangChain, LlamaIndex, Haystack, Self-RAG, Semantic Kernel | GraphRAG research, ToG | Unstructured, Docling precursors | RAGAS, Langfuse, Arize Phoenix | Self-RAG, RAGAS, MemGPT |
| 2024 | Comprehensive Surveys | GraphRAG, LightRAG, RAPTOR, FlashRAG, R2R, RAGFlow | OpenSPG/KAG, Microsoft's GraphRAG, nano-graphrag, Cognee | MinerU, Docling, ColPali, Marker | CRUD-RAG, RGB, RAGChecker | GraphRAG, LightRAG, KAG, CRAG |
| 2025 | Agentic RAG Survey, RAG vs. GraphRAG | DeepResearch agents, Agentic RAG frameworks, smolagents, Agno | Zep, Mem0, Letta, ArchRAG | Multimodal Enterprise RAG | Comet Opik | Agentic RAG, Zep, Mem0 |
| 2026 | Emerging Trends | Continually Updated | Emerging Graph Memory | Long-context Retrieval | Ongoing | TBD |

---

# 🏷️ Resource Categories

The repository includes the following major categories.

| Category | Description |
|-----------|-------------|
| 📚 Surveys | Comprehensive review papers covering retrieval for LLMs |
| 🧠 RAG Frameworks | End-to-end Retrieval-Augmented Generation systems |
| 🌐 GraphRAG | Graph-based retrieval and reasoning |
| 🕸 Knowledge Graphs | Knowledge graph construction and retrieval |
| 🧩 KAG | Knowledge-Augmented Generation frameworks |
| 📄 Document Intelligence | PDF, HTML, OCR, layout-aware retrieval |
| 🖼 Multimodal Retrieval | Vision-language retrieval systems |
| 🤖 Agentic Retrieval | Planning, tool use, autonomous retrieval |
| 🗂 Vector Databases | Storage and similarity search infrastructure |
| 🔍 Search Infrastructure | Search engines and indexing systems |
| 📏 Evaluation | Metrics, benchmarks, hallucination detection |
| 📊 Datasets | Retrieval datasets and benchmarks |

---

# 🧭 Reading Guide

Depending on your interests:

| If you're interested in... | Start with |
|-----------------------------|------------|
| Classic RAG | 2020 → 2022 |
| Production RAG | 2023 |
| GraphRAG | 2024 |
| Knowledge Graph Retrieval | 2024 |
| Enterprise Search | 2023–2025 |
| Agentic Systems | 2024–2026 |
| Multimodal RAG | 2024–2026 |
| Retrieval Evaluation | 2023–2025 |
| Vector Databases | Category Section |
| Benchmarks | Evaluation Section |

---

# 📆 Year-by-Year Resources

The following sections organize retrieval systems chronologically, highlighting the evolution of retrieval-augmented LLM architectures from early dense retrieval and RAG foundations through GraphRAG, Knowledge-Augmented Generation, multimodal retrieval, and agentic retrieval systems.

# 🗓️ 2019

The years preceding modern LLM-based RAG established the foundations of dense retrieval, open-domain question answering, and neural knowledge retrieval.

## 📚 Surveys

- **[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** *(preprint released in 2020; foundational work begun in 2019)* – Introduced dense vector retrieval using dual encoders, replacing sparse lexical retrieval for many QA tasks. `Dense Retrieval` `Open-Domain QA`

---

## Dense Retrieval Foundations

- **DPR (Dense Passage Retrieval)**
  - 📄 Paper: https://arxiv.org/abs/2004.04906
  - 💻 Code: https://github.com/facebookresearch/DPR
  - Facebook Research's dense retriever became one of the foundational building blocks for modern RAG pipelines.

- **ORQA**
  - 📄 Paper: https://arxiv.org/abs/1906.00300
  - 💻 Code: https://github.com/google-research/language
  - Google's Open-Retrieval Question Answering introduced latent retrieval over Wikipedia without explicit supervised retrieval labels.
  `Dense Retrieval`

---

## Knowledge Retrieval

- **REALM**
  - 📄 Paper: https://arxiv.org/abs/2002.08909
  - 💻 Code: https://github.com/google-research/language
  - Retrieval-Augmented Language Model jointly learning retrieval and language modeling.
  `Retrieval LM`

---

## Benchmarks

- **Natural Questions**
  - 📄 https://ai.google.com/research/NaturalQuestions
  - Large-scale open-domain QA benchmark that became a standard evaluation dataset.

- **TriviaQA**
  - 📄 https://nlp.cs.washington.edu/triviaqa/
  - One of the earliest large-scale retrieval QA datasets.

---

# 🗓️ 2020

2020 marks the birth of Retrieval-Augmented Generation (RAG), introducing retrieval as a first-class component in language generation.

## 📚 Surveys

- **[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** – The seminal RAG paper introducing retrieval-augmented generation. `RAG`

---

## RAG Systems & Frameworks

- **RAG**
  - 📄 https://arxiv.org/abs/2005.11401
  - 💻 https://github.com/facebookresearch/DPR
  - Introduced retrieval-augmented generation combining dense retrieval with sequence generation.

- **REALM**
  - 📄 https://arxiv.org/abs/2002.08909
  - 💻 https://github.com/google-research/language
  - Learned retrieval jointly with language model pretraining.

---

## Retrieval Models

- **ANCE**
  - 📄 https://arxiv.org/abs/2007.00808
  - 💻 https://github.com/microsoft/ANCE
  - Improved dense retrieval using asynchronous hard negative mining.

- **RocketQA**
  - 📄 https://arxiv.org/abs/2010.08191
  - 💻 https://github.com/PaddlePaddle/RocketQA
  - Dual-encoder retrieval framework improving passage retrieval quality.

---

## Knowledge Retrieval

- **FiD (Fusion-in-Decoder)**
  - 📄 https://arxiv.org/abs/2007.01282
  - 💻 https://github.com/facebookresearch/FiD
  - Generates answers by fusing multiple retrieved passages during decoding.
  `Fusion Retrieval`

---

## Benchmarks

- **KILT**
  - 📄 https://arxiv.org/abs/2009.02252
  - 💻 https://github.com/facebookresearch/KILT
  - Unified benchmark connecting retrieval and downstream knowledge-intensive tasks.

---

# 🗓️ 2021

Dense retrieval matured into production-ready systems while benchmarking became standardized.

## 📚 Surveys

- **Open-Domain Question Answering Survey**
  - 📄 https://arxiv.org/abs/2101.00774
  - Comprehensive overview of retrieval-based QA systems.

---

## 🛠️ Retrieval Frameworks

### Haystack

- 📄 https://haystack.deepset.ai/

- 💻 https://github.com/deepset-ai/haystack

One of the earliest production-ready open-source frameworks for semantic search, document retrieval, QA, and RAG.

`Framework`

---

### ColBERT

- 📄 https://arxiv.org/abs/2004.12832

- 💻 https://github.com/stanford-futuredata/ColBERT

Introduced late interaction retrieval that dramatically improved retrieval quality while remaining scalable.

`Late Interaction`

---

### Contriever

- 📄 https://arxiv.org/abs/2112.09118

- 💻 https://github.com/facebookresearch/contriever

Unsupervised dense retriever trained without labeled retrieval data.

`Dense Retrieval`

---

## Search Infrastructure

### Elasticsearch

- 🌐 https://www.elastic.co/elasticsearch/

Industry-standard sparse retrieval search engine frequently combined with dense vector retrieval.

---

### OpenSearch

- 🌐 https://opensearch.org/

Open-source search platform supporting hybrid retrieval.

---

## Evaluation

### BEIR

- 📄 https://arxiv.org/abs/2104.08663

- 💻 https://github.com/beir-cellar/beir

Comprehensive benchmark covering diverse retrieval tasks and domains.

`Benchmark`

---

# 🗓️ 2022

The ecosystem shifted from standalone retrieval models to full-stack retrieval frameworks that simplified building LLM applications.

## 📚 Surveys

## RAG Frameworks

### LangChain

- 💻 https://github.com/langchain-ai/langchain

Framework for building retrieval-augmented LLM applications using composable chains, tools, agents, and memory.

`Framework`

---

### LlamaIndex (GPT Index)

- 💻 https://github.com/run-llama/llama_index

Data framework focused on indexing, retrieval, and connecting external knowledge sources to LLMs.

`RAG`

---

### DSP

- 📄 https://arxiv.org/abs/2212.14024

- 💻 https://github.com/stanfordnlp/dsp

Declarative programming framework for language models emphasizing retrieval-aware pipelines.

---

## Vector Databases

### FAISS

- 💻 https://github.com/facebookresearch/faiss

Facebook AI Similarity Search remains one of the most widely used vector indexing libraries.

---

### Milvus

- 💻 https://github.com/milvus-io/milvus

Cloud-native vector database designed for billion-scale similarity search.

---

### Weaviate

- 💻 https://github.com/weaviate/weaviate

Open-source vector database with hybrid retrieval and knowledge graph capabilities.

---

### Qdrant

- 💻 https://github.com/qdrant/qdrant

High-performance vector search engine optimized for semantic search applications.

---

### Pinecone

- 🌐 https://www.pinecone.io/

Managed vector database widely adopted in production RAG deployments.

---

### Chroma

- 💻 https://github.com/chroma-core/chroma

Lightweight open-source embedding database popular for rapid RAG prototyping.

---

## Document Retrieval

### Unstructured

- 💻 https://github.com/Unstructured-IO/unstructured

Open-source library for parsing PDFs, Word documents, HTML, PowerPoint, and enterprise documents into structured chunks.

`Document Analysis`

---

## Knowledge Retrieval

### HyDE

- 📄 https://arxiv.org/abs/2212.10496

Hypothetical Document Embeddings improve retrieval by generating synthetic documents before searching.

`Dense Retrieval`

---

## Retrieval-Augmented Reasoning & Agents

### Atlas

- 📄 Paper: https://arxiv.org/abs/2208.03299
- 💻 Code: https://github.com/facebookresearch/atlas

Meta's retrieval-augmented seq2seq model that jointly pretrains a dense retriever and an encoder-decoder LM, reaching strong few-shot performance on knowledge-intensive tasks with far fewer parameters than comparable LLMs.

`Retrieval LM` `Few-Shot`

---

### ReAct

- 📄 Paper: https://arxiv.org/abs/2210.03629
- 💻 Code: https://github.com/ysymyth/ReAct

Interleaves reasoning traces with actions (including retrieval/search calls), becoming a foundational pattern for tool-using and retrieval agents.

`Agentic Retrieval` `Tool Use`

---

### IRCoT

- 📄 Paper: https://arxiv.org/abs/2212.10509
- 💻 Code: https://github.com/StonyBrookNLP/ircot

Interleaves Chain-of-Thought reasoning with retrieval for multi-step, knowledge-intensive QA, alternating between generating reasoning steps and retrieving supporting paragraphs.

`Multi-hop Retrieval` `Chain-of-Thought`

---

## Evaluation

### MTEB

- 📄 https://arxiv.org/abs/2210.07316

- 💻 https://github.com/embeddings-benchmark/mteb

Massive benchmark evaluating embedding models across retrieval, clustering, reranking, and semantic search tasks.

---

## Notable 2022 Trends

- Emergence of complete RAG application frameworks.
- Rapid adoption of vector databases.
- Declarative retrieval pipelines.
- Improved document parsing.
- Embedding benchmarks became standardized.
- Transition from retrieval research toward production-ready retrieval ecosystems.
- Early interleaving of reasoning and retrieval/tool-use (ReAct, IRCoT) foreshadowed the agentic retrieval systems that matured in 2023–2025.

---

# 🗓️ 2023

The year 2023 marked the explosive adoption of **Retrieval-Augmented Generation (RAG)** following the widespread deployment of foundation models such as GPT-4 and Llama 2. During this period, retrieval evolved from a research topic into a core production architecture, accompanied by rapid growth in evaluation frameworks, agentic workflows, and long-context retrieval methods.

---

## 📚 Surveys

- **[Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)** – One of the earliest comprehensive surveys covering RAG architectures, indexing, retrieval strategies, generation methods, and future research directions. `Survey` `RAG`

- **[Augmented Language Models: A Survey](https://arxiv.org/abs/2302.07842)** – Reviews retrieval augmentation, tool use, memory, and external knowledge integration for language models. `Survey`

---

## RAG Systems & Frameworks

### LangChain

- 📄 https://python.langchain.com/docs/
- 💻 https://github.com/langchain-ai/langchain

The most widely adopted framework for building LLM applications with retrieval, memory, tools, and agents.

`Framework` `RAG`

---

### LlamaIndex

- 📄 https://docs.llamaindex.ai/
- 💻 https://github.com/run-llama/llama_index

Expanded into a complete data framework supporting ingestion, indexing, retrieval, graph indexes, and structured data.

`RAG`

---

### Haystack 2.0

- 📄 https://haystack.deepset.ai/

- 💻 https://github.com/deepset-ai/haystack

Introduced modular pipelines with native support for modern LLMs, hybrid retrieval, and production deployment.

`Framework`

---

### DSPy

- 📄 https://arxiv.org/abs/2310.03714

- 💻 https://github.com/stanfordnlp/dspy

A programming framework that optimizes prompts and retrieval pipelines declaratively rather than through manual prompt engineering.

`Programming Framework` `Retrieval`

---

## Advanced Retrieval

### Self-RAG

- 📄 https://arxiv.org/abs/2310.11511

- 💻 https://github.com/AkariAsai/self-rag

Introduced adaptive retrieval where the model decides **when**, **what**, and **how much** information to retrieve during generation.

`Self-RAG`

---

### Rewrite-Retrieve-Read

- 📄 https://arxiv.org/abs/2305.14283

Improves retrieval quality through automatic query rewriting before document retrieval.

`Query Rewriting`

---

### HyDE

- 📄 https://arxiv.org/abs/2212.10496

Continued gaining popularity as an effective retrieval enhancement strategy through hypothetical document generation.

---

### REPLUG

- 📄 Paper: https://arxiv.org/abs/2301.12652

Treats the LM as a frozen black box and prepends retrieved documents to the input, using LM feedback to tune the retriever — enabling retrieval augmentation without modifying the underlying model.

`Dense Retrieval` `Black-Box LM`

---

### FLARE (Forward-Looking Active Retrieval)

- 📄 Paper: https://arxiv.org/abs/2305.06983
- 💻 Code: https://github.com/jzbjyb/FLARE

Actively decides when and what to retrieve during long-form generation by using a low-confidence prediction of the next sentence as a retrieval query.

`Active Retrieval`

---

### StructGPT

- 📄 Paper: https://arxiv.org/abs/2305.09645
- 💻 Code: https://github.com/RUCAIBox/StructGPT

General Iterative Reading-then-Reasoning framework letting LLMs invoke specialized interfaces to reason over structured data (knowledge graphs, tables, databases).

`Structured Retrieval`

---

### Think-on-Graph (ToG)

- 📄 Paper: https://arxiv.org/abs/2307.07697
- 💻 Code: https://github.com/GasolSun36/ToG

LLM agent that performs beam search directly over a knowledge graph, iteratively exploring entities/relations to build responsible, explainable multi-hop reasoning paths.

`Knowledge Graph` `Multi-hop Retrieval`

---

### Chain-of-Note

- 📄 Paper: https://arxiv.org/abs/2311.09210

Generates sequential reading notes for each retrieved document before answering, improving robustness to noisy/irrelevant retrieved context.

`Robustness`

---

### MemGPT

- 📄 Paper: https://arxiv.org/abs/2310.08560
- 💻 Code: https://github.com/letta-ai/letta

Manages tiered memory (in-context + external storage) for LLM agents, borrowing virtual memory paging concepts from operating systems; later evolved into the Letta framework.

`Agent Memory`

---

## Document & Enterprise RAG

### Unstructured

- 💻 https://github.com/Unstructured-IO/unstructured

Continued to become one of the standard document ingestion libraries for enterprise RAG systems.

---

### LlamaParse

- 🌐 https://www.llamaindex.ai/llamaparse

Document parsing service optimized for PDFs, tables, forms, and enterprise documents.

`Document Parsing`

---

### Apache Tika

- 💻 https://github.com/apache/tika

Widely used document extraction framework integrated into numerous enterprise retrieval pipelines.

---

### Onyx (formerly Danswer)

- 💻 https://github.com/onyx-dot-app/onyx

Open-source enterprise search and AI assistant connecting to 40+ data sources (Slack, Confluence, Google Drive, etc.) with hybrid search, reranking, and knowledge-graph-backed Q&A.

`Enterprise RAG`

---

## Multimodal Retrieval

### CLIP

- 📄 https://arxiv.org/abs/2103.00020

- 💻 https://github.com/openai/CLIP

Although introduced earlier, CLIP became a foundational component for multimodal retrieval systems integrated with LLMs.

`Vision`

---

### BLIP-2

- 📄 https://arxiv.org/abs/2301.12597

Provides efficient vision-language representations for multimodal retrieval and question answering.

---

### LLaVA

- 📄 https://arxiv.org/abs/2304.08485

- 💻 https://github.com/haotian-liu/LLaVA

Popular multimodal LLM architecture frequently incorporated into multimodal RAG pipelines.

---

## Agentic Retrieval

### AutoGen

- 📄 https://arxiv.org/abs/2308.08155

- 💻 https://github.com/microsoft/autogen

Introduced collaborative multi-agent workflows where specialized agents retrieve information and cooperate during reasoning.

`Agent`

---

### CrewAI

- 💻 https://github.com/crewAIInc/crewAI

Multi-agent orchestration framework frequently used for retrieval planning and enterprise assistants.

---

### MetaGPT

- 💻 https://github.com/FoundationAgents/MetaGPT

Agent framework emphasizing collaborative software engineering and tool-augmented retrieval.

---

### Microsoft Semantic Kernel

- 💻 https://github.com/microsoft/semantic-kernel

Model-agnostic SDK (C#/Python/Java) for integrating LLMs with conventional code via plugins, planners, and memory — Microsoft's alternative to LangChain-style orchestration.

`Framework` `Agent`

---

## Vector Databases

### Milvus

https://github.com/milvus-io/milvus

Continued rapid adoption for production-scale vector search.

---

### Weaviate

https://github.com/weaviate/weaviate

Expanded support for hybrid search and multimodal indexing.

---

### Qdrant

https://github.com/qdrant/qdrant

Introduced additional filtering, payload indexing, and scalable retrieval capabilities.

---

### Pinecone

https://www.pinecone.io/

Managed vector database widely adopted in commercial RAG systems.

---

### Chroma

https://github.com/chroma-core/chroma

Popular lightweight vector database for experimentation and local development.

---

### LanceDB

https://github.com/lancedb/lancedb

Modern vector database built on Apache Arrow with efficient local storage.

---

### pgvector

- 💻 https://github.com/pgvector/pgvector

Open-source PostgreSQL extension adding vector similarity search (exact and HNSW/IVFFlat approximate) directly inside Postgres — widely used to add RAG retrieval to existing relational stacks.

`Vector Database` `Postgres`

---

### Redis (Vector Search)

- 🌐 https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/

Redis Stack's vector search adds HNSW/flat vector indexing and hybrid queries on top of Redis's in-memory data structures, commonly used for low-latency RAG caching + retrieval.

`Vector Database` `Hybrid Search`

---

### MongoDB Atlas Vector Search

- 🌐 https://www.mongodb.com/products/platform/atlas-vector-search

Native vector search integrated into MongoDB Atlas, allowing vector and operational/document data to be queried together in a single database.

`Vector Database`

---

### txtai

- 💻 https://github.com/neuml/txtai

All-in-one embeddings database unifying vector indexes, graph networks, and relational storage for semantic search and LLM orchestration workflows.

`Framework` `Vector Database`

---

## 📊 Evaluation & Benchmarks

### RAGAS

- 📄 https://arxiv.org/abs/2309.15217

- 💻 https://github.com/explodinggradients/ragas

Introduced automated evaluation metrics including faithfulness, context precision, context recall, and answer relevance.

`Evaluation`

---

### TruLens

- 💻 https://github.com/truera/trulens

Framework for evaluating groundedness, hallucinations, and retrieval quality in production RAG systems.

---

### DeepEval

- 💻 https://github.com/confident-ai/deepeval

Open-source evaluation toolkit for LLMs supporting retrieval-specific metrics and regression testing.

---

### BEIR

https://github.com/beir-cellar/beir

Remained one of the most important retrieval benchmarks for embedding models.

---

### MTEB

https://github.com/embeddings-benchmark/mteb

Standard benchmark for evaluating retrieval embeddings across diverse tasks.

---

### RGB (Retrieval-Augmented Generation Benchmark)

- 📄 Paper: https://arxiv.org/abs/2309.01431

Evaluates LLMs on four core RAG abilities — noise robustness, negative rejection, information integration, and counterfactual robustness — in English and Chinese.

`Benchmark`

---

### LongBench

- 📄 Paper: https://arxiv.org/abs/2308.14508
- 💻 Code: https://github.com/THUDM/LongBench

First bilingual, multi-task benchmark for long-context understanding (21 datasets across 6 task categories), widely used to evaluate long-context retrieval and RAG pipelines.

`Benchmark` `Long-Context`

---

### Giskard

- 💻 https://github.com/Giskard-AI/giskard-oss

Open-source scanning/testing library for LLM agents and RAG pipelines that automatically detects vulnerabilities such as hallucination, prompt injection, and bias.

`Evaluation` `Red Teaming`

---

### Arize Phoenix

- 💻 https://github.com/Arize-ai/phoenix

Open-source LLM observability platform providing OpenTelemetry-based tracing, RAG-specific evaluations, and dataset/experiment management, runnable locally or at scale.

`Observability` `Evaluation`

---

### Langfuse

- 💻 https://github.com/langfuse/langfuse

Open-source LLM engineering platform combining tracing, evaluation, prompt management, and datasets — commonly used to observe and debug production RAG/agent pipelines.

`Observability`

---

## 🔢 Embedding Models

### BGE

- 📄 Paper: https://arxiv.org/abs/2309.07597 ("C-Pack: Packed Resources For General Chinese Embeddings")
- 💻 Code: https://github.com/FlagOpen/FlagEmbedding

High-performing embedding models (BAAI General Embedding) that quickly became the default choice for many RAG systems.

---

### E5

- 📄 https://arxiv.org/abs/2212.03533

Embedding family optimized for retrieval tasks through weakly supervised contrastive learning.

---

### Instructor

- 📄 https://arxiv.org/abs/2212.09741

Instruction-tuned embeddings designed for retrieval and semantic search.

---

### Voyage AI Embeddings

- 🌐 https://docs.voyageai.com/docs/embeddings

Commercial embedding and reranking API with models tuned for retrieval quality (query/document-aware `input_type`) and multimodal (text + image) embeddings.

`Embedding Model` `Commercial`

---

## Major Trends in 2023

- Explosion of production RAG systems
- Emergence of retrieval evaluation frameworks
- Rise of agent-based retrieval workflows
- Hybrid retrieval became mainstream
- Better document parsing pipelines
- Knowledge graph retrieval gained renewed interest
- Stronger embedding models dramatically improved retrieval quality
- Foundation for GraphRAG research established

---

# 🗓️ 2024

The year **2024** marked a major shift from conventional vector-based Retrieval-Augmented Generation (RAG) toward **graph-aware**, **reasoning-centric**, and **agentic retrieval systems**. Large organizations and the research community introduced frameworks that organize documents into structured knowledge representations, improve long-context reasoning, and support multimodal enterprise retrieval.

---

## 📚 Surveys

- **[Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)** – One of the most comprehensive surveys covering RAG architectures, indexing, retrieval strategies, generation, and evaluation. `Survey` `RAG`

- **[Graph Retrieval-Augmented Generation: A Survey](https://arxiv.org/abs/2408.08921)** – Systematic review of GraphRAG methods, covering graph-based indexing, retrieval, and generation techniques and their advantages over purely vector-based RAG. `GraphRAG` `Survey`

- **[A Survey on Retrieval-Augmented Text Generation for Large Language Models](https://arxiv.org/abs/2404.10981)** – Reviews the evolution from Naive RAG to Advanced and Modular RAG, covering retrieval, generation, and augmentation techniques. `Survey`

---

# 🧠 RAG Systems & Frameworks

### GraphRAG (Microsoft)

- 📄 Paper: https://arxiv.org/abs/2404.16130
- 💻 Code: https://github.com/microsoft/graphrag

Microsoft's GraphRAG automatically extracts entities and relationships from large document collections, constructs a knowledge graph, detects communities, and performs graph-guided retrieval for global and local question answering.

`GraphRAG` `Knowledge Graph` `Enterprise`

---

### LightRAG

- 📄 Paper: https://arxiv.org/abs/2410.05779
- 💻 Code: https://github.com/HKUDS/LightRAG

A lightweight graph-based retrieval framework that combines graph indexing with efficient retrieval while minimizing indexing cost.

`GraphRAG`

---

### RAPTOR

- 📄 Paper: https://arxiv.org/abs/2401.18059
- 💻 Code: https://github.com/parthsarthi03/raptor

Builds hierarchical retrieval trees through recursive clustering and summarization, enabling retrieval across multiple semantic abstraction levels.

`Hierarchical RAG`

---

### FlashRAG

- 📄 Paper: https://arxiv.org/abs/2405.13576
- 💻 Code: https://github.com/RUC-NLPIR/FlashRAG

Research-oriented toolkit for developing, comparing, and benchmarking Retrieval-Augmented Generation pipelines.

`Framework`

---

### FastRAG

- 💻 https://github.com/IntelLabs/fastRAG

Intel's modular framework for building efficient production-grade RAG applications with optimized inference pipelines.

`Framework`

---

### Pathway

- 💻 https://github.com/pathwaycom/pathway

Streaming data processing framework supporting continuously updated retrieval indexes for real-time RAG applications.

`Streaming`

---

### R2R

- 💻 https://github.com/SciPhi-AI/R2R

Production-ready, agentic RAG engine with a RESTful API bundling hybrid search, knowledge-graph extraction, multimodal ingestion, and app/user management.

`Framework` `Agentic`

---

### RAGFlow

- 💻 https://github.com/infiniflow/ragflow

Open-source RAG engine built around deep document understanding, with visualized chunking, traceable citations, and configurable retrieval/reranking pipelines.

`Framework` `Document Analysis`

---

## Advanced Retrieval & RAG Papers

### Corrective RAG (CRAG)

- 📄 Paper: https://arxiv.org/abs/2401.15884
- 💻 Code: https://github.com/HuskyInSalt/CRAG

Adds a lightweight retrieval evaluator that grades retrieved documents and triggers corrective actions (web search fallback, knowledge refinement) when retrieval confidence is low.

`Self-Correction`

---

### Adaptive-RAG

- 📄 Paper: https://arxiv.org/abs/2403.14403
- 💻 Code: https://github.com/starsuzi/Adaptive-RAG

Trains a lightweight query-complexity classifier to dynamically route queries between no-retrieval, single-step, and multi-step retrieval strategies.

`Query Routing`

---

### RQ-RAG

- 📄 Paper: https://arxiv.org/abs/2404.00610
- 💻 Code: https://github.com/chanchimin/RQ-RAG

Trains LLMs to explicitly rewrite, decompose, and disambiguate queries before retrieval, improving performance on ambiguous and multi-hop questions.

`Query Rewriting`

---

### RAFT (Retrieval-Augmented Fine-Tuning)

- 📄 Paper: https://arxiv.org/abs/2403.10131

Fine-tunes models to answer from retrieved context while learning to ignore irrelevant "distractor" documents, improving domain-specific open-book QA.

`Fine-Tuning`

---

### RankRAG

- 📄 Paper: https://arxiv.org/abs/2407.02485

Instruction-tunes a single LLM for both context ranking and answer generation, outperforming pipelines that use a separate expert reranker.

`Reranking`

---

### Speculative RAG

- 📄 Paper: https://arxiv.org/abs/2407.08223

Uses a smaller specialist LM to draft multiple answers from retrieved document subsets in parallel, which a larger generalist LM then verifies — reducing latency and hallucination.

`Efficiency`

---

### RAGTruth

- 📄 Paper: https://arxiv.org/abs/2401.00396
- 💻 Code: https://github.com/ParticleMedia/RAGTruth

Word-level hallucination corpus (~18K annotated LLM responses) for training and benchmarking hallucination-detection models in RAG settings.

`Benchmark` `Hallucination`

---

### CRUD-RAG

- 📄 Paper: https://arxiv.org/abs/2401.17043
- 💻 Code: https://github.com/IAAR-Shanghai/CRUD_RAG

Comprehensive Chinese RAG benchmark organized around Create/Read/Update/Delete task categories, evaluating retrieval and generation jointly.

`Benchmark`

---

### MultiHop-RAG

- 📄 Paper: https://arxiv.org/abs/2401.15391
- 💻 Code: https://github.com/yixuantt/MultiHop-RAG

Dataset and benchmark purpose-built for evaluating RAG systems on queries that require retrieving and reasoning over multiple supporting documents.

`Benchmark` `Multi-hop Retrieval`

---

### RULER

- 📄 Paper: https://arxiv.org/abs/2404.06654
- 💻 Code: https://github.com/NVIDIA/RULER

Synthetic long-context benchmark extending needle-in-a-haystack testing with multi-hop tracing and aggregation tasks, widely used to stress-test long-context retrieval claims.

`Benchmark` `Long-Context`

---

### RAGChecker

- 📄 Paper: https://arxiv.org/abs/2408.08067
- 💻 Code: https://github.com/amazon-science/RAGChecker

Claim-level, fine-grained diagnostic framework scoring both retrieval and generation modules separately, correlating better with human judgment than response-level metrics.

`Evaluation`

---

# 🌐 GraphRAG & Knowledge Graph Systems

### OpenSPG / KAG

- 📄 Paper: https://arxiv.org/abs/2409.13731
- 💻 Code: https://github.com/OpenSPG/KAG

Knowledge-Augmented Generation framework combining logical reasoning, ontology-guided retrieval, and knowledge graphs to address limitations of vector-only RAG.

`KAG` `Knowledge Graph`

---

### HippoRAG

- 📄 Paper: https://arxiv.org/abs/2405.14831
- 💻 Code: https://github.com/OSU-NLP-Group/HippoRAG

Constructs long-term graph memories that enable more reliable multi-hop reasoning over large document collections.

`Graph Memory`

---

### KG-RAG

- 📄 Paper: https://arxiv.org/abs/2405.12035

Uses a knowledge graph as external structured memory to ground LLM generation, bridging factual retrieval with creative/long-form text generation.

`Knowledge Graph`

---

### G-Retriever

- 📄 Paper: https://arxiv.org/abs/2402.07630
- 💻 Code: https://github.com/XiaoxinHe/G-Retriever
- 🌐 Proceedings: https://proceedings.neurips.cc/paper_files/paper/2024/hash/efaf1c9726648c8ba363a5c927440529-Abstract-Conference.html

Graph neural retrieval framework (NeurIPS 2024) combining GNNs, LLMs, and RAG to enable question answering over general textual graphs via soft prompting.

`Graph Retrieval`

---

### nano-graphrag

- 💻 https://github.com/gusye1234/nano-graphrag

A simple, easy-to-hack ~1,100-line reimplementation of GraphRAG's core functionality, designed for readability and rapid experimentation.

`GraphRAG` `Lightweight`

---

### GraphRAG-SDK (FalkorDB)

- 💻 https://github.com/FalkorDB/GraphRAG-SDK

Toolkit for building GraphRAG systems on FalkorDB with ontology management and multi-path retrieval (vector, full-text, Cypher, relationship expansion) combined via reranking.

`GraphRAG` `Framework`

---

### Cognee

- 💻 https://github.com/topoteretes/cognee

Open-source AI memory platform that continuously builds a self-hosted knowledge graph from ingested data, combining vector embeddings and graph reasoning for persistent agent memory.

`Graph Memory`

---

### Neo4j LLM Graph Builder

- 💻 https://github.com/neo4j-labs/llm-graph-builder

Turns unstructured text, PDFs, and web pages into a Neo4j knowledge graph (lexical + entity graph) using LLM-based extraction, then supports GraphRAG, vector, and Text2Cypher retrieval.

`Knowledge Graph` `Tooling`

---

### Kuzu

- 💻 https://github.com/kuzudb/kuzu

Embedded, in-process property graph database implementing Cypher with built-in vector and full-text indexes — used as a lightweight backend for GraphRAG pipelines.

`Graph Database`

---

# 📄 Multimodal & Document Analysis RAG

### Docling

- 💻 https://github.com/DS4SD/docling

IBM's document understanding toolkit supporting PDFs, Office documents, HTML, tables, OCR, and layout-aware parsing for enterprise RAG.

`Document Analysis`

---

### MinerU

- 💻 https://github.com/opendatalab/MinerU

State-of-the-art PDF parsing framework preserving layout, formulas, tables, figures, and reading order.

`PDF`

---

### ColPali

- 📄 Paper: https://arxiv.org/abs/2407.01449
- 💻 Code: https://github.com/illuin-tech/colpali

Vision-language retrieval model capable of retrieving document pages directly from screenshots without OCR.

`Vision Retrieval`

---

### Nougat

- 📄 Paper: https://arxiv.org/abs/2308.13418
- 💻 Code: https://github.com/facebookresearch/nougat

OCR-free document understanding model specialized for scientific PDFs.

---

### LlamaParse

- 🌐 https://www.llamaindex.ai/llamaparse

Advanced document parsing service supporting PDFs, spreadsheets, presentations, and enterprise documents.

---

### Unstructured

- 💻 https://github.com/Unstructured-IO/unstructured

Continued expansion into enterprise-scale document ingestion with improved layout-aware chunking.

---

### Marker

- 💻 https://github.com/datalab-to/marker

Converts PDFs (and Office/EPUB/HTML formats) to Markdown/JSON quickly and accurately, handling tables, forms, equations, and inline math with low hallucination risk.

`PDF` `Document Parsing`

---

### PyMuPDF4LLM

- 💻 https://github.com/pymupdf/pymupdf4llm

Lightweight PyMuPDF extension converting PDFs to structured Markdown/JSON optimized for RAG ingestion, preserving multi-column reading order and tables.

`PDF` `Document Parsing`

---

### Firecrawl

- 💻 https://github.com/firecrawl/firecrawl

API for turning entire websites into clean, LLM-ready Markdown or structured data — scrape, crawl, and search in one call, commonly used for web-RAG ingestion.

`Web RAG` `Crawling`

---

### Reducto

- 🌐 https://reducto.ai

Commercial agentic document platform performing layout-aware OCR and parsing on complex real-world files (tables, handwritten forms, mixed languages) for RAG pipelines.

`Document Parsing` `Commercial`

---

# 🤖 Agentic & Reasoning-Centric Retrieval

### AutoGen

- 📄 https://arxiv.org/abs/2308.08155
- 💻 https://github.com/microsoft/autogen

Multi-agent collaboration framework increasingly adopted for retrieval planning and autonomous information gathering.

`Agent`

---

### CrewAI

- 💻 https://github.com/crewAIInc/crewAI

Lightweight multi-agent orchestration platform supporting retrieval specialists and planning agents.

---

### LangGraph

- 💻 https://github.com/langchain-ai/langgraph

Graph-based orchestration framework enabling stateful retrieval workflows, branching logic, and agent memory.

`Agent`

---

### OpenDevin

- 💻 https://github.com/OpenDevin/OpenDevin

Open-source autonomous software engineering agent utilizing retrieval for coding and documentation tasks.

---

### CAMEL-AI

- 💻 https://github.com/camel-ai/camel

Framework for cooperative autonomous agents frequently used in retrieval-enhanced workflows.

---

### AG2 (AutoGen community fork)

- 💻 https://github.com/ag2ai/ag2

Community-governed continuation of AutoGen's v0.2 API line, maintained by AutoGen's original creators under open governance after Microsoft's v0.4 rewrite.

`Agent` `Multi-Agent`

---

### OpenAI Swarm

- 💻 https://github.com/openai/swarm

Educational, lightweight multi-agent orchestration framework introducing "routines" and "handoffs" as minimal abstractions for agent coordination.

`Agent` `Multi-Agent`

---

# 🗄️ Vector Databases & Retrieval Infrastructure

### Milvus

https://github.com/milvus-io/milvus

Scalable cloud-native vector database supporting billion-scale similarity search.

---

### Weaviate

https://github.com/weaviate/weaviate

Hybrid vector database supporting semantic search and knowledge graph integration.

---

### Qdrant

https://github.com/qdrant/qdrant

High-performance vector search engine supporting payload filtering and hybrid retrieval.

---

### Pinecone

https://www.pinecone.io/

Managed vector database widely deployed in commercial RAG systems.

---

### LanceDB

https://github.com/lancedb/lancedb

Vector database optimized for local analytics and Apache Arrow integration.

---

### Chroma

https://github.com/chroma-core/chroma

Developer-friendly embedding database for rapid experimentation.

---

### Vespa

https://github.com/vespa-engine/vespa

Large-scale serving engine supporting hybrid search, ranking, and recommendation.

---

### turbopuffer

- 🌐 https://turbopuffer.com

Serverless vector + full-text search database built directly on object storage (S3/GCS), offering BM25 + vector hybrid search with tiered NVMe/memory caching.

`Vector Database` `Serverless`

---

### DuckDB VSS

- 💻 https://github.com/duckdb/duckdb-vss

Vector Similarity Search extension for DuckDB, adding HNSW-indexed nearest-neighbor search to the embedded analytical database for local/offline RAG pipelines.

`Vector Database` `Embedded`

---

# 📊 Evaluation & Benchmarks

### RAGAS

- 📄 https://arxiv.org/abs/2309.15217
- 💻 https://github.com/explodinggradients/ragas

Industry-standard evaluation toolkit measuring faithfulness, answer relevance, context precision, and retrieval quality.

`Evaluation`

---

### TruLens

- 💻 https://github.com/truera/trulens

Evaluation framework for measuring groundedness, hallucinations, and retrieval effectiveness.

---

### DeepEval

- 💻 https://github.com/confident-ai/deepeval

Regression testing and evaluation toolkit for LLM applications and RAG systems.

---

### ARES

- 📄 https://arxiv.org/abs/2311.09476
- 💻 https://github.com/stanford-futuredata/ARES

Automatic evaluation framework for retrieval systems using LLM judges.

---

### Comet Opik

- 💻 https://github.com/comet-ml/opik

Open-source LLM observability and evaluation platform (Apache-2.0) offering distributed tracing, LLM-as-judge metrics, prompt management, and CI/CD evaluation for RAG/agent pipelines.

`Observability` `Evaluation`

---

# 🔢 Embedding Models

### BGE-M3

- 📄 https://arxiv.org/abs/2402.03216
- 💻 https://github.com/FlagOpen/FlagEmbedding

Unified embedding model supporting dense retrieval, sparse retrieval, and multi-vector retrieval.

---

### Nomic Embed

- 💻 https://github.com/nomic-ai/nomic

Open embedding models supporting retrieval across long documents.

---

### Jina Embeddings v3

- 📄 Paper: https://arxiv.org/abs/2409.10173
- 🌐 https://jina.ai/models/jina-embeddings-v3/

570M-parameter multilingual, multi-task embedding model with task-specific LoRA adapters and Matryoshka representation learning for flexible-dimension retrieval.

`Embedding Model` `Multilingual`

---

### Snowflake Arctic Embed

- 💻 https://github.com/Snowflake-Labs/arctic-embed

Suite of retrieval-optimized text embedding models (22M–large parameter sizes) achieving state-of-the-art MTEB/BEIR results for their size class.

`Embedding Model`

---

# 📈 Major Trends in 2024

- Microsoft popularized **GraphRAG** as a practical architecture for enterprise knowledge retrieval.
- Knowledge graphs re-emerged as a central retrieval structure through GraphRAG and KAG.
- Hierarchical retrieval (e.g., RAPTOR) improved long-document reasoning.
- Multimodal document understanding advanced rapidly with Docling, MinerU, ColPali, and Nougat.
- Agentic retrieval frameworks became production-ready with LangGraph, CrewAI, and AutoGen.
- Evaluation frameworks matured with RAGAS, ARES, CRUD-RAG, and RGB.
- Hybrid retrieval (dense + sparse + graph) became the dominant architecture for production RAG systems.
- Long-context embeddings and structured retrieval pipelines significantly improved enterprise search.
- A wave of RAG failure-mode papers (CRAG, Adaptive-RAG, RAFT, Speculative RAG) targeted robustness, latency, and hallucination rather than raw retrieval accuracy.
- Purpose-built RAG observability/evaluation platforms (Comet Opik, Arize Phoenix, Langfuse) became standard alongside RAGAS/ARES.

---

# 🗓️ 2025

By 2025, retrieval systems increasingly evolved toward **agentic retrieval**, **reasoning-centric workflows**, **graph-native memory architectures**, and **deep research systems**. The focus shifted from simple retrieval pipelines toward autonomous systems capable of planning, iterative search, tool usage, reflection, and long-horizon reasoning.

Many organizations began treating retrieval not as a standalone component but as part of a larger cognitive architecture involving memory, planning, and structured knowledge representations. GraphRAG and knowledge-centric retrieval continued to mature, while evaluation and observability became critical production requirements. GraphRAG also became one of the dominant retrieval paradigms for enterprise knowledge systems.

---

# 📚 Surveys

### RAG vs. GraphRAG

- 📄 https://arxiv.org/abs/2502.11371

Systematic evaluation comparing traditional retrieval pipelines against graph-based retrieval architectures.

`GraphRAG`

---

### Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

- 📄 https://arxiv.org/abs/2501.09136

Comprehensive survey of Agentic RAG, taxonomizing architectures that embed autonomous agents (reflection, planning, tool use, multi-agent collaboration) into the retrieval pipeline.

`Agentic`

---

### A Survey of Graph Retrieval-Augmented Generation for Customized Large Language Models

- 📄 https://arxiv.org/abs/2501.13958

Reviews knowledge-graph-augmented generation approaches, covering graph construction, retrieval, and customization strategies for domain-specific LLMs.

`KAG` `GraphRAG`

---

# 🔬 Agentic Retrieval & Deep Research

### OpenAI Deep Research

- 🌐 https://openai.com

Research-oriented autonomous retrieval system capable of iterative search, synthesis, and multi-step reasoning.

`Agentic Retrieval`

---

### AutoGen

- 📄 https://arxiv.org/abs/2308.08155
- 💻 https://github.com/microsoft/autogen

Continued adoption as one of the leading multi-agent orchestration frameworks for retrieval planning and tool usage.

`Multi-Agent`

---

### CrewAI

- 💻 https://github.com/crewAIInc/crewAI

Multi-agent framework widely used for enterprise retrieval workflows and task delegation.

`Agent`

---

### LangGraph

- 💻 https://github.com/langchain-ai/langgraph

Stateful graph-based orchestration framework supporting long-running retrieval workflows and agent memory.

`Agent`

---

### OpenHands (formerly OpenDevin)

- 💻 https://github.com/All-Hands-AI/OpenHands

Open-source autonomous software engineering agent heavily leveraging retrieval and tool use.

`Agent`

---

### CAMEL-AI

- 💻 https://github.com/camel-ai/camel

Multi-agent ecosystem supporting collaborative retrieval and reasoning.

---

### smolagents

- 💻 https://github.com/huggingface/smolagents

Hugging Face's barebones (~1,000 LOC) agent library where agents write actions in code rather than JSON tool calls, with sandboxed execution and model-agnostic LLM support.

`Agent` `Lightweight`

---

### Agno (formerly Phidata)

- 💻 https://github.com/agno-agi/agno

High-performance agent runtime for building, running, and managing agent platforms, emphasizing fast agent instantiation and low memory overhead over graph/chain abstractions.

`Agent` `Framework`

---

### PydanticAI

- 💻 https://github.com/pydantic/pydantic-ai

Type-safe, model-agnostic Python agent framework from the Pydantic team, combining structured response validation with dependency injection for retrieval tools and data sources.

`Agent` `Framework`

---

# 🧠 GraphRAG & Graph Memory

### Microsoft GraphRAG

- 📄 https://arxiv.org/abs/2404.16130
- 💻 https://github.com/microsoft/graphrag

Remained one of the most influential graph-based retrieval architectures, enabling entity extraction, community detection, and graph-guided reasoning.

`GraphRAG`

---

### LightRAG

- 📄 https://arxiv.org/abs/2410.05779
- 💻 https://github.com/HKUDS/LightRAG

Focused on reducing graph construction and maintenance costs while preserving retrieval quality.

`GraphRAG`

---

### HippoRAG

- 📄 https://arxiv.org/abs/2405.14831
- 💻 https://github.com/OSU-NLP-Group/HippoRAG

Graph memory architecture supporting associative retrieval and multi-hop reasoning.

`Memory`

---

### Graphiti

- 💻 https://github.com/getzep/graphiti

Temporal knowledge graph memory framework designed for continuously evolving information.

`Graph Memory`

---

### ArchRAG

- 📄 https://arxiv.org/abs/2502.09891

Attributed community-based hierarchical GraphRAG architecture extending Microsoft's GraphRAG design.

`GraphRAG`

---

### Zep

- 📄 Paper: https://arxiv.org/abs/2501.13956
- 🌐 https://www.getzep.com

Context engineering / agent-memory platform built on a bi-temporal knowledge graph (powered by the open-source Graphiti engine) that tracks when facts were true and when they were learned.

`Graph Memory` `Agent Memory`

---

### Mem0

- 📄 Paper: https://arxiv.org/abs/2504.19413
- 💻 Code: https://github.com/mem0ai/mem0

Universal, scalable memory layer for AI agents that extracts, consolidates, and retrieves key conversational facts; includes a graph-based variant (Mem0g) modeling entity relationships.

`Agent Memory`

---

### Letta (formerly MemGPT)

- 💻 https://github.com/letta-ai/letta

Platform for building stateful agents with transparent, tiered long-term memory that persists and improves across sessions; the production evolution of the MemGPT research project.

`Agent Memory` `Framework`

---

# 🧩 Knowledge-Augmented Generation (KAG)

### OpenSPG/KAG

- 📄 https://arxiv.org/abs/2409.13731
- 💻 https://github.com/OpenSPG/KAG

Continued development of ontology-aware retrieval and logical-form-guided reasoning over enterprise knowledge graphs.

`KAG`

---

### Neo4j GraphRAG

- 💻 https://github.com/neo4j/neo4j-graphrag-python

Production-oriented GraphRAG toolkit built around Neo4j graph databases.

`Knowledge Graph`

---

### Memgraph GraphRAG

- 🌐 https://memgraph.com

Graph-native retrieval workflows integrating graph traversal and semantic retrieval.

`Graph Database`

---

# 🏢 Multimodal & Enterprise Retrieval

### Docling

- 💻 https://github.com/DS4SD/docling

One of the most widely adopted document understanding frameworks for enterprise retrieval.

`PDF`

---

### MinerU

- 💻 https://github.com/opendatalab/MinerU

Advanced parsing system for scientific documents, formulas, tables, and layout-aware extraction.

`Document Intelligence`

---

### ColPali

- 📄 https://arxiv.org/abs/2407.01449
- 💻 https://github.com/illuin-tech/colpali

Vision-language retrieval model supporting direct document image retrieval.

`Multimodal`

---

### LlamaParse

- 🌐 https://www.llamaindex.ai/llamaparse

Enterprise document parsing platform integrated with RAG workflows.

---

# 🛠️ Retrieval Frameworks

### LlamaIndex

- 💻 https://github.com/run-llama/llama_index

Expanded support for graph indexes, structured retrieval, agent workflows, and multimodal retrieval.

`Framework`

---

### LangChain

- 💻 https://github.com/langchain-ai/langchain

Continued to serve as a major orchestration layer for retrieval systems.

---

### Haystack

- 💻 https://github.com/deepset-ai/haystack

Production retrieval framework with strong support for hybrid retrieval and evaluation.

---

### DSPy

- 📄 https://arxiv.org/abs/2310.03714
- 💻 https://github.com/stanfordnlp/dspy

Increasingly used to optimize retrieval pipelines and retrieval-aware reasoning programs.

---

### FlashRAG

- 💻 https://github.com/RUC-NLPIR/FlashRAG

Popular benchmarking and experimentation platform for RAG research.

---

# 📡 Evaluation & Observability

### RAGAS

- 📄 https://arxiv.org/abs/2309.15217
- 💻 https://github.com/explodinggradients/ragas

Industry-standard evaluation framework for RAG systems.

---

### ARES

- 📄 https://arxiv.org/abs/2311.09476
- 💻 https://github.com/stanford-futuredata/ARES

Automatic retrieval evaluation using LLM judges.

---

### TruLens

- 💻 https://github.com/truera/trulens

Evaluation framework measuring groundedness and retrieval quality.

---

### DeepEval

- 💻 https://github.com/confident-ai/deepeval

Regression testing framework for retrieval pipelines.

---

### LangSmith

- 🌐 https://smith.langchain.com

Observability platform supporting tracing and debugging of retrieval workflows.

---

# 🗄️ Vector Databases & Retrieval Infrastructure

### Qdrant

- 💻 https://github.com/qdrant/qdrant

---

### Weaviate

- 💻 https://github.com/weaviate/weaviate

---

### Milvus

- 💻 https://github.com/milvus-io/milvus

---

### Pinecone

- 🌐 https://www.pinecone.io

---

### LanceDB

- 💻 https://github.com/lancedb/lancedb

---

### Vespa

- 💻 https://github.com/vespa-engine/vespa

---

# 📈 Major Trends in 2025

- Agentic retrieval became mainstream.
- Retrieval planning replaced single-shot retrieval.
- Deep Research systems demonstrated long-horizon retrieval workflows.
- GraphRAG matured into production deployments; **LazyGraphRAG** showed that graph-quality answers are achievable at near-vector-RAG indexing cost by deferring graph summarization to query time.
- Knowledge graph retrieval experienced renewed adoption.
- Retrieval observability and evaluation became mandatory in enterprise environments.
- Multimodal retrieval increasingly supported PDFs, tables, images, and scientific documents.
- Memory-centric architectures emerged as a major research direction, with dedicated agent-memory products (Zep, Mem0, Letta, Cognee) competing alongside DIY graph-memory stacks.
- Graph memory systems such as HippoRAG and Graphiti expanded retrieval beyond vector search alone.
- Lightweight, code-first agent frameworks (smolagents, PydanticAI, Agno) gained adoption as leaner alternatives to heavier orchestration graphs for retrieval agents.

---

# 🔮 2026

The retrieval ecosystem continues to evolve toward **persistent memory**, **continual retrieval**, **graph-native reasoning**, **agentic knowledge systems**, and **retrieval-aware foundation models**. Many directions remain active research areas, and this section should be updated regularly.

---

## Emerging Directions

### Persistent Agent Memory

- Long-term memory systems for autonomous agents.
- Retrieval over episodic memories.
- Temporal knowledge graphs.
- Lifelong retrieval.

`Memory`

---

### Graph-Native Agents

- Agents operating directly over knowledge graphs.
- Dynamic graph expansion during retrieval.
- Retrieval-aware planning.

`Graph Agents`

---

### Continual Retrieval

- Incremental indexing.
- Streaming retrieval.
- Real-time graph updates.
- Live knowledge integration.

`Streaming`

---

### Structured Reasoning Retrieval

- Logical retrieval.
- Ontology-aware retrieval.
- Neuro-symbolic retrieval.
- Tool-grounded reasoning.

`KAG`

---

## Representative Systems

### GraphRAG

- 📄 https://arxiv.org/abs/2404.16130
- 💻 https://github.com/microsoft/graphrag

Continues to influence graph-based retrieval research and production deployments.

---

### HippoRAG

- 📄 https://arxiv.org/abs/2405.14831
- 💻 https://github.com/OSU-NLP-Group/HippoRAG

Frequently used as a foundation for graph memory research.

---

### Graphiti

- 💻 https://github.com/getzep/graphiti

Temporal graph memory supporting dynamic information updates.

---

### LangGraph

- 💻 https://github.com/langchain-ai/langgraph

Stateful execution framework for long-running retrieval agents.

---

## Research Themes

- Retrieval-aware foundation models.
- Structured memory architectures.
- Long-context retrieval.
- Graph-native reasoning.
- Autonomous research agents.
- Continual learning with retrieval.
- Dynamic GraphRAG.
- Enterprise-scale knowledge orchestration.

---

# 📄 Document & Web RAG

Document-centric Retrieval-Augmented Generation focuses on extracting, indexing, retrieving, and reasoning over unstructured and semi-structured content such as PDFs, Office documents, HTML pages, scientific papers, technical manuals, and enterprise knowledge bases. Modern document pipelines increasingly preserve document structure (e.g., layout, tables, figures, and formulas) to improve retrieval quality and downstream generation.

## Representative Frameworks

| Project | Repository | Focus |
|---------|------------|-------|
| **Docling** | https://github.com/DS4SD/docling | Enterprise document parsing and layout-aware extraction |
| **MinerU** | https://github.com/opendatalab/MinerU | Scientific PDF parsing |
| **Unstructured** | https://github.com/Unstructured-IO/unstructured | Universal document ingestion |
| **LlamaParse** | https://www.llamaindex.ai/llamaparse | High-quality document parsing service |
| **Apache Tika** | https://github.com/apache/tika | Metadata and content extraction |
| **Nougat** | https://github.com/facebookresearch/nougat | OCR-free scientific document parsing |
| **Marker** | https://github.com/datalab-to/marker | Fast, accurate PDF → Markdown/JSON conversion |
| **PyMuPDF4LLM** | https://github.com/pymupdf/pymupdf4llm | PDF → structured Markdown for RAG ingestion |
| **Firecrawl** | https://github.com/firecrawl/firecrawl | Website → LLM-ready Markdown scraping/crawling |
| **Reducto** | https://reducto.ai | Commercial layout-aware document parsing API |
| **RAGFlow** | https://github.com/infiniflow/ragflow | Deep-document-understanding RAG engine |

Typical pipeline:

```text
Documents
      │
      ▼
Parsing
      │
      ▼
Chunking
      │
      ▼
Embedding
      │
      ▼
Vector Store
      │
      ▼
Retriever
      │
      ▼
LLM
```

---

# 🕸️ Knowledge Graph / GraphRAG / KAG

Graph-based retrieval enriches traditional vector search by explicitly modeling entities, relationships, communities, and structured knowledge. These systems are particularly effective for multi-hop reasoning, enterprise search, and long-context applications where relational information is critical.

## Representative Projects

| Project | Repository |
|---------|------------|
| Microsoft GraphRAG | https://github.com/microsoft/graphrag |
| OpenSPG / KAG | https://github.com/OpenSPG/KAG |
| LightRAG | https://github.com/HKUDS/LightRAG |
| HippoRAG | https://github.com/OSU-NLP-Group/HippoRAG |
| Neo4j GraphRAG | https://github.com/neo4j/neo4j-graphrag-python |
| Graphiti | https://github.com/getzep/graphiti |
| nano-graphrag | https://github.com/gusye1234/nano-graphrag |
| GraphRAG-SDK | https://github.com/FalkorDB/GraphRAG-SDK |
| Cognee | https://github.com/topoteretes/cognee |
| Neo4j LLM Graph Builder | https://github.com/neo4j-labs/llm-graph-builder |
| Zep | https://www.getzep.com |
| Kuzu | https://github.com/kuzudb/kuzu |

### Typical GraphRAG Workflow

```text
Raw Documents
        │
        ▼
Entity Extraction
        │
        ▼
Relationship Extraction
        │
        ▼
Knowledge Graph Construction
        │
        ▼
Community Detection
        │
        ▼
Graph Retrieval
        │
        ▼
LLM
```

---

# 🤖 Agentic & Reasoning-Centric Retrieval

Unlike conventional RAG pipelines, agentic retrieval systems can autonomously plan retrieval strategies, invoke tools, rewrite queries, perform iterative search, and reflect on intermediate results before generating an answer.

## Popular Frameworks

| Framework | Repository |
|-----------|------------|
| LangGraph | https://github.com/langchain-ai/langgraph |
| AutoGen | https://github.com/microsoft/autogen |
| AG2 (AutoGen fork) | https://github.com/ag2ai/ag2 |
| CrewAI | https://github.com/crewAIInc/crewAI |
| CAMEL | https://github.com/camel-ai/camel |
| OpenHands | https://github.com/All-Hands-AI/OpenHands |
| smolagents | https://github.com/huggingface/smolagents |
| Agno (formerly Phidata) | https://github.com/agno-agi/agno |
| PydanticAI | https://github.com/pydantic/pydantic-ai |
| OpenAI Swarm | https://github.com/openai/swarm |
| Letta (formerly MemGPT) | https://github.com/letta-ai/letta |
| Mem0 | https://github.com/mem0ai/mem0 |

Typical reasoning loop:

```text
Question
    │
    ▼
Planner
    │
    ▼
Retriever
    │
    ▼
Reflection
    │
    ▼
Additional Retrieval
    │
    ▼
Answer
```

---

# 🗄️ Vector Stores & Indexing Infrastructure

Vector databases provide scalable similarity search for dense embeddings and serve as the storage backbone of modern RAG systems.

## Vector Databases

| Project | Repository |
|---------|------------|
| FAISS | https://github.com/facebookresearch/faiss |
| Milvus | https://github.com/milvus-io/milvus |
| Weaviate | https://github.com/weaviate/weaviate |
| Qdrant | https://github.com/qdrant/qdrant |
| Chroma | https://github.com/chroma-core/chroma |
| LanceDB | https://github.com/lancedb/lancedb |
| Pinecone | https://www.pinecone.io |
| Vespa | https://github.com/vespa-engine/vespa |
| pgvector | https://github.com/pgvector/pgvector |
| Redis Vector Search | https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/ |
| MongoDB Atlas Vector Search | https://www.mongodb.com/products/platform/atlas-vector-search |
| turbopuffer | https://turbopuffer.com |
| DuckDB VSS | https://github.com/duckdb/duckdb-vss |
| txtai | https://github.com/neuml/txtai |

---

# 📊 Evaluation & Analysis Frameworks

Evaluation is essential for understanding retrieval quality, groundedness, and answer faithfulness. Modern RAG evaluation increasingly combines traditional IR metrics with LLM-based judges.

## Representative Projects

| Framework | Repository |
|-----------|------------|
| RAGAS | https://github.com/explodinggradients/ragas |
| TruLens | https://github.com/truera/trulens |
| DeepEval | https://github.com/confident-ai/deepeval |
| ARES | https://github.com/stanford-futuredata/ARES |
| LangSmith | https://smith.langchain.com |
| RAGChecker | https://github.com/amazon-science/RAGChecker |
| Langfuse | https://github.com/langfuse/langfuse |
| Arize Phoenix | https://github.com/Arize-ai/phoenix |
| Comet Opik | https://github.com/comet-ml/opik |
| Giskard | https://github.com/Giskard-AI/giskard-oss |

Common metrics include:

- Context Precision
- Context Recall
- Answer Relevance
- Faithfulness
- Groundedness
- Hallucination Rate
- Retrieval Precision@k
- Retrieval Recall@k
- MRR
- nDCG

---

# 🤝 Contribution Guidelines

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

> 💡 **Tip:** Prefer the **[Add a Paper](https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs/issues/new?template=add-paper.yml)** or **[Add a Resource](https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs/issues/new?template=add-resource.yml)** issue forms — a workflow checks formatting and duplicates automatically. You can also fork the repo, edit `Readme.md`, and open a pull request.

## Adding a New Entry

Place new entries under the appropriate **year** and **category**.

Each entry should include:

- **Name**
- **Paper link** (preferred)
- **GitHub repository** (if available)
- **Project page** (optional)
- **One or two sentence description**
- **Relevant tags**

Example:

```markdown
- **Project Name**
  - 📄 Paper: https://arxiv.org/abs/xxxx.xxxxx
  - 💻 Code: https://github.com/organization/project
  - Short description.
  `RAG` `GraphRAG`
```

## Inclusion Criteria

Projects should be:

- Retrieval-centric
- Relevant to LLMs
- Publicly documented
- Actively maintained (preferred)
- Widely used or academically significant

We welcome:

- Research papers
- Open-source frameworks
- Benchmarks
- Evaluation toolkits
- Graph retrieval systems
- Knowledge graph systems
- Vector databases
- Enterprise retrieval tools
- Agentic retrieval frameworks

---

# 📖 Citation

If you use this repository in academic research, surveys, blog posts, or educational material, please cite it.

### BibTeX

```bibtex
@misc{awesome_retrieval_systems_for_llms,
  title        = {Awesome Retrieval Systems for LLMs},
  author       = {Awesome Retrieval Systems for LLMs Contributors},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs}},
  note         = {A curated list of retrieval-centric systems for large language models}
}
```

### Citation File Format

You can also cite this repository using the machine-readable [CITATION.cff](CITATION.cff) file. Many reference managers (Zotero, Mendeley, etc.) can import `.cff` files directly.

### APA Style

> Awesome Retrieval Systems for LLMs Contributors. (2026). *Awesome Retrieval Systems for LLMs* [Computer software]. GitHub. https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs

If this list helps your work, consider giving the repository a ⭐ and referencing it alongside relevant RAG, GraphRAG, and agentic retrieval surveys.

---

# 📜 License

This repository is released under the **[MIT License](LICENSE)**.

| Permission | Allowed |
|------------|---------|
| ✅ Academic use | Yes |
| ✅ Commercial use | Yes |
| ✅ Modification | Yes |
| ✅ Distribution | Yes |
| ✅ Private use | Yes |

> ⚠️ **Note:** The licenses of linked projects, datasets, papers, and third-party resources are governed by their respective authors and repositories. This list is provided for informational purposes only.

See [LICENSE](LICENSE) for the full license text.

---

# 🙏 Acknowledgements

This repository builds upon the contributions of the open-source and research communities working on:

- Retrieval-Augmented Generation (RAG)
- Knowledge-Augmented Generation (KAG)
- GraphRAG
- Knowledge Graph Question Answering (KG-QA)
- Dense and Hybrid Retrieval
- Agentic AI
- Information Retrieval
- Vector Databases
- Multimodal Retrieval
- Document Intelligence

Special thanks to the authors and maintainers of the many outstanding papers, frameworks, benchmarks, and open-source projects that continue to advance retrieval systems for Large Language Models.

---

## ⭐ Star History

If you find this repository useful, consider giving it a ⭐ to support future updates and help others discover it.

[![Star History Chart](https://api.star-history.com/svg?repos=amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs&type=Date)](https://star-history.com/#amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs&Date)

---

## 🤝 Maintainers

Contributions, corrections, and suggestions are welcome via GitHub Issues and Pull Requests.

Together, we can build a comprehensive resource for the rapidly evolving ecosystem of retrieval systems for Large Language Models.