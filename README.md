# 🤖 Intelligent Agentic Research Assistant

> **Building a production-quality AI Research Assistant---one release at
> a time.**

A production-oriented AI application built with **Python, LangChain,
ChromaDB, Hugging Face, Groq, and Tavily**, following modern software
engineering principles while progressively evolving from a
Retrieval-Augmented Generation (RAG) system into a fully autonomous
**Agentic AI Research Assistant**.

Rather than focusing solely on implementing AI features, this project
emphasizes **clean architecture, modular design, maintainability, and
scalable software engineering practices**. Each release introduces
meaningful capabilities while preserving a well-structured codebase that
can evolve into a production-ready intelligent assistant.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-Chroma-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
![Tavily](https://img.shields.io/badge/Search-Tavily-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

------------------------------------------------------------------------

# 🌟 Vision

Large Language Models become truly valuable when they can **retrieve
reliable information, reason over it, evaluate the quality of retrieved
knowledge, and interact with external tools**.

This repository documents that journey.

Instead of building a simple "Chat with PDF" application, this project
incrementally develops a production-oriented AI research assistant while
applying modern software engineering principles, clean architecture, and
modular design.

Each release focuses on introducing meaningful capabilities without
sacrificing maintainability or code quality. The long-term goal is to
evolve this project into a fully autonomous **Agentic AI Research
Assistant** capable of planning, reasoning, retrieving information from
multiple knowledge sources, and orchestrating external tools.

------------------------------------------------------------------------

# 🚀 Current Capabilities

The current implementation provides:

-   📄 Retrieval-Augmented Generation (RAG) over PDF documents
-   🌐 AI-powered web search using Tavily
-   🔀 Adaptive PDF-only, Hybrid, and Web-only retrieval strategies
-   🔗 True hybrid retrieval across PDF and Web evidence
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
-   🏗️ Clean layered architecture
-   ⚙️ Centralized configuration management
-   🔐 Centralized environment initialization
-   📦 Persistent vector database
-   📝 Fully typed and documented codebase
-   🔄 Extensible architecture for future AI capabilities

------------------------------------------------------------------------

# 🎯 Current Release

## **v2.5.0 -- Adaptive Hybrid Retrieval & Cross-Source Reranking**

### ✨ Highlights

-   🔀 Adaptive PDF-only, Hybrid, and Web-only retrieval strategies
-   🔗 True PDF + Web hybrid retrieval
-   🧩 Shared `RetrievalCandidate` representation across knowledge
    sources
-   🎯 Embedding-based cross-source reranking
-   🏆 `RankedCandidate` model with a common relevance score
-   ✂️ Configurable `HYBRID_TOP_K` evidence selection
-   🧬 Structured multi-source context fusion
-   📑 Unified PDF, Web, and Hybrid citations
-   📊 Combined confidence handling for hybrid responses
-   🛡️ Safe Null Object behavior when no source provides sufficient
    evidence
-   🏗️ Simplified routing through a dedicated hybrid RAG workflow
-   📝 Fully typed and modular implementation

### What's New in v2.5.0?

This release evolves the previous PDF-first fallback pipeline into an
**adaptive hybrid retrieval system**.

The assistant first evaluates local PDF retrieval quality and selects
one of three strategies:

-   **PDF Only** --- strong local evidence is sufficient, so no
    unnecessary web request is made.
-   **Hybrid** --- usable but uncertain PDF evidence is supplemented
    with Tavily web retrieval.
-   **Web Only** --- unusable PDF evidence causes the workflow to rely
    on evaluated web results.

PDF and web results are converted into a shared `RetrievalCandidate`
representation. Because Chroma distance scores and Tavily relevance
scores are not directly comparable, candidates are reranked against the
original question using the same Hugging Face embedding model and cosine
similarity. The strongest candidates are retained using `HYBRID_TOP_K`.

The selected evidence is fused into structured multi-source context
while preserving source metadata and citations. The final response can
accurately report **PDF**, **Web**, **Hybrid**, or **None** as its
source.

This release establishes the retrieval foundation for **conversation
memory and context-aware multi-turn interactions** in v2.6.0.

------------------------------------------------------------------------

# 🏛️ System Architecture

``` text
                              User Question
                                   │
                                   ▼
                                 app.py
                                   │
                                   ▼
                            route_question()
                                   │
                                   ▼
                         answer_from_hybrid()
                                   │
                                   ▼
                      PDF Retrieval + Evaluation
                                   │
                                   ▼
                       Retrieval Strategy
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
              PDF_ONLY           HYBRID           WEB_ONLY
                 │                 │                 │
                 │                 ▼                 ▼
                 │          Tavily Web Search   Tavily Web Search
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   ▼
                         Candidate Normalization
                         RetrievalCandidate[]
                                   │
                                   ▼
                     Common Embedding-Space Reranker
                                   │
                                   ▼
                          RankedCandidate[]
                                   │
                                   ▼
                             HYBRID_TOP_K
                                   │
                                   ▼
                            Context Fusion
                          ┌────────┴────────┐
                          ▼                 ▼
                       Context          Citations
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

The application keeps retrieval, evaluation, strategy selection,
candidate normalization, reranking, context fusion, generation, and
response construction as focused responsibilities.

-   **Retriever** retrieves relevant PDF evidence from ChromaDB.
-   **Web Search** retrieves external evidence through Tavily when
    required.
-   **Evaluator** interprets source-specific retrieval scores and
    assigns confidence.
-   **Retrieval Strategy** selects PDF-only, Hybrid, or Web-only
    behavior.
-   **Candidate Builder** converts source-specific results into a common
    representation.
-   **Reranker** compares PDF and web candidates in one embedding space.
-   **Context Fusion** combines the strongest ranked evidence while
    preserving citations.
-   **Generator** produces a grounded answer from the fused context.
-   **Router** delegates questions to the hybrid RAG workflow.
-   **Response models** provide a consistent answer, source, confidence,
    and citation interface.

PDF distance and Tavily relevance values are never directly compared
because they have different score semantics.

------------------------------------------------------------------------

# 📁 Project Structure

``` text
intelligent-agentic-research-assistant/
│
├── app.py
├── config/
│   └── settings.py
├── data/
├── db/
├── models/
│   ├── __init__.py
│   ├── citation.py
│   ├── confidence.py
│   ├── ranked_candidate.py
│   ├── response.py
│   ├── retrieval_candidate.py
│   ├── retrieval_evaluation.py
│   ├── retrieval_strategy.py
│   ├── source.py
│   └── web_result.py
├── services/
│   ├── __init__.py
│   ├── candidate_builder.py
│   ├── context_fusion.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── evaluator.py
│   ├── generator.py
│   ├── hybrid_rag.py
│   ├── llm.py
│   ├── pipeline.py
│   ├── rag.py
│   ├── reranker.py
│   ├── retrieval_strategy.py
│   ├── retriever.py
│   ├── router.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   ├── web_rag.py
│   └── web_search.py
├── requirements.txt
├── README.md
├── LICENSE
└── .env
```

### Directory Overview

  Directory       Purpose
  --------------- ------------------------------------------------
  **config/**     Centralized application configuration
  **models/**     Domain models used throughout the application
  **services/**   Business logic and application services
  **db/**         Persistent Chroma vector database
  **data/**       PDF documents used as the local knowledge base

------------------------------------------------------------------------

# ⚙️ Technology Stack

  Technology          Purpose
  ------------------- ----------------------------------------
  **Python 3.12**     Core programming language
  **LangChain**       LLM application framework
  **LCEL**            Pipeline composition and orchestration
  **ChromaDB**        Persistent vector database
  **Hugging Face**    Sentence Transformer embeddings
  **Groq**            Large Language Model inference
  **Tavily**          AI-powered web search
  **PyPDF**           PDF document processing
  **python-dotenv**   Environment variable management

------------------------------------------------------------------------

# 🏗️ Software Design Principles

The project is designed around modern software engineering practices
rather than simply implementing AI functionality.

Some of the architectural principles used include:

-   Single Responsibility Principle (SRP)
-   Separation of Concerns
-   Domain-driven models
-   Null Object Pattern
-   Service-oriented architecture
-   Strong typing throughout the codebase
-   Immutable response objects
-   Modular and extensible design

The goal is to create a codebase that remains maintainable as additional
capabilities such as conversation memory, multi-document knowledge
bases, and AI agents are introduced.

------------------------------------------------------------------------

# 🚀 Getting Started

Follow these steps to set up and run the Intelligent Agentic Research
Assistant locally.

## 1. Clone the Repository

``` bash
git clone https://github.com/hbhandari247-git/intelligent-agentic-research-assistant.git

cd intelligent-agentic-research-assistant
```

------------------------------------------------------------------------

## 2. Create a Virtual Environment

### macOS / Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

``` powershell
python -m venv .venv
.venv\Scripts\activate
```

------------------------------------------------------------------------

## 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4. Configure Environment Variables

Create a `.env` file in the project root.

``` env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

------------------------------------------------------------------------

## 5. Configure the Application

Most application settings can be customized from:

``` text
config/settings.py
```

This includes:

-   PDF document path
-   Embedding model
-   Chroma database location
-   Chunk size
-   Chunk overlap
-   Retrieval Top-K
-   Hybrid reranking Top-K (`HYBRID_TOP_K`)
-   PDF retrieval threshold
-   Web retrieval threshold
-   Tavily search configuration
-   LLM model
-   Temperature

------------------------------------------------------------------------

## 6. Build the Vector Database

The first time you run the application, the PDF is indexed into the
persistent Chroma vector database.

Subsequent executions reuse the existing database automatically.

------------------------------------------------------------------------

## 7. Run the Assistant

``` bash
python app.py
```

------------------------------------------------------------------------

# 💬 Example Session

``` text
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

------------------------------------------------------------------------

# ⚙️ Configuration

Application behavior is centralized in:

``` text
config/settings.py
```

### Retrieval

-   Number of PDF chunks retrieved
-   PDF retrieval threshold
-   Web retrieval threshold
-   Hybrid reranking Top-K (`HYBRID_TOP_K`)
-   Chunk size
-   Chunk overlap

### Embeddings

-   Hugging Face embedding model
-   Embedding cache
-   Shared embedding space for cross-source reranking

### LLM

-   Groq model
-   Temperature

### Web Search

-   Tavily search depth
-   Maximum search results

### Storage

-   Persistent Chroma database path
-   PDF document location

Centralizing these settings makes experimentation straightforward
without requiring changes throughout the codebase.

------------------------------------------------------------------------

# 🧠 How It Works

The assistant follows an adaptive retrieval workflow designed to use
strong local evidence efficiently while supplementing uncertain
retrieval with external knowledge when needed.

## Step 1 --- User Question

The application accepts a natural language question.

## Step 2 --- PDF Semantic Retrieval

The question is embedded and compared against the persistent Chroma
vector database to retrieve relevant PDF chunks.

## Step 3 --- PDF Retrieval Evaluation

PDF results are evaluated using the configured distance threshold and
mapped to a confidence level.

## Step 4 --- Adaptive Retrieval Strategy

The evaluation selects one of three strategies:

``` text
Strong PDF evidence            → PDF_ONLY
Usable but uncertain evidence  → HYBRID (PDF + Web)
Unusable PDF evidence          → WEB_ONLY
```

This avoids unnecessary web requests when local evidence is already
strong.

## Step 5 --- Web Retrieval and Evaluation

Hybrid and Web-only strategies use Tavily. Web results are independently
evaluated using web relevance-score semantics.

PDF distance scores and Tavily relevance scores are **not directly
compared**.

## Step 6 --- Candidate Normalization

Source-specific results become a common application representation:

``` text
PDF Document + Distance ──┐
                          ├──► RetrievalCandidate
Tavily WebResult ─────────┘
```

Each candidate preserves content, source, its original retrieval score,
and citation metadata.

## Step 7 --- Cross-Source Reranking

All candidates are embedded using the same Hugging Face embedding model
and compared with the original question using cosine similarity.

``` text
RetrievalCandidate[]
        │
        ▼
Embedding Reranker
        │
        ▼
RankedCandidate[]
```

The original source-specific retrieval score remains unchanged for
traceability.

## Step 8 --- Top-K Evidence Selection

Only the strongest reranked candidates are retained according to
`HYBRID_TOP_K`.

The reranker score is used for **ordering evidence**, not as an
acceptance threshold or final confidence score.

## Step 9 --- Context Fusion

Ranked PDF and web evidence is fused into structured context while
preserving source boundaries, document titles, PDF page locations, and
web citation metadata.

## Step 10 --- Grounded Response Generation

The Groq LLM generates an answer using **only** the fused retrieval
context.

If neither PDF nor web retrieval provides acceptable evidence, the
assistant returns the Null Object response instead of guessing.

## Step 11 --- Structured Response

Every response contains:

-   Answer
-   Source (`PDF`, `Web`, `Hybrid`, or `None`)
-   Confidence
-   Citations when available

Citations are constructed only from evidence that survives reranking and
Top-K selection.

------------------------------------------------------------------------

# 📦 Release History

  -----------------------------------------------------------------------
  Version                        Description
  ------------------------------ ----------------------------------------
  **v2.5.0**                     Adaptive hybrid retrieval, normalized
                                 cross-source candidates, embedding-based
                                 reranking, Top-K evidence selection,
                                 context fusion, and hybrid responses

  **v2.4.0**                     Confidence-based retrieval evaluation,
                                 structured response models, citations,
                                 clean layered architecture, and improved
                                 answer generation

  **v2.3.0**                     Intelligent PDF-first routing with
                                 Tavily web fallback

  **v2.2.1**                     Centralized environment initialization
                                 and startup architecture improvements

  **v2.2.0**                     Initial stable modular PDF RAG
                                 implementation
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 🗺️ Roadmap

The long-term goal is to evolve this project into a production-quality
autonomous research assistant.

## ✅ v2.5.0

### Adaptive Hybrid Retrieval

-   True Hybrid Retrieval (PDF + Web)
-   Adaptive PDF-only, Hybrid, and Web-only strategies
-   Shared retrieval candidate representation
-   Embedding-based cross-source reranking
-   Ranked evidence selection
-   Configurable Hybrid Top-K
-   Structured context fusion
-   Hybrid source attribution and citations
-   Combined retrieval confidence policy
-   Simplified hybrid RAG orchestration

------------------------------------------------------------------------

## 🚀 v2.6.0

### Memory

-   Conversation memory
-   Context-aware responses
-   Multi-turn conversations

------------------------------------------------------------------------

## 🚀 v2.7.0

### Knowledge Base

-   Multiple PDF collections
-   Dynamic document indexing
-   Metadata filtering

------------------------------------------------------------------------

## 🚀 v2.8.0

### AI Agents

-   Tool Calling
-   ReAct Agents
-   Function Calling
-   External API integrations

------------------------------------------------------------------------

## 🚀 v2.9.0

### Agent Workflows

-   LangGraph workflows
-   Planning and execution
-   Multi-step reasoning

------------------------------------------------------------------------

## 🎯 v3.0.0

### Intelligent Agentic Research Assistant

-   Autonomous planning
-   Multi-agent collaboration
-   Research report generation
-   Model Context Protocol (MCP)
-   Long-term memory
-   Intelligent tool ecosystem
-   Autonomous research workflows

------------------------------------------------------------------------

# 📚 Learning Journey

This repository serves as a practical exploration of modern AI
application development and software engineering.

Topics covered throughout the project include:

-   Retrieval-Augmented Generation (RAG)
-   Adaptive Hybrid Retrieval
-   Cross-source Reranking
-   Context Fusion
-   Semantic Search
-   Vector Databases
-   Prompt Engineering
-   LangChain & LCEL
-   ChromaDB
-   Confidence-based Retrieval
-   Software Architecture
-   Design Patterns
-   AI Agents
-   LangGraph
-   Model Context Protocol (MCP)

Each release introduces meaningful capabilities while preserving a
clean, maintainable, and extensible architecture.

Rather than rapidly adding features, this project emphasizes **building
AI systems correctly**, ensuring every architectural decision supports
future growth.

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, ideas, and feedback are always welcome.

If you'd like to improve the project, feel free to:

-   ⭐ Star the repository
-   🐛 Report bugs by opening an issue
-   💡 Suggest new features
-   🔧 Submit pull requests
-   📖 Improve the documentation

Whether it's fixing a typo, improving the architecture, or proposing new
AI capabilities, every contribution is appreciated.

------------------------------------------------------------------------

# 📜 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute the project in accordance with
the license terms.

------------------------------------------------------------------------

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on
GitHub.

Your support helps others discover the project and motivates continued
development.

------------------------------------------------------------------------

# 👨‍💻 Author

**Himanshu Bhandari**

AI Engineer passionate about building production-quality AI systems with
a strong emphasis on software architecture, Retrieval-Augmented
Generation (RAG), Agentic AI, and scalable machine learning
applications.

### Connect

-   GitHub: https://github.com/hbhandari247-git
-   LinkedIn: https://www.linkedin.com/in/hbhandari247

------------------------------------------------------------------------

# 🙏 Acknowledgements

This project is built using several outstanding open-source
technologies.

Special thanks to the communities behind:

-   LangChain
-   ChromaDB
-   Hugging Face
-   Groq
-   Tavily

Their work makes modern AI application development significantly more
accessible.

------------------------------------------------------------------------

# 🚀 What's Next?

The journey doesn't end with v2.5.0.

The next release will focus on **conversation memory and context-aware
multi-turn interactions**, followed by broader knowledge-base and agent
capabilities.

Upcoming work includes:

-   Conversation Memory
-   Context-Aware Responses
-   Multi-turn Conversations
-   Multi-document Knowledge Bases
-   LangGraph Workflows
-   Autonomous AI Agents
-   Model Context Protocol (MCP)
-   Production Deployment
-   Continuous Evaluation

The goal is to evolve this repository into a complete
**production-quality Agentic AI Research Assistant** while documenting
every architectural decision along the way.

------------------------------------------------------------------------

> **"Great AI systems aren't built in a single release---they evolve
> through thoughtful architecture, continuous learning, and disciplined
> engineering."**
