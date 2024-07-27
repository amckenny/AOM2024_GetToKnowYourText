"""Preprocesses the abstracts"""

import spacy
from gensim.models.phrases import Phrases

import src.general as gen
import src.preprocessing as pp

AUTHOR_PHRASE_MODEL = gen.DATA_DIRECTORY / "author_phrases.model"
JOURNAL_PHRASE_MODEL = gen.DATA_DIRECTORY / "journal_phrases.model"


def main() -> None:
    """Main function for cleaning abstracts"""

    print("=====Loading data files into memory=====")
    author_data, journal_data = gen.load_data_files()

    print("=====Dropping Withdrawn/retracted/Errata/etc. articles=====")
    for word in [
        "withdrawn",
        "retracted",
        "errata",
        "correction",
        "retraction",
        "editorial",
        "issue information",
        "journal information",
    ]:
        author_data = author_data[
            ~author_data["Title"].str.lower().str.contains(word, case=False)
        ]
        journal_data = journal_data[
            ~journal_data["Title"].str.lower().str.contains(word, case=False)
        ]

    print("=====Dropping duplicate articles=====")
    # Drop duplicates based on DOI but only for journal corpus
    # Don't drop for author corpus or else we lose association for one of the
    # authors when 2+ authors worked on the same paper
    journal_data = journal_data.drop_duplicates(subset="DOI")

    print("=====Cleaning abstracts to remove non-content statements=====")
    author_data["Abstract_clean"] = pp.remove_noncontent_statements(
        author_data["Abstract"]
    ).astype(str)
    journal_data["Abstract_clean"] = pp.remove_noncontent_statements(
        journal_data["Abstract"]
    ).astype(str)

    print("=====Dropping articles with no abstracts=====")
    author_data = author_data[author_data["Abstract_clean"].notna()]
    journal_data = journal_data[journal_data["Abstract_clean"].notna()]
    author_data = author_data[author_data["Abstract_clean"].str.lower()!="none"]
    journal_data = journal_data[journal_data["Abstract_clean"].str.lower()!="none"]
    author_data = author_data[author_data["Abstract_clean"].str.strip() != ""]
    journal_data = journal_data[journal_data["Abstract_clean"].str.strip() != ""]

    print("=====Preparing preprocessing models=====")
    gen.check_download_models()

    print("=====Preprocessing corpora=====")
    nlp = spacy.load("en_core_web_sm")

    print(">> Author corpus...")
    author_data["Full_name"] = (
        author_data["First_name"] + " " + author_data["Last_name"]
    )
    author_abstracts_list = author_data["Abstract_clean"].tolist()
    author_docs = list(nlp.pipe(author_abstracts_list))
    author_data["Abstract_clean"] = [doc.text for doc in author_docs]
    author_preprocessed = pp.preprocess_docs(author_docs, True, True, True)
    author_data["Abstract_preprocessed"] = author_preprocessed
    author_phrases = Phrases(author_preprocessed, min_count=3, threshold=10)
    author_phrases.save(str(AUTHOR_PHRASE_MODEL))
    author_data["Abstract_w_bigrams"] = author_data["Abstract_preprocessed"].apply(
        lambda x: author_phrases[x]
    )
    author_data["Abstract_bigram_ws"] = author_data["Abstract_w_bigrams"].str.join(" ")

    print(">> Journal corpus...")
    journal_abstracts_list = journal_data["Abstract_clean"].tolist()
    journal_docs = list(nlp.pipe(journal_abstracts_list))
    journal_data["Abstract_clean"] = [doc.text for doc in journal_docs]
    journal_preprocessed = pp.preprocess_docs(journal_docs, True, True, True)
    journal_data["Abstract_preprocessed"] = journal_preprocessed
    journal_phrases = Phrases(journal_preprocessed, min_count=3, threshold=10)
    journal_phrases.save(str(JOURNAL_PHRASE_MODEL))
    journal_data["Abstract_w_bigrams"] = journal_data["Abstract_preprocessed"].apply(
        lambda x: journal_phrases[x]
    )
    journal_data["Abstract_bigram_ws"] = journal_data["Abstract_w_bigrams"].str.join(
        " "
    )

    print("=====Saving data files to disk=====")
    gen.save_data_files(author_data, journal_data)

    print("*****Processing complete*****")
    print(f"Data files saved to {gen.DATA_DIRECTORY}")


if __name__ == "__main__":
    main()
