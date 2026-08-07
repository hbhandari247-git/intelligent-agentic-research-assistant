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
-   📚 Multiple document collections
-   🗂️ Dynamic collection discovery
-   ♻️ Automatic document index rebuilding
-   📄 Generic document loading pipeline
-   📑 Manifest-based index synchronization
-   📝 Fully typed and documented codebase
-   💬 Context-aware multi-turn conversations
-   🧠 Bounded in-session conversation memory
-   ✍️ Standalone question rewriting for follow-up retrieval
-   🔗 Pronoun and conversational reference resolution
-   🛡️ Unresolved-context detection before retrieval
-   🧹 Conversation memory reset with the `clear` command
-   🧪 Unit and external integration test coverage with pytest
-   🔄 Extensible architecture for future AI capabilities

------------------------------------------------------------------------

# 🎯 Current Release

## **v2.8.0 -- Modular AI Agent Architecture & Tool Calling**

### ✨ Highlights

-   💬 Context-aware multi-turn conversations
-   🧠 Bounded in-session conversation memory
-   ✍️ Follow-up questions rewritten into standalone retrieval queries
-   🔗 Pronoun and conversational reference resolution
-   🛡️ Unresolved-context detection before PDF or Web retrieval
-   🧹 `clear` command for resetting session memory
-   🏗️ Dedicated `ConversationService` orchestration layer
-   🧩 Typed `ConversationMessage` and `RewriteResult` models
-   🧪 Deterministic memory unit tests plus Groq and Tavily integration
    tests
-   🔀 Full compatibility with the v2.5.0 adaptive hybrid retrieval
    pipeline

### What's New in v2.6.0?

v2.6.0 adds a conversational layer in front of the adaptive hybrid RAG
pipeline. The assistant now retains a bounded window of recent user and
assistant messages and uses that history to resolve follow-up questions
before retrieval.

For example, after answering `Who is the CEO of OpenAI?`, the follow-up
`What company does he lead?` can be rewritten as a standalone question
such as `What company does Sam Altman lead?` before entering retrieval.

The rewriter also detects questions that depend on missing context.
After memory is cleared, an ambiguous question such as
`What company does he lead?` is stopped before Chroma or Tavily
retrieval and the assistant asks the user to clarify the missing
reference instead of searching an underspecified query.

Conversation behavior is coordinated by `ConversationService`, keeping
the command-line interface focused on input, commands, and response
rendering while preserving the existing PDF-only, Hybrid, and Web-only
retrieval strategies introduced in v2.5.0.

------------------------------------------------------------------------

# 🏛️ System Architecture

``` text
                              User Question
                                   │
                                   ▼
                                  app.py
                                   │
                                   ▼
                         ConversationService
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                 ConversationMemory   Question Rewriter
                         │                   │
                         │             RewriteResult
                         │                   │
                         └─────────┬─────────┘
                                   │
                         resolved? │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
               unresolved                    resolved
                    │                             │
                    ▼                             ▼
          Ask user to clarify              route_question()
                                                  │
                                                  ▼
                                         answer_from_hybrid()
                                                  │
                                                  ▼
                                      PDF Retrieval + Evaluation
                                                  │
                                                  ▼
                                         Retrieval Strategy
                                  ┌───────────────┼───────────────┐
                                  ▼               ▼               ▼
                               PDF_ONLY         HYBRID          WEB_ONLY
                                  │               │               │
                                  │               ▼               ▼
                                  │        Tavily Web Search  Tavily Web Search
                                  └───────────────┼───────────────┘
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
                                      ┌───────────┴───────────┐
                                      ▼                       ▼
                                   Context                 Citations
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
                                      │
                                      ▼
                         Update ConversationMemory
```

The application separates conversational orchestration from retrieval
and generation responsibilities.

-   **Conversation Service** coordinates context resolution, retrieval
    routing, and memory updates.
-   **Conversation Memory** stores a bounded in-session history of typed
    user and assistant messages.
