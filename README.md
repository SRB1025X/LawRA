# ⚖️ LAWRA: THE LAW RESEARCH AGENT
MULTI-AGENT LEGAL RESEARCH COMPANION FOR
LAW STUDENTS

> A Multi-Agent AI System for Structured Legal Research, Argument Extraction, and Citation Discovery

---

## 📘 Project Overview

This project is a multi-agent legal research system designed to assist law students and legal researchers in extracting arguments, generating keywords, finding citations, and scoring sources. It automates a traditionally manual and error-prone legal workflow using **CrewAI**, **Serper**, and an LLM backend (Gemma or Gemini).

The framework supports full PDF ingestion, URL-based analysis, keyword simulation, legal document retrieval, citation tracing, and relevance scoring.

---

## 💡 Key Features

* Accepts PDF input and research angle
* Extracts legal arguments from academic papers or judgments
* Simulates keyword searches used by legal researchers
* Searches verified law databases (IJLLR, NLSJ, IJCLP, etc.)
* Follows reference trails from cited sources
* Scores sources on credibility, legal alignment, and usefulness
* Outputs summarized briefs and citation lists

---

## 🏗️ Core Technologies

### 🔗 [CrewAI](https://docs.crewai.com)

Multi-agent orchestration framework used to define agents, delegate tasks, and control task flow sequentially.

### 🤖 LLM Backends

Supports **either** of the following:

#### 1. **Gemma (via Ollama)**

* Lightweight, fast, and runs locally with Ollama
* Download using:

```bash
ollama pull gemma3:1b
```

* Ensure `ollama` is running before launching the app:

```bash
ollama run gemma3:1b
```

#### 2. **Gemini API (Google)**

* Cloud-based LLM with high performance on reasoning tasks
* Requires an API key from Google AI Studio

`.env` file setup:

```bash
GEMINI_API_KEY=your_google_gemini_key
```

In code, simply call `query_gemini(prompt)` using `google.generativeai` from the `google-generativeai` package.

---

## 📁 Project Structure

```
├── agents.py                # All agents in one place (argument extractor, search, etc.)
├── tasks.py                 # Task definitions per agent
├── tools.py                 # Custom tools using Serper and scrapers
├── llm_config.py            # Gemma or Gemini wrapper functions
├── crew.py                  # Crew definition and execution logic
├── utils.py                 # PDF/URL extractors and processing utilities
├── sample_base_paper.pdf    # Example paper for testing
├── .env                     # API keys
├── Pipfile / Pipfile.lock   # Pipenv environment config
```

---

## 📦 Installation & Setup

### 1. Clone the Repo

```bash
git clone https://github.com/Anil970198/LawRA.git
cd LawRA
```

### 2. Setup Pipenv Environment

```bash
pipenv --python 3.11
pipenv install crewai crewai-tools ollama python-dotenv PyPDF2 requests
pipenv shell
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
SERPER_API_KEY=your_serper_key
GEMINI_API_KEY=your_gemini_key   # Optional if using Gemini
```

---

## 🧠 Agent Roles

| Agent                  | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| `argument_extractor`   | Extracts base argument and student's critique from the document |
| `keyword_generator`    | Generates legal keyword permutations after stopword filtering   |
| `legal_search_agent`   | Searches curated law sources using Serper tool                  |
| `citation_chain_agent` | Traces references in top documents for deeper sourcing          |
| `relevance_scorer`     | Scores sources by credibility, legal fit, and insight quality   |
| `citation_formatter`   | Formats citations into APA/Bluebook                             |
| `output_assembler`     | Assembles output into structured research text files            |

---

## 🖥️ How to Run

### Run from PDF:

```bash
python crew.py sample_base_paper.pdf
```

Ensure Gemma is running if used:

```bash
ollama run gemma3:1b
```

### Sample Output Files:

* `legal_research_extracted.txt`
* `legal_memo_output_final.txt`
* `legal_research.log`

---

## 🖼️ Sample Outputs

### 📌 Argument Extraction Output

![Argument Extraction Screenshot](https://github.com/Anil970198/LawRA/blob/4cfccddc61347c4c94f98c9b16870731683453d5/home%20screen.png?raw=true)

### 📌 Final Citation Breakdown Output

![Citation Results Screenshot](https://github.com/Anil970198/LawRA/blob/4cfccddc61347c4c94f98c9b16870731683453d5/results.png?raw=true)


---

## 🛣️ Future Plans

* Add a Streamlit UI for file upload + inline viewing
* Support jurisdiction toggling (India, US, UK)
* Add memory agent to personalize suggestions
* Auto-export to PDF or DOCX format

---

## 🛡️ License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* Google Gemini API (for cloud inference)
* CrewAI (for agent orchestration)
* Ollama team (for running local Gemma LLMs)
* Serper DevTool (for integrated web search)

---

## Authors

* *Shreyas* - Computer Science Student at JNTUH - [Shreyas Github](https://github.com/SRB1025X) - [Shreyas Linkedin](https://www.linkedin.com/in/srb1025x/)
* *Anil* - Computer Science Student at JNTUH - [Anil Github](https://github.com/Anil970198) - [Anil Linkedin](https://www.linkedin.com/in/mondru-anil/)
