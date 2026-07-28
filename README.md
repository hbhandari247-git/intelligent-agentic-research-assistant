# 🤖 Intelligent Agentic Research Assistant

> **Building an AI Research Assistant from the ground up—one version at a time.**

A production-oriented AI application built with **Python, LangChain, ChromaDB, HuggingFace, Groq, and Tavily**, following modern software engineering principles while progressively evolving from a Retrieval-Augmented Generation (RAG) system into a fully autonomous **Agentic AI Research Assistant**.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-Chroma-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
![Tavily](https://img.shields.io/badge/Search-Tavily-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

---

# 🌟 Vision

Large Language Models become truly useful when they can **retrieve information, reason about it, and interact with external tools**.

This repository documents that journey.

Rather than building a single "Chat with PDF" application, this project incrementally develops a production-style AI assistant while applying clean architecture, modular design, and software engineering best practices.

Each release introduces a meaningful capability, transforming the project from a simple RAG system into a complete autonomous research assistant.

---

# 🚀 Current Capabilities

The current implementation provides:

* 📄 Question answering over PDF documents
* 🌐 AI-powered web search using Tavily
* 🔀 Hybrid Retrieval (PDF + Web)
* 🧠 Intelligent query routing
* 🔍 Semantic retrieval using ChromaDB
* 🧠 HuggingFace Sentence Transformer embeddings
* ⚡ Groq LLM integration
* 🏗️ Modular service-oriented architecture
* ⚙️ Centralized configuration management
* 🔐 Centralized environment initialization
* 📦 Persistent vector database
* 📝 Fully typed and documented codebase
* 🔄 Extensible architecture for future AI capabilities

---

# 🎯 Current Release

## **v2.3.0 – Hybrid Retrieval**

### Highlights

* 📄 PDF Retrieval-Augmented Generation (RAG)
* 🌐 Tavily Web Search integration
* 🔀 Intelligent PDF-first query routing
* 🤖 Shared LLM generation pipeline
* 🏗️ Modular service-oriented architecture
* ⚙️ Centralized configuration management
* 🔐 Centralized environment initialization
* 📦 Persistent Chroma vector database
* 📝 Fully typed and documented codebase

This release introduces **Hybrid Retrieval**, enabling the assistant to answer questions from indexed PDF documents while automatically falling back to AI-powered web search whenever the requested information is unavailable in the local knowledge base.

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
               ┌──────────┴──────────┐
               │                     │
               ▼                     ▼
        answer_from_pdf()     answer_from_web()
               │                     │
               ▼                     ▼
     retrieve_documents()   retrieve_from_web()
               │                     │
               └──────────┬──────────┘
                          ▼
                  build_context()
                          ▼
                  generate_answer()
                          ▼
                      Groq LLM
                          ▼
                     Final Answer
```

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
├── services/
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── generator.py
│   ├── llm.py
│   ├── pipeline.py
│   ├── rag.py
│   ├── retriever.py
│   ├── router.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   ├── web_rag.py
│   └── web_search.py
│
├── tests/
│   ├── __init__.py
│   └── test_tavily.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .env
```

---

# ⚙️ Technology Stack

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| Python      | Core programming language |
| LangChain   | LLM application framework |
| LCEL        | Pipeline orchestration    |
| ChromaDB    | Vector database           |
| HuggingFace | Embedding generation      |
| Groq        | Large Language Model      |
| Tavily      | AI-powered web retrieval  |
| PyPDFLoader | PDF document processing   |

---

# 🚀 Getting Started

## Clone the Repository

```bash
git clone https://github.com/hbhandari247-git/intelligent-agentic-research-assistant.git

cd intelligent-agentic-research-assistant
```

## Create a Virtual Environment

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Run the Application

```bash
python app.py
```

---

# 💬 Example

```text
🤖 Intelligent Agentic Research Assistant

You: What is self-attention?

🤖 Self-attention is an attention mechanism that enables each token in a sequence to attend to every other token, allowing Transformer models to capture long-range dependencies efficiently.

You: Who won the FIFA World Cup in 2022?

🤖 Argentina won the 2022 FIFA World Cup after defeating France in the final on penalties following a 3–3 draw.
```

---

# ⚙️ Configuration

Application settings are centralized in:

```text
config/settings.py
```

Configurable parameters include:

* PDF path
* Embedding model
* Vector database
* Chunk size
* Chunk overlap
* Retrieval Top-K
* Similarity threshold
* Tavily search results
* LLM model
* Temperature

---

# 🧠 How It Works

1. Initialize the PDF retrieval pipeline.
2. Accept a user question.
3. Route the question to the PDF retrieval workflow.
4. Retrieve the most relevant document chunks.
5. Check whether sufficient context exists.
6. If relevant, build the context and generate the answer.
7. Otherwise, automatically perform a Tavily web search.
8. Build context from web search results.
9. Generate the final response using Groq.

---

# 📦 Release History

| Version    | Description                                                                  |
| ---------- | ---------------------------------------------------------------------------- |
| **v2.3.0** | Hybrid Retrieval with PDF-first routing and Tavily web fallback              |
| **v2.2.1** | Centralized environment initialization and startup architecture improvements |
| **v2.2.0** | Initial stable modular PDF RAG implementation                                |

---

# 🗺️ Roadmap

## ✅ v2.3.0

* Hybrid Retrieval
* Tavily Search Integration
* Intelligent Query Routing
* Shared LLM Generation Pipeline
* Modular Web RAG Workflow

---

## 🚀 v2.4.0

* Retrieval Quality Improvements
* Better Routing Decisions
* Source Attribution
* Enhanced Context Selection

---

## 🚀 v2.5.0

* Conversation Memory
* Context-Aware Responses

---

## 🚀 v2.6.0

* Streaming Responses

---

## 🚀 v2.7.0

* Multi-PDF Knowledge Base

---

## 🚀 v2.8.0

* Tool Calling
* ReAct Agents

---

## 🚀 v2.9.0

* LangGraph Workflows

---

## 🎯 v3.0.0

### Intelligent Agentic Research Assistant

* Autonomous Planning
* Multi-Agent Collaboration
* Hybrid Knowledge Retrieval
* Research Report Generation
* Model Context Protocol (MCP)
* Long-Term Memory
* Intelligent Tool Ecosystem

---

# 📚 Learning Journey

This repository serves as a practical exploration of modern AI application development.

Topics covered throughout the project include:

* Retrieval-Augmented Generation (RAG)
* Hybrid Retrieval
* Semantic Search
* Vector Databases
* Prompt Engineering
* LangChain & LCEL
* Software Architecture
* AI Agents
* LangGraph
* Model Context Protocol (MCP)

Every release introduces a new capability while preserving a clean, maintainable, and production-oriented architecture.

---

# 🤝 Contributing

Contributions, ideas, and feedback are always welcome.

If you'd like to improve the project, feel free to open an issue or submit a pull request.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

Your support helps others discover the project and motivates future development.

---

# 👨‍💻 Author

**Himanshu Bhandari**

AI Engineer passionate about building production-quality AI systems, Retrieval-Augmented Generation (RAG) applications, Hybrid AI architectures, Agentic AI workflows, and scalable software engineering solutions.

---

> **"Great AI systems aren't built in a single release—they evolve through thoughtful architecture, continuous learning, and disciplined engineering."**
