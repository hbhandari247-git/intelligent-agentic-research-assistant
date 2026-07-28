# 🤖 Intelligent Agentic Research Assistant

> **Building an AI Research Assistant from the ground up—one version at a time.**

A production-oriented AI application built with **Python, LangChain, ChromaDB, HuggingFace, and Groq**, following modern software engineering principles while progressively evolving from a Retrieval-Augmented Generation (RAG) system into a fully autonomous **Agentic AI Research Assistant**.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-Chroma-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
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
* 🔍 Semantic retrieval using Chroma Vector Database
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

## **v2.2.1 – Stable Modular PDF RAG**

### Highlights

* Modular application architecture
* PDF ingestion pipeline
* Recursive text chunking
* Semantic vector search
* Context relevance validation
* Prompt-based response generation
* Groq-powered inference
* Clean startup architecture
* Centralized configuration
* Centralized environment loading

This release focuses on creating a solid architectural foundation before introducing hybrid retrieval and agentic workflows.

---

# 🏛️ System Architecture

```text
                    User Question
                          │
                          ▼
                      app.py
                          │
                          ▼
                 load_dotenv()
                          │
                          ▼
              initialize_pipeline()
                          │
                          ▼
                 answer_from_pdf()
                          │
                          ▼
             retrieve_documents()
                          │
                          ▼
           has_relevant_context()
                 │             │
        Relevant         Not Relevant
            │                  │
            ▼                  ▼
    build_context()     (Future)
            │        Tavily Web Search
            ▼
    generate_answer()
            │
            ▼
      Groq LLM Response
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
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│   ├── llm.py
│   ├── rag.py
│   ├── pipeline.py
│   └── web_search.py
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
```

## Run the Application

```bash
python app.py
```

---

# 💬 Example

```text
🤖 Intelligent Agentic Research Assistant

You:
What is self-attention?

Assistant:
Self-attention allows each token to attend to every other token in the sequence, enabling Transformers to model long-range dependencies efficiently.
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
* LLM model
* Temperature

---

# 🧠 How It Works

1. Load the PDF document.
2. Split it into semantic chunks.
3. Generate embeddings.
4. Store embeddings in ChromaDB.
5. Retrieve relevant context.
6. Validate retrieval quality.
7. Build the prompt context.
8. Generate the final response using Groq.

---

# 📦 Release History

| Version    | Description                                                                  |
| ---------- | ---------------------------------------------------------------------------- |
| **v2.2.1** | Centralized environment initialization and startup architecture improvements |
| **v2.2.0** | Initial stable modular PDF RAG implementation                                |

---

# 🗺️ Roadmap

## ✅ v2.2.1

* Stable Modular PDF RAG
* Clean Service-Oriented Architecture
* ChromaDB Integration
* HuggingFace Embeddings
* Groq Integration
* Centralized Configuration
* Centralized Environment Initialization

---

## 🚧 v2.3.0

* Tavily Search Integration
* Hybrid Retrieval (PDF + Web)
* Intelligent Query Routing

---

## 🚀 v2.4.0

* Conversation Memory
* Context-Aware Responses

---

## 🚀 v2.5.0

* Streaming Responses

---

## 🚀 v2.6.0

* Multi-PDF Knowledge Base

---

## 🚀 v2.7.0

* Tool Calling
* ReAct Agents

---

## 🚀 v2.8.0

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
* Semantic Search
* Vector Databases
* Prompt Engineering
* LangChain & LCEL
* Software Architecture
* Hybrid Retrieval
* AI Agents
* LangGraph
* Model Context Protocol (MCP)

Every release introduces a new concept while preserving a clean, maintainable architecture.

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

AI Engineer passionate about building production-quality AI systems, Retrieval-Augmented Generation (RAG) applications, Agentic AI workflows, and scalable software architectures.

---

> **"Great AI systems aren't built in a single release—they evolve through thoughtful architecture, continuous learning, and disciplined engineering."**
