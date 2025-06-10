# Create virtual environment
venv:
	python3.13 -m venv venv

# Install dependencies in venv
install: venv
	. venv/bin/activate && pip install -r requirements.txt

# Run the pipeline using venv
run: venv
	. venv/bin/activate && python main.py --num-papers 10 --preferences "finance,llm,machine learning" --threshold 0.5

# Open all downloaded PDFs
open:
	open papers/pdfs/*.pdf 