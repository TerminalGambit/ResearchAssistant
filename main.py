import argparse
from research_assistant.pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Fetch, filter, and download relevant arXiv AI papers.")
    parser.add_argument("--num-papers", type=int, default=5, help="Number of latest AI papers to fetch from arXiv")
    parser.add_argument("--preferences", type=str, default="finance,llm,machine learning", help="Comma-separated list of user preferences (topics)")
    parser.add_argument("--threshold", type=float, default=0.5, help="Minimum relevance score (0-1) to download a paper")
    parser.add_argument("--open", action="store_true", help="Open downloaded PDFs after download")
    args = parser.parse_args()

    preferences = [p.strip() for p in args.preferences.split(",") if p.strip()]
    run_pipeline(args.num_papers, preferences, args.threshold, open_pdfs=args.open)

if __name__ == "__main__":
    main() 