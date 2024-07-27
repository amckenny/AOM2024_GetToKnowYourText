"""CrossRef API Functions"""

import json
from pathlib import Path
from typing import List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

SETTINGS_FILE = Path(__file__).parents[1] / "settings.json"
assert SETTINGS_FILE.exists(), f"Settings file not found at {SETTINGS_FILE}"


def get_user_agent() -> str:
    """Gets the User-Agent from settings.json

    https://api.crossref.org/swagger-ui/index.html
    >> "Good manners = more reliable service"

    Returns:
        str: User-Agent for Crossref API
    """
    with open(SETTINGS_FILE, encoding="utf8") as infile:
        json_data = infile.read()

    assert json_data, "No data in settings.json"

    settings = json.loads(json_data)
    assert "CrossRef" in settings, "CrossRef not in settings.json"
    assert "User-Agent" in settings["CrossRef"], "User-Agent not in settings.json"
    assert (
        "YourEmailHere" not in settings["CrossRef"]["User-Agent"]
    ), "Please update your email in settings.json -> CrossRef -> User-Agent"

    return settings["CrossRef"]["User-Agent"]


def get_issn_list(journals: Optional[List[str]] = None) -> List[str]:
    """Get list of journal ISSNs from settings.json. Returns all ISSNs if no journals specified.

    Args:
        journals (Optional[List[str]]): List of journals to get ISSNs for. Defaults to None.

    Returns:
        [str]: List of ISSNs
    """
    with open(SETTINGS_FILE, encoding="utf8") as infile:
        json_data = infile.read()

    assert json_data, "No data in settings.json"

    settings = json.loads(json_data)
    assert "ISSNs" in settings, "ISSNs not in settings.json"

    if journals:
        # Return ISSNs for specified journals
        return [
            issn
            for journal in settings["ISSNs"]
            for issn in settings["ISSNs"][journal]
            if journal in journals
        ]

    # Return all ISSNs if no journals specified
    return [
        issn for journal in settings["ISSNs"] for issn in settings["ISSNs"][journal]
    ]


def get_works_by_name(fname: str, lname: str, s_year: int) -> dict:
    """Get works by author name

    Args:
        fname (str): First name
        lname (str): Last name
        s_year (int): Start year

    Returns:
        dict: Works
    """
    url = "https://api.crossref.org/works?"
    url += f"query.author={fname}+{lname}"
    url += f"&filter=from-pub-date:{s_year}-01-01"
    for issn in get_issn_list():
        url += f",issn:{issn}"
    url += "&rows=1000"
    headers = {"User-Agent": get_user_agent()}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    assert (
        response.json()["status"] == "ok"
    ), f"Crossref API query failed for {fname} {lname}"

    return response.json()["message"]["items"]


def get_works_by_issn(issn: str, s_year: int) -> dict:
    """Get works by ISSN

    Args:
        issn (str): Journal ISSN
        s_year (int): Start year

    Returns:
        dict: Works
    """
    all_results = []
    total_results = 0
    current_offset = 0

    while total_results == 0 or current_offset < total_results:

        url = f"https://api.crossref.org/journals/{issn}/works?"
        url += f"filter=from-pub-date:{s_year}-01-01"
        url += "&rows=1000"
        if current_offset:
            url += f"&offset={current_offset}"
        headers = {"User-Agent": get_user_agent()}
        response = requests.get(url, headers=headers, timeout=100)
        response.raise_for_status()

        assert (
            response.json()["status"] == "ok"
        ), f"Crossref API query failed for issn: {issn}"

        all_results.extend(response.json()["message"]["items"])
        total_results = response.json()["message"]["total-results"]
        current_offset += response.json()["message"]["items-per-page"]

    return all_results


def parse_author_works_to_df(fname: str, lname: str, works: List[dict]) -> pd.DataFrame:
    """Parse works to DataFrame

    Args:
        works (dict): Works responses from Crossref API
    """
    rows = []
    for work in works:
        # If article doesn't have a title or isn't an article, skip it
        if not work.get("title") or work['type'] != 'journal-article':
            continue

        for author in work["author"]:
            if (
                fname.lower() in author.get("given","").lower()
                and lname.lower() in author.get("family", "").lower()
            ):
                break
        else:
            continue
        doi = work["DOI"]
        title = work["title"][0]
        journal = work["container-title"][0]
        abstract = work.get("abstract")
        pub_date = work["published"]["date-parts"][0][0]
        citations = work["is-referenced-by-count"]
        rows.append((fname, lname, doi, title, journal, abstract, pub_date, citations))
    df = pd.DataFrame(
        rows,
        columns=[
            "First_name",
            "Last_name",
            "DOI",
            "Title",
            "Journal",
            "Abstract",
            "Pub Date",
            "Citations",
        ],
    ).drop_duplicates("DOI")

    return df

def parse_journal_works_to_df(works: List[dict]) -> pd.DataFrame:
    """Parse works to DataFrame

    Args:
        works (dict): Works responses from Crossref API
    """
    rows = []
    for work in works:
        # If article doesn't have a title or isn't an article, skip it
        if not work.get("title") or work['type'] != 'journal-article':
            continue

        doi = work["DOI"]
        title = work["title"][0]
        journal = work["container-title"][0]
        abstract = work.get("abstract", None)
        pub_date = work["published"]["date-parts"][0][0]
        citations = work["is-referenced-by-count"]
        rows.append((doi, title, journal, abstract, pub_date, citations))
    df = pd.DataFrame(
        rows,
        columns=[
            "DOI",
            "Title",
            "Journal",
            "Abstract",
            "Pub Date",
            "Citations",
        ],
    ).drop_duplicates("DOI")

    return df

def remove_xml_from_abstract(abstract_text:str) -> str | None:
    """Cleans the abstract text of XML tags
    Args:
        abstract_text (str): Abstract text with XML tags

    Returns:
        str: cleaned abstract or None if no abstract text
    """

    if not abstract_text:
        return None

    soup = BeautifulSoup(abstract_text, "lxml")
    for title in soup.find_all("jats:title"):
        title.clear()

    cleaned_text = ""
    for element in soup.find_all():
        if element.name == "jats:p":
            if cleaned_text:
                cleaned_text += " "  # Add a space before adding new paragraph
            cleaned_text += element.get_text()

    return cleaned_text.strip()
