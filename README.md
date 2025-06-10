# Research Assistant: arXiv AI Paper Fetcher

This script fetches, filters, and downloads the latest AI research papers from arXiv based on your topic preferences using a zero-shot classifier.

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