-   **Question Rewriter** converts contextual follow-ups into standalone
    retrieval questions and identifies missing conversational context.
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
-   **Router** delegates resolved standalone questions to the hybrid RAG
    workflow.
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
│   ├── conversation_message.py
│   ├── confidence.py
│   ├── ranked_candidate.py
│   ├── response.py
│   ├── rewrite_result.py
│   ├── retrieval_candidate.py
│   ├── retrieval_evaluation.py
│   ├── retrieval_strategy.py
│   ├── source.py
│   └── web_result.py
├── services/
│   ├── __init__.py
│   ├── candidate_builder.py
│   ├── context_fusion.py
│   ├── conversation.py
│   ├── conversation_memory.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── evaluator.py
│   ├── generator.py
│   ├── hybrid_rag.py
│   ├── llm.py
│   ├── pipeline.py
│   ├── question_rewriter.py
│   ├── rag.py
│   ├── reranker.py
│   ├── retrieval_strategy.py
│   ├── retriever.py
│   ├── router.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   ├── web_rag.py
│   └── web_search.py
├── tests/
│   ├── __init__.py
│   ├── test_conversation_memory.py
│   ├── test_rewriter.py
│   └── test_tavily.py
├── requirements.txt
├── README.md
├── LICENSE
└── .env
```

### Directory Overview

  -----------------------------------------------------------------------
  Directory                           Purpose
  ----------------------------------- -----------------------------------
  `config/`                           Centralized application
                                      configuration

  `models/`                           Domain models used throughout the
                                      application

  `services/`                         Business logic and application
                                      services

  `db/`                               Persistent Chroma vector databases
                                      (one per collection)

  `data/`                             Collection-based local knowledge
                                      base

  `tests/`                            Deterministic unit tests and opt-in
                                      external integration tests
  -----------------------------------------------------------------------

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
-   Conversation memory limit (`MAX_CONVERSATION_MESSAGES`)

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

During a session:

-   Type `exit` to quit.
-   Type `clear` to reset conversation memory without restarting the
    application.

------------------------------------------------------------------------

# 💬 Example Session

``` text
🤖 Intelligent Agentic Research Assistant
Type 'exit' to quit.
Type 'clear' to clear conversation memory.

You: What is self-attention?

Self-attention is an attention mechanism that relates different positions
of a sequence in order to compute a representation of that sequence.

Source: PDF
Confidence: High

You: Why is it useful?

Self-attention is useful because it can directly model relationships
between positions in the sequence and supports parallel computation.

Source: PDF
Confidence: High

You: Who is the CEO of OpenAI?

Sam Altman is the CEO of OpenAI.

Source: Web
Confidence: Very High

You: What company does he lead?

Sam Altman is the CEO of OpenAI.

Source: Web
Confidence: High

You: clear

🧹 Conversation memory cleared.

You: What company does he lead?

I need more context to understand your question. Please clarify what
you are referring to.
```

The follow-up question is rewritten internally for retrieval while the
original user message is retained in conversation memory. After `clear`,
the missing reference is detected before retrieval.

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

### Conversation Memory

-   Maximum retained conversation messages (`MAX_CONVERSATION_MESSAGES`)
-   The limit must be positive and even so normal history windows
    preserve complete user/assistant exchanges

### Storage

-   Persistent Chroma database path
-   PDF document location

Centralizing these settings makes experimentation straightforward
without requiring changes throughout the codebase.

------------------------------------------------------------------------

# 🧠 How It Works

The assistant combines a conversational resolution layer with the
adaptive hybrid retrieval workflow introduced in v2.5.0.

## Step 1 --- User Question

The CLI accepts a natural-language question and passes it to
`ConversationService`.

## Step 2 --- Conversation Context Resolution

Recent bounded conversation history is supplied to the question
rewriter. The rewriter determines whether the current question has
enough context to be understood.

If a required conversational reference cannot be resolved, retrieval is
skipped and the assistant asks the user to clarify.

## Step 3 --- Standalone Question Rewriting

Resolved follow-up questions are rewritten into standalone retrieval
queries while preserving the user's intent. Standalone questions remain
standalone.

## Step 4 --- PDF Semantic Retrieval

The resolved question is embedded and compared against the persistent
Chroma vector database to retrieve relevant PDF chunks.

## Step 5 --- PDF Retrieval Evaluation

PDF results are evaluated using the configured distance threshold and
mapped to a confidence level.

## Step 6 --- Adaptive Retrieval Strategy

The evaluation selects one of three strategies:

``` text
Strong PDF evidence            → PDF_ONLY
Usable but uncertain evidence  → HYBRID (PDF + Web)
Unusable PDF evidence          → WEB_ONLY
```

This avoids unnecessary web requests when local evidence is already
strong.

## Step 7 --- Web Retrieval and Evaluation

Hybrid and Web-only strategies use Tavily. Web results are independently
evaluated using web relevance-score semantics. PDF distance scores and
Tavily relevance scores are **not directly compared**.

## Step 8 --- Candidate Normalization

Source-specific results become a common application representation:

``` text
PDF Document + Distance ──┐
                          ├──► RetrievalCandidate
