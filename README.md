# 🤖 Intelligent Agentic Research Assistant

> **A modular Retrieval-Augmented Generation (RAG) system built with LangChain, ChromaDB, HuggingFace Embeddings, and Groq — designed to evolve into a fully autonomous Agentic AI Research Assistant.**

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-Chroma-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🌟 Overview

Most RAG tutorials end with a simple **"Chat with PDF"** application.

This project takes a different approach.

The goal is to build a **production-style AI application** step by step, following clean software engineering practices while gradually introducing modern AI concepts such as Retrieval-Augmented Generation (RAG), Hybrid Search, Agentic Workflows, Multi-Agent Systems, and the Model Context Protocol (MCP).

The current version implements a clean, modular RAG architecture capable of answering questions from PDF documents using semantic search.

---

# ✨ Features

* 📄 Ask questions about PDF documents
* 🔍 Semantic search with Chroma Vector Database
* 🧠 HuggingFace Sentence Transformer embeddings
* ⚡ Groq LLM integration
* 🏗️ Modular service-oriented architecture
* ⚙️ Centralized configuration management
* 📦 Persistent vector database
* 📝 Type hints and comprehensive documentation
* 🔄 Easily extensible for future AI capabilities

---

# 🎯 Current Version

## **v2.2.0 – Modular PDF RAG**

### Implemented

* ✅ Modular project architecture
* ✅ PDF document ingestion
* ✅ Recursive text chunking
* ✅ HuggingFace embeddings
* ✅ Chroma vector database
* ✅ Semantic document retrieval
* ✅ Context validation
* ✅ Prompt-based answer generation
* ✅ Groq LLM integration
* ✅ Configurable application settings

---

# 🏛️ System Architecture

```text
                         User Question
                               │
                               ▼
                           app.py
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
                      │               │
             Relevant          Not Relevant
                  │                    │
                  ▼                    ▼
          build_context()      (Future)
                  │         Tavily Search
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
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   └── Attention_is_All_You_Need.pdf
│
├── db/
│
├── services/
│   ├── __init__.py
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
└── .env
```

---

# ⚙️ Technology Stack

| Technology  | Purpose                       |
| ----------- | ----------------------------- |
| Python      | Programming Language          |
| LangChain   | LLM Application Framework     |
| LCEL        | LangChain Expression Language |
| ChromaDB    | Vector Database               |
| HuggingFace | Embedding Model               |
| Groq        | Large Language Model          |
| PyPDFLoader | PDF Processing                |

---

# 🚀 Getting Started

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

```bash
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
```

---

## 5. Run the Application

```bash
python app.py
```

---

# 💬 Example

```text
📄 Loading PDF...
✂️ Splitting document into chunks...
🆕 Creating new vector database...
✅ Pipeline initialized.

Ask a question:

> What is self-attention?

Assistant:

Self-attention allows each token in a sequence to attend to every other token, enabling the Transformer to model long-range dependencies without recurrence.
```

---

# ⚙️ Configuration

All application settings are centralized in:

```text
config/settings.py
```

Available configuration includes:

* PDF document path
* Chroma database location
* Embedding model
* Chunk size
* Chunk overlap
* Retrieval Top-K
* Similarity threshold
* LLM model
* Temperature

---

# 🧠 How It Works

1. Load the PDF document.
2. Split the document into semantic chunks.
3. Generate embeddings for every chunk.
4. Store embeddings inside ChromaDB.
5. Retrieve the most relevant chunks.
6. Validate retrieval relevance.
7. Build the retrieval context.
8. Generate the final answer using the LLM.

---

# 📈 Project Roadmap

## ✅ v2.2.0

* [x] Modular RAG Architecture
* [x] PDF Question Answering
* [x] Chroma Vector Database
* [x] HuggingFace Embeddings
* [x] Groq Integration
* [x] Service-Oriented Design

---

## 🚧 v2.3.0

* [ ] Tavily Web Search
* [ ] Hybrid PDF/Web Routing
* [ ] Intelligent Query Router

---

## 🚀 v2.4.0

* [ ] Conversation Memory
* [ ] Context-Aware Responses

---

## 🚀 v2.5.0

* [ ] Streaming Responses

---

## 🚀 v2.6.0

* [ ] Multi-PDF Knowledge Base

---

## 🚀 v2.7.0

* [ ] Tool Calling
* [ ] ReAct Agents

---

## 🚀 v2.8.0

* [ ] LangGraph Workflows

---

## 🎯 v3.0.0

### Intelligent Agentic Research Assistant

* [ ] Autonomous Planning
* [ ] Multi-Agent Collaboration
* [ ] Web + Documents + APIs
* [ ] Research Report Generation
* [ ] MCP Integration
* [ ] Long-Term Memory
* [ ] Intelligent Tool Ecosystem

---

# 📚 Learning Objectives

This repository is built as a learning journey through modern AI application development.

Topics covered include:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search
* Prompt Engineering
* LangChain LCEL
* Modular Python Architecture
* Hybrid Retrieval
* AI Agents
* LangGraph
* Model Context Protocol (MCP)

Each version introduces one major concept while keeping the architecture clean and maintainable.

---

# 🤝 Contributing

Contributions are welcome.

If you have suggestions, find a bug, or want to improve the project, feel free to open an issue or submit a pull request.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# ⭐ Support

If you found this project useful or interesting, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.

---

# 👨‍💻 Author

**Himanshu Bhandari**

AI Engineer passionate about building production-quality LLM applications, Retrieval-Augmented Generation (RAG) systems, Agentic AI, and modern AI software architectures.

---

> **"Build it modular. Build it understandable. Then make it intelligent."**
