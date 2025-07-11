# PubMed Paper Fetcher

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Output Format](#output-format)
- [Project Structure](#project-structure)
- [Tools and Libraries Used](#tools-and-libraries-used)
- [Development](#development)
- [Publishing](#publishing)

---

This is a command-line tool to fetch research papers from PubMed based on a user-specified query and filter those papers to identify authors affiliated with pharmaceutical or biotech companies. The output is saved as a CSV file.

## Features

- Fetch research papers using PubMed's Entrez API
- Identify papers with at least one author affiliated with a pharmaceutical or biotech company
- Output includes PubMed ID, title, publication date, non-academic authors, company affiliations, and corresponding author email
- Command-line interface with helpful options
- Uses typed, modular Python with good error handling
- Designed for performance and code clarity

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1. Clone the repository:

```bash
git clone https://github.com/miniware9/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher
```

2. Install Poetry (if not already installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
# Then run:
source $HOME/.poetry/env
```

3. Install dependencies:

```bash
poetry install
```

## Usage

After installing dependencies, run:

```bash
poetry run get-papers-list "your search query here" [options]
```

### Options

- `-f`, `--file`: Specify output CSV filename. If not provided, output is printed to the console.
- `-d`, `--debug`: Print debug logs during execution.
- `-h`, `--help`: Show usage instructions.

### Example

```bash
poetry run get-papers-list "mRNA vaccine" -f results.csv -d
```

## Output Format

The CSV (or console) output contains the following columns:

- **PubmedID**: Unique identifier of the paper
- **Title**: Title of the paper
- **Publication Date**: Date the paper was published
- **Non-academic Author(s)**: Author names affiliated with non-academic institutions
- **Company Affiliation(s)**: Company or industry-related affiliations
- **Corresponding Author Email**: Email of the corresponding author (if available)

## Project Structure

```
pubmed-paper-fetcher/
├── pyproject.toml
├── README.md
├── src/
│   └── pubmed_paper_fetcher/
│       ├── __init__.py
│       ├── fetch.py         # Core logic for fetching and filtering papers
│       └── cli.py           # Command-line interface entry point
```

## Tools and Libraries Used

- `requests` – HTTP library for API calls
- `lxml` – XML parsing
- `Poetry` – Dependency and packaging tool
- `PubMed Entrez API` – Source of research data

## Development

- Typed Python is used throughout (mypy compatible)
- Code is modular and testable
- Errors are handled gracefully
- Pagination is implemented for large queries using `retstart`
- For `efetch`, GET is used when fetching ≤ 200 records, and POST is used for > 200

> Note: `retmax=10000` is used to retrieve the maximum number of PubMed IDs per `esearch` call. If the result count exceeds 10,000, the tool paginates using `retstart` to fetch remaining records in batches of 10,000. This ensures completeness without exceeding API limits.


---
