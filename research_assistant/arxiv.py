import feedparser
from typing import List, Dict

def fetch_arxiv_ai_papers(num_papers: int = 5) -> List[Dict]:
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