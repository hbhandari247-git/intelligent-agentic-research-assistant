# 🚀 Fresh Laptop Setup Guide: Intelligent Agentic Research Assistant

This guide walks you through setting up, configuring, and running the **Intelligent Agentic Research Assistant** from scratch on a clean/fresh machine (macOS, Linux, or Windows).

---

## 📋 Table of Contents
1. [System Prerequisites](#1-system-prerequisites)
2. [Get Your API Keys](#2-get-your-api-keys)
3. [Clone and Setup Workspace](#3-clone-and-setup-workspace)
4. [Python Environment & Dependencies](#4-python-environment--dependencies)
5. [Configure Environment Variables (`.env`)](#5-configure-environment-variables-env)
6. [Configure LLM Provider & Routing (`config/settings.py`)](#6-configure-llm-provider--routing-configsettingspy)
7. [Running the Application](#7-running-the-application)
8. [Running Automated Tests](#8-running-automated-tests)
9. [Project Directory Structure](#9-project-directory-structure)
10. [Troubleshooting & FAQs](#10-troubleshooting--faqs)

---

## 1. System Prerequisites

Ensure your new machine has the following tools installed:

- **Git**: [git-scm.com](https://git-scm.com/downloads)
  ```bash
  git --version
  ```
- **Python 3.10 or 3.11** (Python 3.11 is recommended):
  ```bash
  python3 --version
  # or on Windows:
  python --version
  ```
- **(Optional) Docker Desktop**: [docker.com](https://www.docker.com/products/docker-desktop/) *(Only needed if you run the local OmniRoute AI proxy gateway container).*

---

## 2. Get Your API Keys

You will need two free API keys to enable the LLM and live web search tools:

1. **Groq Cloud API Key** *(for LLM generation & tool routing)*:
   - Sign up for a free account at [console.groq.com](https://console.groq.com/).
   - Go to **API Keys** $\rightarrow$ Create a key $\rightarrow$ Copy the key (starts with `gsk_...`).
2. **Tavily API Key** *(for live internet search & fallback routing)*:
   - Sign up for a free account at [app.tavily.com](https://app.tavily.com/).
   - Copy your default API key (starts with `tvly-...`).
3. *(Optional)* **Hugging Face Access Token** *(prevents rate limit warnings when downloading embedding model weights)*:
   - Create a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

---

## 3. Clone and Setup Workspace

Open your terminal, navigate to your desired directory, and clone the repository:

```bash
git clone https://github.com/hbhandari247-git/intelligent-agentic-research-assistant.git
cd intelligent-agentic-research-assistant
```

---

## 4. Python Environment & Dependencies

### Step 4.1: Create a Python Virtual Environment
Creating a virtual environment ensures all libraries remain isolated and don't conflict with system packages.

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

*(You will see `(venv)` appear at the start of your terminal prompt indicating the virtual environment is active).*

---

### Step 4.2: Install Required Packages
Upgrade `pip` and install all necessary dependencies (LangChain, ChromaDB, Sentence-Transformers, PyPDF, CrewAI, etc.):

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(Note: The initial download includes Hugging Face embedding weights and takes ~1-2 minutes depending on your network speed).*

---

## 5. Configure Environment Variables (`.env`)

Copy the provided template `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

Open `.env` in any text editor and paste your credentials:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
TAVILY_API_KEY=tvly-your_actual_tavily_api_key_here

# Optional:
# HF_TOKEN=hf_your_actual_token_here
```

> ⚠️ **Important:** The `.env` file is already listed in `.gitignore` so your private API keys will never be accidentally pushed to Git.

---

## 6. Configure LLM Provider & Routing (`config/settings.py`)

Open `config/settings.py` to inspect or toggle between **Direct Groq Cloud Mode** and **Local OmniRoute Gateway Mode**:

```python
# ============================================================
# Mode A: Direct Groq Cloud (Standard / Default for Fresh Machines)
# ============================================================
USE_OMNIROUTE = False
MODEL_NAME = "llama-3.3-70b-versatile"  # or "llama3-8b-8192"

# ============================================================
# Mode B: Local OmniRoute Gateway (When Docker container is running)
# ============================================================
USE_OMNIROUTE = True
MODEL_NAME = "openai/gpt-oss-120b"
```

* **Embedding Model Setting:** 
  The default embedding model is set to `"BAAI/bge-small-en-v1.5"`:
  ```python
  EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
  ```

---

## 7. Running the Application

Make sure your virtual environment is active (`source venv/bin/activate`), then start the application:

```bash
python app.py
```

### Initial Run & Collection Selection
1. On initial startup, the application discovers all folders inside `data/`:
   ```text
   📂 Discovering document collections...
   ✅ Pipeline initialized.

   📚 Available collections:
   1. finance (1 documents)
   2. legal (1 documents)
   3. medical (2 documents)
   4. research (3 documents)

   Select a collection: 4
   ```
2. Type `4` and press Enter to select the **`research`** collection *(which includes `Attention_is_All_You_Need.pdf`, `BERT.pdf`, and `NEURAL_MACHINE_TRANSLATION.pdf`)*.
3. The embedding engine will vectorize and store the document chunks in `db/research_vector_store`.

---

### Interactive Main Menu Walkthrough

```text
🤖 Intelligent Agentic Research Assistant
📚 Active Collection: research
------------------------------------------
1. Start Interactive Q&A Chat Session
2. Start Autonomous Research & Report Generation (v3.0.0)
3. View Past Research Reports Logs (LTM)
4. Update Research Style Preferences (LTM)
5. Change Document Collection
6. Rebuild Current Collection Index
7. Clear Conversational Memory
8. Exit
------------------------------------------
```

| Option | Feature | Description |
| :--- | :--- | :--- |
| **`1`** | **Conversational RAG Chat** | Multi-turn conversational Q&A with pronoun resolution, citation tracking, and dynamic fallback to Tavily live web search. Type `exit` to return to menu or `clear` to reset chat memory. |
| **`2`** | **Autonomous Research Crew** | CrewAI multi-agent team (Planner, Specialist, Synthesizer) performs deep research on a topic, compiles a structured report, and saves it to `outputs/`. |
| **`3`** | **View Past Reports (LTM)** | Reads and displays previously generated research reports from SQLite database (`db/memory.db`). |
| **`4`** | **Update Preferences (LTM)** | Adjusts agent tone, output depth (`brief` / `detailed` / `comprehensive`), and style (`technical` / `concise`) stored in SQLite memory. |
| **`5`** | **Change Collection** | Switch between `finance`, `legal`, `medical`, and `research` collections on the fly. |
| **`6`** | **Rebuild Index** | Force-deletes existing vector database cache and re-indexes the collection from raw PDF documents. |
| **`7`** | **Clear Memory** | Clears short-term conversational message history buffer. |
| **`8`** | **Exit** | Cleanly terminates the application session. |

---

## 8. Running Automated Tests

Run the full pytest suite to verify all 25 unit tests pass on your machine:

```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run a specific test module:
```bash
pytest tests/test_agent_workflow.py -v
```

---

## 9. Project Directory Structure

```text
intelligent-agentic-research-assistant/
├── app.py                      # Main Interactive CLI Application Entry Point
├── config/
│   └── settings.py             # Global constants, LLM & embedding configurations
├── data/                       # Local document repositories by category
│   ├── finance/
│   ├── legal/
│   ├── medical/
│   └── research/               # Attention Is All You Need, BERT, NMT PDFs
├── db/                         # Persistent storage (Chroma Vector DBs & SQLite memory.db)
├── models/                     # Strongly-typed Pydantic & dataclass domain models
├── services/                   # Core pipeline & agent services
│   ├── agent.py                # ReAct orchestrator loop
│   ├── agent_planner.py        # Planning & tool selection interface
│   ├── tool_selector.py        # Routing mini-agent (PDF vs Web search selection)
│   ├── question_rewriter.py    # Multi-turn context resolution & query rewriter
│   ├── retriever.py            # ChromaDB vector retrieval & MMR search
│   ├── reranker.py             # Cosine similarity reranker
│   ├── generator.py            # Grounded generation with citation synthesis
│   ├── crew_service.py         # CrewAI autonomous multi-agent research workflow
│   └── memory_service.py       # SQLite Long-Term Memory (LTM) database operations
├── study_guides/               # Presentation & concept study guides (viewer.html)
├── tests/                      # Automated unit test suite (25 test cases)
├── .env.example                # Sample environment file template
├── requirements.txt            # Python dependencies
└── Setup.md                    # This setup guide
```

---

## 10. Troubleshooting & FAQs

### Q1: Warning: "You are sending unauthenticated requests to the HF Hub"
* **Explanation:** Hugging Face issues a mild warning when downloading open weights anonymously.
* **Fix:** You can safely ignore this. If you want faster download speeds or to suppress the message, generate a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and add `HF_TOKEN=hf_...` in your `.env` file.

---

### Q2: Error connecting to `http://localhost:20128/v1` (OmniRoute Gateway)
* **Explanation:** `config/settings.py` has `USE_OMNIROUTE = True`, but the local Docker container is not running on your new laptop.
* **Fix:** Either:
  1. Open `config/settings.py` and set `USE_OMNIROUTE = False` to call Groq directly over the cloud.
  2. Or start your local OmniRoute docker container on port `20128`.

---

### Q3: How do I force re-index after adding new PDFs?
* **Fix:** Launch `python app.py` and choose **Option 6 (Rebuild Current Collection Index)**. Alternatively, you can delete the corresponding folder inside `db/` (e.g. `rm -rf db/research_vector_store`) and restart `app.py`.

---

### Q4: Pytest shows warnings for CrewAI / function calling
* **Explanation:** CrewAI internal deprecation warnings for future version upgrades.
* **Fix:** These warnings are harmless and can be ignored. All tests pass with exit code `0`.

---

🎉 **You are all set! Happy Researching!**
