# 🤖 Intelligent Agentic Research Assistant

> **Building a production-quality AI Research Assistant—one release at a time.**

A production-oriented AI application built with **Python, LangChain, ChromaDB, Hugging Face, Groq, and Tavily**, following modern software engineering principles while progressively evolving from a Retrieval-Augmented Generation (RAG) system into a fully autonomous **Agentic AI Research Assistant**.

Rather than focusing solely on implementing AI features, this project emphasizes **clean architecture, modular design, maintainability, and scalable software engineering practices**. Each release introduces meaningful capabilities while preserving a well-structured codebase that can evolve into a production-ready intelligent assistant.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-Chroma-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
![Tavily](https://img.shields.io/badge/Search-Tavily-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

---

# 🌟 Vision

Large Language Models become truly valuable when they can **retrieve reliable information, reason over it, evaluate the quality of retrieved knowledge, and interact with external tools**.

This repository documents that journey.

Instead of building a simple "Chat with PDF" application, this project incrementally develops a production-oriented AI research assistant while applying modern software engineering principles, clean architecture, and modular design.

Each release focuses on introducing meaningful capabilities without sacrificing maintainability or code quality. The long-term goal is to evolve this project into a fully autonomous **Agentic AI Research Assistant** capable of planning, reasoning, retrieving information from multiple knowledge sources, and orchestrating external tools.

---

# 🚀 Current Capabilities

The current implementation provides:

- 📄 Retrieval-Augmented Generation (RAG) over PDF documents
- 🌐 AI-powered web search using Tavily
- 🔀 Intelligent PDF-first routing with automatic web fallback
- 🔍 Semantic retrieval using ChromaDB
- 🧠 Hugging Face Sentence Transformer embeddings
- ⚡ Groq LLM integration
- 📊 Confidence-based retrieval evaluation
- 📑 Source attribution with citations
- 🧩 Structured response models
- 🏗️ Clean layered architecture
- ⚙️ Centralized configuration management
- 🔐 Centralized environment initialization
- 📦 Persistent vector database
- 📝 Fully typed and documented codebase
- 🔄 Extensible architecture for future AI capabilities

---

# 🎯 Current Release

## **v2.4.0 – Intelligent Retrieval & Response Pipeline**

### ✨ Highlights

- 📄 PDF Retrieval-Augmented Generation (RAG)
- 🌐 Tavily AI Web Search integration
- 🔀 Intelligent PDF-first routing with automatic web fallback
- 📊 Confidence-based retrieval evaluation
- 📑 Source attribution and citations
- 🧩 Structured response model
- 🤖 Shared LLM generation pipeline
- 🏗️ Clean layered architecture
- 📝 Fully typed domain models
- ⚡ Improved maintainability and extensibility

### What's New in v2.4.0?

This release focuses on **architecture, reliability, and response quality**.

Major improvements include:

- A dedicated retrieval evaluation layer for confidence scoring.
- Structured response objects using domain models.
- Source attribution through citations.
- Null Object pattern for handling unanswered queries.
- Cleaner separation of responsibilities across services.
- Improved prompt engineering for better synthesized answers.
- Consistent typing and documentation across the project.

These improvements establish a solid architectural foundation for future features such as **true hybrid retrieval, conversation memory, LangGraph workflows, and autonomous AI agents.**

---

# 🏛️ System Architecture

```text
                            User Question
                                  │
                                  ▼
                              app.py
                                  │
                                  ▼
                          route_question()
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             answer_from_pdf()          answer_from_web()
                    │                           │
                    ▼                           ▼
         retrieve_documents()          retrieve_from_web()
                    │                           │
                    ▼                           ▼
        evaluate_retrieval()         evaluate_retrieval()
                    │                           │
            (Confidence Score)        (Confidence Score)
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                          build_context()
                                  │
                                  ▼
                         generate_answer()
                                  │
                                  ▼
                              Groq LLM
                                  │
                                  ▼
                               Response
      (Answer • Source • Confidence • Citations)
```

The application follows a layered architecture where each service has a single responsibility.

- **Retriever** retrieves relevant information.
- **Evaluator** determines retrieval quality and confidence.
- **Generator** builds responses using the LLM.
- **Router** decides whether to answer from the local knowledge base or fall back to web search.
- **Response models** provide a consistent interface between all layers.

This separation keeps the codebase modular, testable, and easy to extend.

---

# 📁 Project Structure

```text
intelligent-agentic-research-assistant/
│
├── app.py
│
├── config/
│   └── settings.py
│
├── data/
│
├── db/
│
├── models/
│   ├── citation.py
│   ├── confidence.py
│   ├── response.py
│   ├── retrieval_evaluation.py
│   ├── source.py
│   └── web_result.py
│
├── services/
│   ├── evaluator.py
│   ├── generator.py
│   ├── pipeline.py
│   ├── rag.py
│   ├── retriever.py
│   ├── router.py
│   ├── web_rag.py
│   └── web_search.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .env
```

### Directory Overview

| Directory | Purpose |
|------------|---------|
| **config/** | Centralized application configuration |
| **models/** | Domain models used throughout the application |
| **services/** | Business logic and application services |
| **db/** | Persistent Chroma vector database |
| **data/** | PDF documents used as the local knowledge base |

---

# ⚙️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12** | Core programming language |
| **LangChain** | LLM application framework |
| **LCEL** | Pipeline composition and orchestration |
| **ChromaDB** | Persistent vector database |
| **Hugging Face** | Sentence Transformer embeddings |
| **Groq** | Large Language Model inference |
| **Tavily** | AI-powered web search |
| **PyPDF** | PDF document processing |
| **python-dotenv** | Environment variable management |

---

# 🏗️ Software Design Principles

The project is designed around modern software engineering practices rather than simply implementing AI functionality.

Some of the architectural principles used include:

- Single Responsibility Principle (SRP)
- Separation of Concerns
- Domain-driven models
- Null Object Pattern
- Service-oriented architecture
- Strong typing throughout the codebase
- Immutable response objects
- Modular and extensible design

The goal is to create a codebase that remains maintainable as additional capabilities such as conversation memory, hybrid retrieval, and AI agents are introduced.

---

# 🚀 Getting Started

Follow these steps to set up and run the Intelligent Agentic Research Assistant locally.

## 1. Clone the Repository

```bash
git clone https://github.com/hbhandari247-git/intelligent-agentic-research-assistant.git

cd intelligent-agentic-research-assistant
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 5. Configure the Application

Most application settings can be customized from:

```text
config/settings.py
```

This includes:

- PDF document path
- Embedding model
- Chroma database location
- Chunk size
- Chunk overlap
- Retrieval Top-K
- Similarity threshold
- Tavily search configuration
- LLM model
- Temperature

---

## 6. Build the Vector Database

The first time you run the application, the PDF is indexed into the persistent Chroma vector database.

Subsequent executions reuse the existing database automatically.

---

## 7. Run the Assistant

```bash
python app.py
```

---

# 💬 Example Session

```text
🤖 Intelligent Agentic Research Assistant

You:
What is self-attention?

🤖
Self-attention is an attention mechanism that enables each token in a sequence to attend to every other token. Unlike recurrent architectures, it allows the model to capture long-range dependencies by computing relationships between all tokens in parallel.

Source:
PDF

Confidence:
High

References:
• Attention Is All You Need.pdf — Page 2
• Attention Is All You Need.pdf — Page 6

------------------------------------------------------------

You:
Who is the CEO of OpenAI?

🤖
Sam Altman is the CEO of OpenAI.

Source:
Web

Confidence:
Very High

References:
• OpenAI

------------------------------------------------------------

You:
asdkfjhasdkjfh

🤖
I couldn't find relevant information to answer your question.

Source:
None

Confidence:
None
```

---

# ⚙️ Configuration

Application behavior is centralized in:

```text
config/settings.py
```

### Retrieval

- Number of retrieved document chunks
- Similarity threshold
- Chunk size
- Chunk overlap

### Embeddings

- Hugging Face embedding model
- Embedding cache

### LLM

- Groq model
- Temperature

### Web Search

- Tavily search depth
- Maximum search results

### Storage

- Persistent Chroma database path
- PDF document location

Centralizing these settings makes experimentation straightforward without requiring changes throughout the codebase.

---

# 🧠 How It Works

The assistant follows a retrieval-first workflow designed to maximize answer quality while minimizing hallucinations.

## Step 1 — User Question

The application accepts a natural language question from the user.

```
"What is self-attention?"
```

↓

## Step 2 — Semantic Retrieval

The question is converted into an embedding and compared against the Chroma vector database to retrieve the most relevant document chunks.

↓

## Step 3 — Retrieval Evaluation

The retrieved results are evaluated using similarity thresholds to determine:

- Whether enough relevant context exists
- The confidence level of the retrieval
- Whether the answer should come from the local knowledge base

Possible confidence levels include:

- Very High
- High
- Medium
- Low
- None

↓

## Step 4 — Intelligent Routing

If retrieval quality is sufficient:

```
Question
    │
    ▼
 PDF RAG
```

Otherwise:

```
Question
    │
    ▼
 Tavily Web Search
```

↓

## Step 5 — Context Construction

Relevant information from the selected source is combined into a single context for the language model.

↓

## Step 6 — Response Generation

The Groq LLM generates a response using **only** the retrieved context.

If insufficient information exists, the assistant returns a safe fallback response instead of hallucinating.

↓

## Step 7 — Structured Response

Every response contains:

- Answer
- Source
- Confidence
- Citations (when available)

This structured response model provides a consistent interface throughout the application while making future extensions significantly easier.

---

# 📦 Release History

| Version | Description |
|----------|-------------|
| **v2.4.0** | Confidence-based retrieval evaluation, structured response models, citations, clean layered architecture, and improved answer generation |
| **v2.3.0** | Intelligent PDF-first routing with Tavily web fallback |
| **v2.2.1** | Centralized environment initialization and startup architecture improvements |
| **v2.2.0** | Initial stable modular PDF RAG implementation |

---

# 🗺️ Roadmap

The long-term goal is to evolve this project into a production-quality autonomous research assistant.

## ✅ v2.4.0

- Confidence-based retrieval evaluation
- Structured response model
- Source attribution and citations
- Null Object pattern
- Improved prompt engineering
- Clean layered architecture

---

## 🚀 v2.5.0

### Retrieval Improvements

- True Hybrid Retrieval (PDF + Web)
- Retrieval reranking
- Context fusion
- Better routing decisions

---

## 🚀 v2.6.0

### Memory

- Conversation memory
- Context-aware responses
- Multi-turn conversations

---

## 🚀 v2.7.0

### Knowledge Base

- Multiple PDF collections
- Dynamic document indexing
- Metadata filtering

---

## 🚀 v2.8.0

### AI Agents

- Tool Calling
- ReAct Agents
- Function Calling
- External API integrations

---

## 🚀 v2.9.0

### Agent Workflows

- LangGraph workflows
- Planning and execution
- Multi-step reasoning

---

## 🎯 v3.0.0

### Intelligent Agentic Research Assistant

- Autonomous planning
- Multi-agent collaboration
- Research report generation
- Model Context Protocol (MCP)
- Long-term memory
- Intelligent tool ecosystem
- Autonomous research workflows

---

# 📚 Learning Journey

This repository serves as a practical exploration of modern AI application development and software engineering.

Topics covered throughout the project include:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Prompt Engineering
- LangChain & LCEL
- ChromaDB
- Confidence-based Retrieval
- Software Architecture
- Design Patterns
- AI Agents
- LangGraph
- Model Context Protocol (MCP)

Each release introduces meaningful capabilities while preserving a clean, maintainable, and extensible architecture.

Rather than rapidly adding features, this project emphasizes **building AI systems correctly**, ensuring every architectural decision supports future growth.

---

# 🤝 Contributing

Contributions, ideas, and feedback are always welcome.

If you'd like to improve the project, feel free to:

- ⭐ Star the repository
- 🐛 Report bugs by opening an issue
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve the documentation

Whether it's fixing a typo, improving the architecture, or proposing new AI capabilities, every contribution is appreciated.

---

# 📜 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute the project in accordance with the license terms.

---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

Your support helps others discover the project and motivates continued development.

---

# 👨‍💻 Author

**Himanshu Bhandari**

AI Engineer passionate about building production-quality AI systems with a strong emphasis on software architecture, Retrieval-Augmented Generation (RAG), Agentic AI, and scalable machine learning applications.

### Connect

- GitHub: https://github.com/hbhandari247-git
- LinkedIn: *(linkedin.com/in/hbhandari247)*

---

# 🙏 Acknowledgements

This project is built using several outstanding open-source technologies.

Special thanks to the communities behind:

- LangChain
- ChromaDB
- Hugging Face
- Groq
- Tavily

Their work makes modern AI application development significantly more accessible.

---

# 🚀 What's Next?

The journey doesn't end with v2.4.0.

Upcoming releases will focus on:

- True Hybrid Retrieval
- Conversation Memory
- Multi-document Knowledge Bases
- LangGraph Workflows
- Autonomous AI Agents
- Model Context Protocol (MCP)
- Production Deployment
- Continuous Evaluation

The goal is to evolve this repository into a complete **production-quality Agentic AI Research Assistant** while documenting every architectural decision along the way.

---

> **"Great AI systems aren't built in a single release—they evolve through thoughtful architecture, continuous learning, and disciplined engineering."**
