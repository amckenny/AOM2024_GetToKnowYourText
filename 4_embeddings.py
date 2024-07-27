import sys

import ollama

import src.general as gen
import src.embeddings as emb


def main() -> None:
    """Main function for embedding functions"""

    print("=====Initializing vector database directory=====")
    if emb.VECTORDB_DIRECTORY.exists():
        while True:
            response = input(
                "Vector database already exists. [R]eset or [U]se as-is? (r/u): "
            )
            if response.lower() in ["r", "u"]:
                break
            print("Invalid response. Please enter 'r' or 'u'\n")

        if response.lower() == "r":
            emb.delete_vectordb_directory()
    else:
        response = "r"
    emb.create_vectordb_directory()

    print("=====Getting Ollama model=====")
    model = emb.get_ollama_model()
    if not emb.ollama_is_ready(model):
        sys.exit()

    print("=====Loading datafiles=====")
    _, journal_data = gen.load_data_files()

    print("=====Dropping unneeded columns=====")
    journal_data = journal_data.drop(
        columns=[
            "Abstract",
            "Abstract_preprocessed",
            "Abstract_w_bigrams",
            "Abstract_bigram_ws",
        ]
    )

    if response.lower() == "r":
        print("=====Creating vector database=====")
        db = emb.create_vectordb(journal_data, model)
    else:
        print("=====Loading vector database=====")
        db = emb.load_vectordb(model)

    print("=====Generating journal summary embeddings=====")
    journal_summary_embeddings = emb.generate_journal_summary_embeddings(db)

    test_abstracts = emb.get_test_abstracts()
    test_query = emb.get_test_query()

    print("****************Test Abstracts*****************")
    for field, test_abstract in test_abstracts:
        print(f"\n\n--------------{field}--------------")
        print(test_abstract[:500], end="")
        if len(test_abstract) > 500:
            print("...")
        else:
            print()
        print("----------------Embedding Vector---------------")
        test_embedding = ollama.embeddings(model=model, prompt=test_abstract)[
            "embedding"
        ]
        rounded_embedding = [round(x, 2) for x in test_embedding]
        print(rounded_embedding[:50], "...")
        print("---------------Cosine Similarity---------------")
        for i, (journal, embedding) in enumerate(journal_summary_embeddings.iterrows()):
            similarity = emb.get_cosine_similarity(
                test_embedding, embedding["Embedding"]
            )
            print(f"{i+1}. {journal} - {similarity:.4f}")
        print("-------------Most similar articles-------------")
        most_similar = db.similarity_search_by_vector(test_embedding, k=5)
        for i, doc in enumerate(most_similar):
            doc_embedding = ollama.embeddings(model=model, prompt=doc.page_content)[
                "embedding"
            ]
            similarity = emb.get_cosine_similarity(test_embedding, doc_embedding)
            print(f"{i+1}. {doc.metadata['Title']} - {similarity:.4f}")
    print("\n*******************Test Query******************")
    print(test_query)
    print("----------------Embedding Vector---------------")
    test_query_embedding = ollama.embeddings(model=model, prompt=test_query)[
        "embedding"
    ]
    rounded_query_embedding = [round(x, 2) for x in test_query_embedding]
    print(rounded_query_embedding[:50], "...")
    print("-------------Top Articles by Query-------------")
    top_articles = db.similarity_search_by_vector(test_query_embedding, k=5)
    for i, doc in enumerate(top_articles):
        doc_embedding = ollama.embeddings(model=model, prompt=doc.page_content)[
            "embedding"
        ]
        similarity = emb.get_cosine_similarity(test_query_embedding, doc_embedding)
        print(f"{i+1}. {doc.metadata['Title']} - {similarity:.4f}")
    print("\n***********************************************")
    print("*           Visualizing Embeddings            *")
    print("***********************************************")
    print("=====Reducing dimensions with t-SNE=====")
    tsne_df = emb.reduce_dimensions_tsne(db)
    print("=====Creating t-SNE scatterplot=====")
    emb.create_tsne_scatterplot(tsne_df)

    print("*****Processing complete*****")
    print(f"t-SNE Scatterplot saved to {gen.OUTPUT_DIRECTORY}")


if __name__ == "__main__":
    main()