Tavily WebResult ─────────┘
```

Each candidate preserves content, source, its original retrieval score,
and citation metadata.

## Step 9 --- Cross-Source Reranking

All candidates are embedded using the same Hugging Face embedding model
and compared with the standalone question using cosine similarity.

## Step 10 --- Top-K Evidence Selection

Only the strongest reranked candidates are retained according to
`HYBRID_TOP_K`. The reranker score orders evidence; it is not used as
the final confidence score.

## Step 11 --- Context Fusion

Ranked PDF and web evidence is fused into structured context while
preserving source boundaries and citation metadata.

## Step 12 --- Grounded Response Generation

The Groq LLM generates an answer using the fused retrieval context. If
neither PDF nor web retrieval provides acceptable evidence, the
assistant returns the Null Object response instead of guessing.

## Step 13 --- Memory Update

After a resolved interaction completes, the original user question and
generated assistant answer are stored in bounded in-session memory.
Internal rewritten questions are not stored as user messages.

## Step 14 --- Structured Response

Every retrieval response contains:

-   Answer
-   Source (`PDF`, `Web`, `Hybrid`, or `None`)
-   Confidence
-   Citations when available

------------------------------------------------------------------------

# 🧪 Testing

The project uses pytest for deterministic unit tests and opt-in external
integration tests.

Run the normal test suite:

``` bash
pytest -v
```

LLM and Tavily tests are skipped by default so normal tests do not
depend on external API calls. To explicitly run all external integration
tests:

``` bash
RUN_LLM_TESTS=true RUN_TAVILY_TESTS=true pytest -v
```

The v2.6.0 validation suite covers bounded memory behavior,
context-aware question rewriting, unresolved references, conversational
follow-ups, and Tavily result structure/relevance.

------------------------------------------------------------------------

# 📦 Release History

  ---------------------------------------------------------------------
  Version                       Description
  ----------------------------- ---------------------------------------
  **v2.6.0**                    Bounded in-session conversation memory,
                                context-aware question rewriting,
                                follow-up reference resolution,
                                unresolved-context detection, memory
                                reset, conversation orchestration, and
                                pytest validation

  **v2.5.0**                    Adaptive hybrid retrieval, normalized
                                cross-source candidates,
                                embedding-based reranking, Top-K
                                evidence selection, context fusion, and
                                hybrid responses

  **v2.4.0**                    Confidence-based retrieval evaluation,
                                structured response models, citations,
                                clean layered architecture, and
                                improved answer generation

  **v2.3.0**                    Intelligent PDF-first routing with
                                Tavily web fallback

  **v2.2.1**                    Centralized environment initialization
                                and startup architecture improvements

  **v2.2.0**                    Initial stable modular PDF RAG
                                implementation
  ---------------------------------------------------------------------

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

## ✅ v2.6.0

### Conversation Memory & Context-Aware Interactions

-   Bounded in-session conversation memory
-   Typed user and assistant conversation messages
-   Context-aware responses
-   Multi-turn conversations
-   Standalone follow-up question rewriting
-   Pronoun and reference resolution
-   Unresolved-context detection before retrieval
-   Graceful clarification for missing context
-   `clear` command for resetting memory
-   Dedicated conversation orchestration service
-   Unit and external integration testing

------------------------------------------------------------------------

## ✅ v2.7.0

### Multi-Collection Knowledge Base

-   Multiple PDF collections
-   Dynamic collection discovery
-   Automatic document indexing
-   Manifest-based index synchronization
-   Dedicated IndexManager
-   Collection-aware vector databases

------------------------------------------------------------------------

## ✅ v2.8.0

### Agent Architecture & Tool Calling

-   Modular AI Agent architecture
-   Agent state management
-   Tool registry
-   Tool planner
-   Tool runtime
-   Tool execution pipeline
-   PDF knowledge tool
-   Web search tool
-   Knowledge abstraction layer
-   External Tavily web search integration
-   Foundation for ReAct and function calling

------------------------------------------------------------------------

## 🚀 v2.9.0

### Intelligent Agents

-   LLM-powered tool selection
-   Function calling
-   ReAct reasoning
-   Dynamic tool execution
-   Observation handling
-   Multi-step planning

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
-   Conversation Memory
-   Context-Aware Question Rewriting
-   Multi-Turn Interaction Design
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

v2.8.0 introduces a modular AI Agent architecture with tool calling, an agent planner, tool runtime, tool execution pipeline, and dedicated PDF and Web tools. The next release focuses on intelligent planning through LLM-powered tool selection, ReAct reasoning, and function calling.

Upcoming work includes:

-   Multi-document Knowledge Bases
-   Dynamic document indexing
-   Metadata filtering
-   LangGraph Workflows
-   Autonomous AI Agents
-   Model Context Protocol (MCP)
-   Production Deployment
-   Continuous Evaluation
-   Longer-term and persistent memory in a future release

The goal is to evolve this repository into a complete
**production-quality Agentic AI Research Assistant** while documenting
every architectural decision along the way.

------------------------------------------------------------------------

> **"Great AI systems aren't built in a single release---they evolve
> through thoughtful architecture, continuous learning, and disciplined
> engineering."**
