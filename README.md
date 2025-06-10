# Research Assistant: arXiv AI Paper Fetcher

This script fetches, filters, and downloads the latest AI research papers from arXiv based on your topic preferences using a zero-shot classifier.

## Agentic AI Process

This project embodies an **agentic AI workflow**—a modular, autonomous pipeline that simulates the behavior of a research assistant agent. The system operates in the following stages:

1. **Autonomous Information Gathering:**
   - The agent proactively queries arXiv for the latest research in artificial intelligence, ensuring up-to-date coverage of the field.

2. **Intelligent Relevance Assessment:**
   - Leveraging a zero-shot language model, the agent evaluates each paper's abstract against user-defined preferences (e.g., "finance", "LLM", "machine learning").
   - Each paper is assigned a relevance score, simulating a decision-making process akin to a human research assistant prioritizing reading material.

3. **Selective Curation and Action:**
   - Only papers surpassing a configurable relevance threshold are selected for download, optimizing for quality over quantity.
   - The agent autonomously downloads the full PDF of each relevant paper, organizing them for easy access.

4. **Extensible and Modular Reasoning:**
   - The pipeline is designed for extensibility: new modules (e.g., summarization, citation extraction, or advanced ranking) can be added to enhance the agent's capabilities.
   - Each stage is encapsulated in its own module, allowing the agent to be upgraded or specialized for different research domains.

5. **Human-in-the-Loop and Automation:**
   - The agent can operate fully autonomously or with human guidance (via CLI arguments or Makefile targets), supporting both batch and interactive research workflows.

This agentic process transforms the traditional, manual literature review into an automated, intelligent, and scalable research workflow—empowering users to focus on insight and discovery rather than information overload.

## Setup

1. **Create a virtual environment (recommended):**
   ```sh
   python3.13 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

Or, use the Makefile for all steps:

```sh
make install
```

## Usage

- **Run the pipeline:**
  ```sh
  make run
  ```
  This fetches, filters, and downloads relevant papers (default: 10, preferences: finance, llm, machine learning).

- **Open all downloaded PDFs:**
  ```sh
  make open
  ```

- **Custom run:**
  Activate your venv, then run:
  ```sh
  python main.py --num-papers 20 --preferences "llm,finance" --threshold 0.7
  ```

**Note:** Always activate your venv before running Python commands if not using the Makefile. 