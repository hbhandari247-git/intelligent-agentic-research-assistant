# 🤖 Intelligent Agentic Research Assistant

> **Building a production-quality AI Research Assistant---one release at a time.**

A production-oriented AI application built with **Python, LangChain, CrewAI, ChromaDB, Hugging Face, Groq, and Tavily**, following modern software engineering principles while progressively evolving from a Retrieval-Augmented Generation (RAG) system into a fully autonomous **Agentic AI Research Assistant**.

Rather than focusing solely on implementing AI features, this project emphasizes **clean architecture, modular design, maintainability, and scalable software engineering practices**. Each release introduces meaningful capabilities while preserving a well-structured codebase that can evolve into a production-ready intelligent assistant.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![Orchestrator](https://img.shields.io/badge/Orchestrator-CrewAI-cyan)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-Chroma-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
![Tavily](https://img.shields.io/badge/Search-Tavily-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

------------------------------------------------------------------------

# 🌟 Vision

Large Language Models become truly valuable when they can **retrieve reliable information, reason over it, evaluate the quality of retrieved knowledge, and interact with external tools**.

This repository documents that journey.

Instead of building a simple "Chat with PDF" application, this project incrementally develops a production-oriented AI research assistant while applying modern software engineering principles, clean architecture, and modular design.

Each release focuses on introducing meaningful capabilities without sacrificing maintainability or code quality. The long-term goal is to evolve this project into a fully autonomous **Agentic AI Research Assistant** capable of planning, reasoning, retrieving information from multiple knowledge sources, and orchestrating external tools.

------------------------------------------------------------------------

# 🚀 Current Capabilities

The current implementation provides:

-   📄 Retrieval-Augmented Generation (RAG) over PDF documents
-   🌐 AI-powered web search using Tavily
-   🔀 Adaptive PDF-only, Hybrid, and Web-only retrieval strategies
-   🤖 **Autonomous Multi-Agent Crew (v3.0.0):** Specialized Lead Research Planner, Evidence Specialist, and Synthesis Agent cooperating for deep research.
-   💾 **Long-Term Memory (LTM) database (v3.0.0):** SQLite engine mapping past contexts and custom style preferences.
-   🔌 **Model Context Protocol (v3.0.0):** stdio client dynamically mapping server tools into the researcher agent's loop.
-   🔀 True hybrid retrieval across PDF and Web evidence
-   🧩 Normalized cross-source retrieval candidates
-   🎯 Embedding-based cross-source reranking
-   🏆 Ranked evidence selection with configurable Hybrid Top-K
-   🧬 Structured multi-source context fusion
-   🔍 Semantic retrieval using ChromaDB
-   🧠 Hugging Face Sentence Transformer embeddings
-   ⚡ Groq LLM integration
-   📊 Confidence-based retrieval evaluation
-   📑 PDF, Web, and Hybrid source attribution with citations
-   🧩 Structured response models
-   🔧 Dynamic tool registry and execution adapters
-   🔄 Bounded multi-step agent loop with observations
-   🛡️ Duplicate-call and per-tool execution safeguards
-   🏗️ Clean layered architecture
-   ⚙️ Centralized configuration management
-   🔐 Centralized environment initialization
-   📦 Persistent vector database
-   📚 Multiple document collections
-   🗂️ Dynamic collection discovery
-   ♻️ Automatic document index rebuilding
-   📄 Generic document loading pipeline
-   📑 Manifest-based index synchronization
-   📝 Fully typed and documented codebase
-   💬 Context-aware multi-turn conversations
-   🧠 Bounded in-session conversation memory
-   ✍️ Standalone question rewriting for follow-up retrieval
-   🧹 Conversational memory reset with the `clear` command
-   🧪 Extensive unit test coverage (52% code coverage) under mocked environments

------------------------------------------------------------------------

# 🎯 Current Release

## **v3.0.0 -- Autonomous Multi-Agent Crews & Long-Term Memory (LTM) Architecture**

### ✨ Highlights

-   🤖 **Multi-Agent CrewAI Orchestration:** Replaced the single-agent pipeline with a cooperative Crew of three specialized agents:
    *   **Lead Research Planner:** Analyzes the topic, queries past contexts, and drafts a structured search query plan.
    *   **Evidence Retrieval Specialist:** Executes search tools (local database and web) to collect facts.
    *   **Synthesis & Verification Specialist:** Compiles findings, runs grounding checks, and builds the final Markdown report.
-   💾 **SQLite Long-Term Memory (LTM) Engine:** Created a persistent SQLite database (`db/memory.db`) storing:
    *   `research_history`: Logs past topics and generated reports.
    *   `user_preferences`: Stores user depth (comprehensive vs. quick overview) and style guidelines (technical, concise, tutorial).
-   🔌 **Model Context Protocol (MCP) Client:** Implemented stdio-based JSON-RPC transport client connecting to local MCP servers. Dynamically discovers tools and exposes them to the researcher crew.
-   🛡️ **Rate-Limit & Token Safeguards:** Constrained agent ReAct iterations (`max_iter=3`), query counts (max 3), and tool observation chunks (capped to `500` characters) to strictly fit inside Groq's 8,000 TPM limit.
-   ⚖️ **Metadata Refinement:** Configured fallback overrides setting `Source.NONE`, `Confidence.NONE`, and empty citations when the generator issues an unknown refusal message (*"I don't have enough information..."*).

---

# 📜 Previous Releases

## **v2.9.6 -- OmniRoute AI Gateway Integration**

-   🌐 **OmniRoute AI Gateway Integration:** Configured standard OpenAI-compatible client routing through a local proxy to support auto-fallback across multiple API keys, round-robin load balancing, and prompt token compression.
-   🛠️ **Configurable Toggle:** Added the `USE_OMNIROUTE` toggle and `OMNIROUTE_API_BASE` parameters to `config/settings.py` for backward-compatible routing.
-   🧪 **Clean Proxy Call Path:** Swapped from `ChatGroq` to `ChatOpenAI` when using the gateway, resolving the `404 Unknown API Route` bug caused by the Groq SDK client library appending custom namespaces.

## **v2.9.5 -- Optimization and Comparative RAG**

-   🏆 **Prioritized Document-Level Source Diversity:** Grouped candidate sources by their exact document filename and placed the top representative of each document at the front of the candidate list.
-   🎯 **Optimized Relevance Thresholds:** Tuned `MIN_SOURCE_RELEVANCE = 0.40` to allow secondary documents in comparative queries to pass representation filters.

------------------------------------------------------------------------

# 🏛️ System Architecture

``` text
                               User Topic / Question
                                         │
                                         ▼
                                      app.py
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
          Conversational Mode                      Autonomous Crew Mode (v3.0.0)
                   │                                           │
                   ▼                                           ▼
          ConversationService                         services/crew_service.py
          ┌────────┴────────┐                                  │
          ▼                 ▼                                  ▼
   Memory Rewriter  Agent Orchestrator                1. Fetch LTM Context
          │                 │                            * past reports
          ▼                 ▼                            * style preferences
    Standalone Q      Tool Selector                            │
          │                 │                                  ▼
          └────────┬────────┘                         2. Load MCP Tools (stdio client)
                   │                                           │
                   ▼                                           ▼
             Tool Registry                            3. Crew Kickoff
          ┌────────┴────────┐                            * Planner Agent (drafts queries)
          ▼                 ▼                            * Researcher Agent (runs tools)
      PDF Tool           Web Tool                        * Synthesis Agent (writes MD)
          │                 │                                  │
          └────────┬────────┘                                  ▼
                   │                                  4. Save Report to SQLite
                   ▼                                           │
         Cross-Source Reranker                                 ▼
                   │                                  5. Export outputs/report.md
                   ▼
             Context Fusion
                   │
                   ▼
           Grounded Generator
```

------------------------------------------------------------------------

# 📁 Project Structure

``` text
intelligent-agentic-research-assistant/
│
├── app.py                      # Interactive CLI application entry point
├── config/
│   ├── settings.py             # Centralized application parameters
│   └── mcp_servers.json        # MCP server connection configurations
├── data/                       # Local document collection directories
├── db/                         # Chroma DB vector database files (ignored)
├── scratch/                    # Temporary and diagnostic test scripts
├── models/                     # Type contracts and dataclasses
│   ├── collection.py
│   ├── response.py
│   ├── source.py
│   └── ...
├── services/
│   ├── crew_service.py         # CrewAI agent setup and kickoff
│   ├── memory_service.py       # SQLite database queries and preferences
│   ├── mcp_client.py           # stdio JSON-RPC MCP tool wrappers
│   ├── response_builder.py     # Reranking and response metadata assembly
│   └── ...
├── tests/                      # Python pytest files
│   ├── conftest.py             # Global dummy environments setups
│   ├── test_memory.py          # SQLite database assertions
│   ├── test_mcp.py             # Handshake and tool listing mock assertions
│   └── ...
├── requirements.txt
└── .env
```

------------------------------------------------------------------------

# ⚙️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12** | Programming language |
| **LangChain** | LLM orchestrations |
| **CrewAI** | Multi-Agent Crew setup |
| **ChromaDB** | Vector Database |
| **Hugging Face** | Embeddings pipeline |
| **Tavily** | Search engine |
| **SQLite** | Long-Term Memory (LTM) storage |
| **OmniRoute** | OpenAI Gateway Proxy (Direct/direct routing) |

------------------------------------------------------------------------

# 🚀 Getting Started

Follow these steps to set up and run the Intelligent Agentic Research Assistant locally.

## 1. Clone the Repository

``` bash
git clone https://github.com/hbhandari247-git/intelligent-agentic-research-assistant.git
cd intelligent-agentic-research-assistant
```

## 2. Set Up Virtual Environment & Dependencies

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Create a `.env` file in the project root:

``` env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 4. Run the Application

``` bash
python app.py
```

*   **Option 1:** Start interactive conversational chat (RAG).
*   **Option 2:** Launch autonomous Crew research reports.
*   **Option 3:** Inspect SQLite past report history log entries.
*   **Option 4:** Edit custom LTM style and depth guidelines.
*   **Option 8:** Exit application.

------------------------------------------------------------------------

# 🔌 Model Context Protocol (MCP) Setup

To connect filesystem tools or custom APIs:
1. Open [`config/mcp_servers.json`](file:///Users/himanshubhandari/Downloads/RTB/RTB_Project_Impetus/intelligent-agentic-research-assistant/config/mcp_servers.json).
2. Configure your server command and arguments:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "node",
         "args": ["/path/to/server/index.js", "/path/to/data"]
       }
     }
   }
   ```
3. During autonomous research (Option 2), the system will connect to the server, discover tools, and provide them to the researcher agent automatically.

------------------------------------------------------------------------

# 🧪 Running Tests

Verify the codebase functionality using `pytest`:

``` bash
# Run all unit tests
pytest -v

# Run with test coverage reporting
pytest --cov=services --cov=models tests/
```
