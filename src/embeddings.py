"""Embedding functions"""

import shutil
from time import sleep
from typing import List, Tuple

import httpx
import numpy as np
import ollama
import pandas as pd
import plotly.express as px
import sklearn
import tqdm

from sklearn.manifold import TSNE
from langchain_chroma import Chroma
from langchain_community.document_loaders import DataFrameLoader
from langchain_ollama import OllamaEmbeddings

import src.general as gen

VECTORDB_DIRECTORY = gen.DATA_DIRECTORY / "vectordb"
SCATTERPLOT_FILE = gen.OUTPUT_DIRECTORY / "tsne_scatterplot.html"


def create_vectordb_directory() -> None:
    """Create the vector database directory"""

    VECTORDB_DIRECTORY.mkdir(exist_ok=True)


def delete_vectordb_directory() -> None:
    """Reset the vector database directory"""

    if VECTORDB_DIRECTORY.exists() and VECTORDB_DIRECTORY.is_dir():
        shutil.rmtree(VECTORDB_DIRECTORY)


def get_ollama_model() -> str:
    """Get the Ollama model from settings.json

    Returns:
        str: Ollama model from settings.json
    """

    settings = gen.get_settings()
    assert "Ollama Model" in settings, "Ollama Model not in settings.json"

    return settings["Ollama Model"]


def get_test_abstracts() -> List[Tuple[str, str]]:
    """Get the test abstracts from settings.json

    Returns:
        str: Field
        str: Abstract
    """

    settings = gen.get_settings()
    assert "Test Abstracts" in settings, "Test Abstracts not in settings.json"

    abstracts = [(field, abstract) for field, abstract in settings["Test Abstracts"]]

    return abstracts


def get_test_query() -> str:
    """Get the test query from settings.json

    Returns:
        str: Test query
    """

    settings = gen.get_settings()
    assert "Test Query" in settings, "Test Query not in settings.json"

    return settings["Test Query"]


def ollama_is_ready(model: str) -> bool:
    """Check to see if the Ollama server is ready

    Args:
        model (str): Ollama model

    Returns:
        bool: True if the Ollama server is ready, False otherwise
    """

    try:
        ollama.embeddings(model=model, prompt="Testing 123")
        return True, None, None
    except httpx.ConnectError as e:
        print(f"Ollama server does not appear to be running: {e}")
        return False
    except ollama._types.ResponseError as e:
        print(
            f"Ollama server is running, but the model is not responding as expected: {e}"
        )
        return False


def get_embedding(model: str, text: str) -> List[float]:
    """Get the embedding for a given text

    Args:
        model (str): Ollama model
        text (str): Text to embed

    Returns:
        List[float]: Embedding for the text
    """

    result = ollama.embeddings(model=model, prompt=text)
    return result["embedding"]


def get_cosine_similarity(embedding1: list, embedding2: list) -> float:
    """Get the cosine similarity between two embeddings

    Args:
        embedding1 (list): First embedding
        embedding2 (list): Second embedding

    Returns:
        float: Cosine similarity between the two embeddings
    """

    return sklearn.metrics.pairwise.cosine_similarity([embedding1], [embedding2])[0][0]


def create_vectordb(journal_data: pd.DataFrame, model: str) -> Chroma:
    """Create or load the vector database

    This is FAR from the best way to load the data. However, for computers with
    limited GPU memory (and I don't know what kind of computer this will
    be run on), this at least allows a good chance the data will be loaded
    albeit in chunks and potentially slowly.

    Args:
        journal_data (pd.DataFrame): Journal data
        model (str): Ollama model

    Returns:
        Chroma: Chroma vector database object
    """

    n_partitions = journal_data.shape[0] // 10
    if n_partitions == 0:
        n_partitions = 1

    partitions = np.array_split(journal_data, n_partitions)

    embeddings = OllamaEmbeddings(model=model)
    journal_db = Chroma(
        embedding_function=embeddings,
        collection_name="journal_embeddings",
        persist_directory=str(VECTORDB_DIRECTORY),
    )

    for partition in tqdm.tqdm(partitions, desc="Adding documents to database"):
        journal_data_loader = DataFrameLoader(
            partition, page_content_column="Abstract_clean"
        )
        journal_dataloader = journal_data_loader.load()
        attempts = 0
        while attempts < 5:
            try:
                journal_db.add_documents(journal_dataloader)
                break
            except ollama._types.ResponseError as e:
                attempts += 1
                if attempts > 5:
                    raise e
                print(f"\nError adding documents to database: {e}")
                print("This often happens when the Ollama server is busy.")
                print(f"Waiting 20 seconds before retrying...{attempts} of 5")
                sleep(20)

    return journal_db


def load_vectordb(model: str) -> Chroma:
    """Load the vector database

    Args:
        model (str): Ollama model

    Returns:
        Chroma: Chroma vector database object
    """
    embeddings = OllamaEmbeddings(model=model)
    journal_db = Chroma(
        collection_name="journal_embeddings",
        embedding_function=embeddings,
        persist_directory=str(VECTORDB_DIRECTORY),
    )
    return journal_db


def generate_journal_summary_embeddings(db: Chroma) -> pd.DataFrame:
    """Generate journal summary embeddings

    Args:
        db (Chroma): Chroma vector database object

    Returns:
        pd.DataFrame: Journal summary embeddings
    """

    results = db._collection.get(include=["embeddings", "metadatas"])
    df = pd.DataFrame(
        zip([data["Journal"] for data in results["metadatas"]], results["embeddings"]),
        columns=["Journal", "Embedding"],
    )
    df["Embedding"] = df["Embedding"].apply(np.array)
    journal_summary_embeddings = (
        df.groupby("Journal")["Embedding"]
        .apply(lambda e: np.mean(np.stack(e), axis=0))
        .reset_index()
        .set_index("Journal")
    )
    return journal_summary_embeddings


def reduce_dimensions_tsne(db: Chroma) -> pd.DataFrame:
    """Reduce dimensions using t-SNE

    Args:
        db (Chroma): Chroma vector database object

    Returns:
        pd.DataFrame: Journal data with t-SNE embeddings
        TSNE: fitted t-SNE model
    """
    results = db._collection.get(include=["embeddings", "metadatas"])
    df = pd.DataFrame(
        zip(
            [data["Journal"] for data in results["metadatas"]],
            [data["Title"] for data in results["metadatas"]],
            results["embeddings"],
        ),
        columns=["Journal", "Title", "Embedding"],
    )

    individual_embeddings = np.array(df["Embedding"].to_list())
    tsne_model = TSNE(
        n_components=2, random_state=24601, perplexity=30, learning_rate="auto"
    )
    tsne_results = tsne_model.fit_transform(individual_embeddings)
    df["TSNE1"], df["TSNE2"] = tsne_results[:, 0], tsne_results[:, 1]

    return df


def create_tsne_scatterplot(df: pd.DataFrame) -> None:
    """Create a t-SNE scatterplot

    Args:
        df (pd.DataFrame): Journal data with t-SNE embeddings
    """
    fig = px.scatter(
        df,
        x="TSNE1",
        y="TSNE2",
        color="Journal",
        hover_data=["Journal", "Title"],
        title="t-SNE Scatterplot of Journal Embeddings",
    )
    fig.update_layout(
        template="plotly_dark",
        legend={
            "font": {"size": 24},
            "itemsizing": "constant",
        },
        hoverlabel={"font": {"color": "white"}},
        title={"font": {"size": 20}},
        xaxis={"title": {"font": {"size": 16}}},
        yaxis={"title": {"font": {"size": 16}}},
    )
    fig.write_html(SCATTERPLOT_FILE)
