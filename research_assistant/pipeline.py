from .arxiv import fetch_arxiv_ai_papers
from .relevance import RelevanceScorer
from .pdf import download_pdf, open_pdf
from pathlib import Path
import json

def get_arxiv_id(link: str) -> str:
    return link.rstrip("/").split("/")[-1]

def save_papers(papers, output_dir="papers"):
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    filename = output_path / f"arxiv_ai_papers.json"
    with open(filename, "w") as f:
        json.dump(papers, f, indent=2)
    print(f"Papers saved to {filename}")

def run_pipeline(num_papers, preferences, threshold, open_pdfs=False):
    scorer = RelevanceScorer(preferences, threshold)
    papers = fetch_arxiv_ai_papers(num_papers)
    relevant_papers = []
    for paper in papers:
        score = scorer.score(paper["summary"])
        if score >= threshold:
            arxiv_id = get_arxiv_id(paper["link"])
            pdf_path = download_pdf(arxiv_id)
            paper["relevance_score"] = score
            paper["pdf_path"] = pdf_path
            relevant_papers.append(paper)
            if open_pdfs and pdf_path:
                open_pdf(pdf_path)
        else:
            print(f"Skipping '{paper['title']}' (score: {score:.2f})")
    save_papers(relevant_papers) 