"""General use functions"""

import json
from pathlib import Path
from typing import Tuple

import nltk
import pandas as pd
import spacy

DATA_DIRECTORY = Path(__file__).parents[1] / "data"
DATA_DIRECTORY.mkdir(exist_ok=True)
OUTPUT_DIRECTORY = Path(__file__).parents[1] / "output"
OUTPUT_DIRECTORY.mkdir(exist_ok=True)

AUTHOR_DATA_FILE = DATA_DIRECTORY / "author_publications.pkl"
JOURNAL_DATA_FILE = DATA_DIRECTORY / "journal_publications.pkl"


def get_settings() -> dict:
    """Get settings from settings.json"""

    settings_file = Path(__file__).parents[1] / "settings.json"
    assert settings_file.exists(), f"Settings file not found at {settings_file}"

    with open(settings_file, encoding="utf8") as infile:
        json_data = infile.read()

    assert json_data, "No data in settings.json"

    return json.loads(json_data)


def check_download_models() -> None:
    """Download spaCy model if it doesn't exist"""

    print("Downloading NLTK and SpaCy resources...")
    nltk.download("stopwords")

    if "en_core_web_sm" not in spacy.util.get_installed_models():
        spacy.cli.download("en_core_web_sm", False, False, "--quiet")


def load_data_files() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Check that data files exist and load them into memory

    Returns:
        pd.DataFrame: Author data
        pd.DataFrame: Journal data
    """

    assert (
        AUTHOR_DATA_FILE.exists()
    ), f"Author data file not found at {AUTHOR_DATA_FILE}"
    assert (
        JOURNAL_DATA_FILE.exists()
    ), f"Journal data file not found at {JOURNAL_DATA_FILE}"

    author_data = pd.read_pickle(AUTHOR_DATA_FILE)
    journal_data = pd.read_pickle(JOURNAL_DATA_FILE)

    return author_data, journal_data


def save_data_files(author_data: pd.DataFrame, journal_data: pd.DataFrame) -> None:
    """Save data files to disk

    Args:
        author_data (pd.DataFrame): Author data
        journal_data (pd.DataFrame): Journal data
    """

    author_data.to_pickle(AUTHOR_DATA_FILE)
    journal_data.to_pickle(JOURNAL_DATA_FILE)
