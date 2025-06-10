import requests
from pathlib import Path
import os

def download_pdf(arxiv_id: str, output_dir: str = "papers/pdfs") -> str:
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    output_path = Path(output_dir)
    try:
        output_path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        print(f"Error creating directory {output_dir}: {e}")
        return ""
    pdf_file = output_path / f"{arxiv_id}.pdf"
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(pdf_file, "wb") as f:
            f.write(response.content)
        print(f"Downloaded PDF: {pdf_file}")
        return str(pdf_file)
    except Exception as e:
        print(f"Error downloading PDF for {arxiv_id}: {e}")
        return ""

def open_pdf(pdf_path: str):
    try:
        os.system(f"open '{pdf_path}'")  # macOS; use xdg-open for Linux, start for Windows
    except Exception as e:
        print(f"Error opening PDF {pdf_path}: {e}") 