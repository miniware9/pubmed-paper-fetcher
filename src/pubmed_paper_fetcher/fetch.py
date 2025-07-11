# src/pubmed_paper_fetcher/fetch.py

import requests
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET
import re

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str, retmax: int = 10000, debug: bool = False) -> List[str]:
    """Fetch PubMed IDs matching a query."""
    url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": retmax
    }
    if debug:
        print(f"[DEBUG] Querying PubMed for IDs: {url} with {params}")

    response = requests.get(url, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.content)

    return [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text]


def fetch_papers_metadata(pubmed_ids: List[str], debug: bool = False) -> List[Dict]:
    """
    Fetch metadata for a list of PubMed IDs and return relevant paper details.
    Uses GET if <= 200 IDs, otherwise POST.
    """
    if not pubmed_ids:
        return []

    url = f"{BASE_URL}efetch.fcgi"
    ids_str = ",".join(pubmed_ids)
    method = "GET" if len(pubmed_ids) <= 200 else "POST"

    params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": ids_str
    }

    if debug:
        print(f"[DEBUG] Fetching metadata for {len(pubmed_ids)} papers using {method}")

    if method == "GET":
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, data=params)

    response.raise_for_status()
    root = ET.fromstring(response.content)
    articles = root.findall(".//PubmedArticle")

    return [extract_paper_details(article) for article in articles if article is not None]


def extract_paper_details(article: ET.Element) -> Dict:
    """Extract details from one PubMedArticle XML element."""
    title_elem = article.find(".//ArticleTitle")
    pub_date_elem = article.find(".//PubDate")
    year = pub_date_elem.findtext("Year") if pub_date_elem is not None else "Unknown"
    month = pub_date_elem.findtext("Month") or ""
    day = pub_date_elem.findtext("Day") or ""
    pub_date = f"{year}-{month}-{day}".strip("-")

    non_academic_authors = []
    companies = []

    author_list = article.findall(".//Author")
    for author in author_list:
        last_name = author.findtext("LastName") or ""
        aff_info = author.findall(".//AffiliationInfo")
        for aff in aff_info:
            aff_text = aff.findtext("Affiliation") or ""
            if is_company_affiliation(aff_text):
                companies.append(aff_text)
                if last_name:
                    non_academic_authors.append(last_name)

    affiliations = article.findall(".//AffiliationInfo")
    email = extract_email_from_affiliations(affiliations)

    return {
        "PubmedID": article.findtext(".//PMID") or "",
        "Title": title_elem.text if title_elem is not None else "",
        "Publication Date": pub_date,
        "Non-academic Author(s)": "; ".join(non_academic_authors),
        "Company Affiliation(s)": "; ".join(companies),
        "Corresponding Author Email": email or ""
    }


def is_company_affiliation(affiliation: str) -> bool:
    """Heuristic to determine if an affiliation is non-academic (e.g., company)."""
    academic_keywords = ["university", "hospital", "college", "institute", "school"]
    company_keywords = ["pharma", "biotech", "inc", "corp", "ltd", "gmbh", "s.a."]

    aff_lower = affiliation.lower()
    return any(kw in aff_lower for kw in company_keywords) and not any(kw in aff_lower for kw in academic_keywords)


def extract_email_from_affiliations(affiliations) -> Optional[str]:
    """Attempt to extract an email from the affiliation text."""
    for aff in affiliations:
        text = aff.findtext("Affiliation") or ""
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        if match:
            return match.group(0)
    return None
