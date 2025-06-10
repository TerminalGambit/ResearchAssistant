#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import feedparser
import requests
from transformers import pipeline


class ResearchAssistant:
    """
    Minimalist assistant to fetch, filter, and store the latest AI research papers from arXiv.
    Uses a zero-shot classifier to filter papers by user preferences.
    """

    def __init__(self, preferences: List[str], threshold: float = 0.5):
        self.preferences = preferences
        self.threshold = threshold
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )

    def fetch_arxiv_ai_papers(self, num_papers: int = 5) -> List[Dict]:
        """
        Fetch the latest AI research papers from arXiv (cs.AI category).
        Returns a list of dictionaries with paper metadata.
        """
        feed_url = "http://export.arxiv.org/rss/cs.AI"
        papers = []
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:num_papers]:
                papers.append(
                    {
                        "title": entry.title,
                        "authors": entry.get("author", "Unknown"),
                        "summary": entry.summary,
                        "published": entry.published,
                        "link": entry.link,
                    }
                )
            return papers
        except Exception as e:
            print(f"Error fetching arXiv papers: {e}")
            return []

    def evaluate_relevance(self, summary: str) -> float:
        """
        Use zero-shot classification to score the relevance of a paper summary.
        Returns the highest score among the preferences.
        """
        result = self.classifier(summary, candidate_labels=self.preferences)
        return max(result["scores"])

    def get_arxiv_id(self, link: str) -> str:
        """
        Extract the arXiv ID from the paper link.
        """
        return link.rstrip("/").split("/")[-1]

    def download_pdf(self, arxiv_id: str, output_dir: str = "papers/pdfs") -> str:
        """
        Download the PDF for a given arXiv ID. Returns the file path if successful, else ''.
        """
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

    def filter_and_download(
        self, papers: List[Dict], output_dir: str = "papers"
    ) -> List[Dict]:
        """
        Filter papers by relevance and download PDFs for relevant ones.
        Returns the list of relevant papers (with PDF path if downloaded).
        """
        relevant_papers = []
        for paper in papers:
            score = self.evaluate_relevance(paper["summary"])
            if score >= self.threshold:
                arxiv_id = self.get_arxiv_id(paper["link"])
                pdf_path = self.download_pdf(arxiv_id, output_dir=output_dir + "/pdfs")
                paper["relevance_score"] = score
                paper["pdf_path"] = pdf_path
                relevant_papers.append(paper)
            else:
                print(f"Skipping '{paper['title']}' (score: {score:.2f})")
        return relevant_papers

    def save_papers(self, papers: List[Dict], output_dir: str = "papers"):
        """
        Save the fetched papers to a JSON file in the specified directory.
        Ensures the directory exists and handles file writing errors gracefully.
        Also creates/updates a symlink to the latest file for convenience (if supported).
        """
        output_path = Path(output_dir)
        try:
            output_path.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {output_dir}: {e}")
            return
        filename = f"arxiv_ai_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = output_path / filename
        try:
            with open(file_path, "w") as f:
                json.dump(papers, f, indent=2)
            print(f"Papers saved to {file_path}")
            # Create or update a symlink to the latest file (if supported)
            latest_symlink = output_path / "latest.json"
            try:
                if latest_symlink.exists() or latest_symlink.is_symlink():
                    latest_symlink.unlink()
                latest_symlink.symlink_to(file_path.name)
            except Exception as e:
                print(f"Could not create symlink to latest file: {e}")
        except Exception as e:
            print(f"Error saving papers to {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch, filter, and store the latest AI arXiv papers by relevance."
    )
    parser.add_argument(
        "--num-papers",
        type=int,
        default=5,
        help="Number of latest AI papers to fetch from arXiv",
    )
    parser.add_argument(
        "--preferences",
        type=str,
        default="finance,llm,machine learning",
        help="Comma-separated list of user preferences (topics)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Minimum relevance score (0-1) to download a paper",
    )
    args = parser.parse_args()

    preferences = [p.strip() for p in args.preferences.split(",") if p.strip()]
    assistant = ResearchAssistant(preferences, threshold=args.threshold)
    papers = assistant.fetch_arxiv_ai_papers(args.num_papers)
    if papers:
        relevant_papers = assistant.filter_and_download(papers)
        assistant.save_papers(relevant_papers)
    else:
        print("No papers found or error fetching from arXiv.")


if __name__ == "__main__":
    main()
