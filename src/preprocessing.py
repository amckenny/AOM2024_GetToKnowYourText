"""Preprocessing module for text data"""

from typing import List

import nltk
import pandas as pd
import spacy

import src.general as gen


def get_stopwords() -> List[str]:
    """Get list of stopwords from NLTK and custom words from settings

    Returns:
        List[str]: List of stopwords
    """

    stops = nltk.corpus.stopwords.words("english")

    settings = gen.get_settings()
    assert "Custom Stopwords" in settings, "Custom Stopwords not in settings.json"

    return settings["Custom Stopwords"] + stops


def preprocess_docs(
    docs: List[spacy.tokens.Doc],
    remove_stops: bool,
    remove_nwcs: bool,
    lemmatize: bool,
) -> List[List[str]]:
    """Preprocesses docs"""

    stopwords = get_stopwords()

    preprocessed = []
    for doc in docs:
        preprocessed_doc = []
        for token in doc:
            if remove_nwcs and token.pos_ in ["PUNCT", "SYM", "NUM", "X", "PART"]:
                continue
            if lemmatize:
                if len(token.lemma_) <= 2:
                    continue
                if remove_stops and token.lemma_.lower() in stopwords:
                    continue
                preprocessed_doc.append(token.lemma_.lower().strip())
            else:
                if len(token.text) <= 2:
                    continue
                if remove_stops and token.text.lower() in stopwords:
                    continue
                preprocessed_doc.append(token.text.lower().strip())
        preprocessed.append(preprocessed_doc)

    return preprocessed


def get_noncontent_regexes() -> List[str]:
    """Get list of regexes for non-content statements in abstracts

    Returns:
        List[str]: List of regex strings from settings.json
    """

    settings = gen.get_settings()
    assert "Non-content Regexes" in settings, "Non-content Regexes not in settings.json"

    return settings["Non-content Regexes"]


def remove_noncontent_statements(texts: pd.Series) -> pd.Series:
    """Removes non-content statements from abstracts"""

    regexes = get_noncontent_regexes()

    for regex_str in regexes:
        texts = texts.replace(regex_str, "", regex=True)

    return texts
