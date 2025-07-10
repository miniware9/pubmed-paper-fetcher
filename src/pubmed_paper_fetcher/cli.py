# src/pubmed_paper_fetcher/cli.py

import argparse
import csv
from pubmed_paper_fetcher.fetch import fetch_pubmed_ids, fetch_papers_metadata


def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with at least one pharmaceutical/biotech-affiliated author."
    )
    parser.add_argument("query", type=str, help="Search query to fetch papers from PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the CSV output.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging.")

    args = parser.parse_args()

    if args.debug:
        print(f"[DEBUG] Running query: {args.query}")

    try:
        ids = fetch_pubmed_ids(args.query, debug=args.debug)
        if not ids:
            print("No papers found for this query.")
            return

        papers = fetch_papers_metadata(ids, debug=args.debug)
        if not papers:
            print("No qualifying papers found.")
            return

        if args.file:
            write_to_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            print_results(papers)

    except Exception as e:
        print(f"Error: {e}")


def write_to_csv(papers, filename):
    """Write results to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email"
        ])
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)


def print_results(papers):
    """Print results to console."""
    for paper in papers:
        print("=" * 80)
        for key, value in paper.items():
            print(f"{key}: {value}")
        print()
