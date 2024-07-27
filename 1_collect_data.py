"""Main data collection script for AOM 2024 Entrepreneurship Language PDW presentation"""

import time
from pathlib import Path
from typing import List, Tuple

import pandas as pd

import src.general as gen
import src.crossref as crossref

SCOPUS_DATA_FILE = gen.DATA_DIRECTORY / "scopus_download.parquet"


def write_data_file(file_path: Path) -> bool:
    """Verify file exists and prompt user to overwrite if it does"""
    if not file_path.exists():
        return True

    while True:
        print(f"Data file {file_path} already exists. Overwrite? (y/n) > ", end="")
        response = input().strip().lower()
        if response == "n":
            print("Skipping data collection")
            return False
        elif response == "y":
            print(f"Overwriting data file {file_path}")
            return True
        else:
            print("Invalid response.")


def get_scholars() -> List[dict]:
    """Get list of scholars from settings.json

    Returns:
        [dict]: List of scholars names and start years in dicts
    """

    settings = gen.get_settings()
    assert "Scholars" in settings, "Scholars not in settings.json"

    return settings["Scholars"]


def collect_author_data(api_delay: int) -> pd.DataFrame:
    """Collect author data from Crossref API and save to pickle file"""

    if not write_data_file(gen.AUTHOR_DATA_FILE):
        return pd.read_pickle(gen.AUTHOR_DATA_FILE)

    scholar_list = get_scholars()
    author_data_list = []

    for scholar in scholar_list:
        fname, lname = scholar["first_name"], scholar["last_name"]
        s_year = scholar["start_year"]
        works = crossref.get_works_by_name(fname, lname, s_year)
        author_data = crossref.parse_author_works_to_df(fname, lname, works)
        author_data_list.append(author_data)
        print(f"Collected {len(author_data)} publications for {fname} {lname}")
        if api_delay:
            print(f"Sleeping for {api_delay} seconds to avoid taxing API")
            time.sleep(api_delay)

    author_data = pd.concat(author_data_list, ignore_index=True)
    author_data["Abstract"] = author_data["Abstract"].apply(
        crossref.remove_xml_from_abstract
    )
    return author_data


def get_journal_sample_frame() -> Tuple[List[str], int]:
    """Get list of journals from settings.json

    Returns:
        List[str]: List of journal names
        int: Start year for sampling frame
    """

    settings = gen.get_settings()
    assert "Journal Pub Sample" in settings, "Journal Pub Sample not in settings.json"
    sample = settings["Journal Pub Sample"]

    assert "journals" in sample, "journals not in Journal Pub Sample"
    assert "start_year" in sample, "start_year not in Journal Pub Sample"
    journal_list = sample["journals"]
    start_year = sample["start_year"]

    assert isinstance(journal_list, list), "journals must be a list"
    assert isinstance(start_year, int), "start_year must be an integer"

    return (journal_list, start_year)


def collect_journal_data(api_delay: int) -> pd.DataFrame:
    """Collect journal data from Crossref API and save to pickle file"""

    if not write_data_file(gen.JOURNAL_DATA_FILE):
        return pd.read_pickle(gen.JOURNAL_DATA_FILE)

    journal_list, start_year = get_journal_sample_frame()

    issn_list = crossref.get_issn_list(journal_list)
    journal_data_list = []

    for issn in issn_list:
        works = crossref.get_works_by_issn(issn, start_year)
        journal_data = crossref.parse_journal_works_to_df(works)
        journal_data_list.append(journal_data)
        print(f"Collected {len(journal_data)} publications for journal {issn}")
        if api_delay:
            print(f"Sleeping for {api_delay} seconds to avoid taxing API")
            time.sleep(api_delay)

    journal_data = pd.concat(journal_data_list, ignore_index=True)
    journal_data["Abstract"] = journal_data["Abstract"].apply(
        crossref.remove_xml_from_abstract
    )
    return journal_data


def merge_w_scopus_data(df: pd.DataFrame, scopus_data: pd.DataFrame) -> pd.DataFrame:
    """Merge Crossref data with Scopus data to fill in missing abstracts

    Args:
        df (pd.DataFrame): Crossref data
        scopus_data (pd.DataFrame): Scopus data

    Returns:
        pd.DataFrame: Merged data
    """
    # Merge on DOI
    merged_df = df.merge(
        scopus_data[["title", "abstract"]],
        left_on="Title",
        right_on="title",
        how="left",
    )

    # Fill in missing abstracts
    df["Abstract"] = df["Abstract"].combine_first(merged_df["abstract"])

    return df


def main(api_delay: int = 2) -> None:
    """Main data collection function

    Args:
        api_delay (int, optional): Delay in seconds between API calls. Defaults to
            2.
    """

    # Collect samples from Crossref API
    print("=====Author Data Collection=====")
    author_data = collect_author_data(api_delay)

    print("=====Journal Data Collection=====")
    journal_data = collect_journal_data(api_delay)

    # Fill in missing abstract data where possible using Scopus data
    # Requires manual intervention from user beyond the scope of this repository
    if not SCOPUS_DATA_FILE.exists():
        print("==(Optional) Manual data needed==")
        print(
            "You will need to use Scopus to collect the missing abstracts to "
            "use the following code."
        )
        print("Only the 'title' and 'abstract' columns are needed.")
        print(f"Save the Scopus data as: {SCOPUS_DATA_FILE}.")
        print(
            "You do not need to do so to run the rest of the code "
            "but you will have missing abstracts for some journals and authors"
        )
    else:
        print("=====Merging abstracts from Scopus data=====")

    if SCOPUS_DATA_FILE.exists():
        scopus_data = pd.read_parquet(SCOPUS_DATA_FILE)

        print("=====Filling in Missing Abstracts in Author Data=====")
        author_data = merge_w_scopus_data(author_data, scopus_data)

        print("=====Filling in Missing Abstracts in Journal Data=====")
        journal_data = merge_w_scopus_data(journal_data, scopus_data)

    print("=====Saving data files to disk=====")
    gen.save_data_files(author_data, journal_data)

    print("*****Processing complete*****")
    print(f"Data files saved to {gen.DATA_DIRECTORY}")


if __name__ == "__main__":
    main()
