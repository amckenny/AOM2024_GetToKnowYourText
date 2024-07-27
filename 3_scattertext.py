"""Runs scattertext on the cleaned abstracts"""

import pandas as pd
import scattertext as st

import src.general as gen


def one_vs_rest_authors(author_data) -> None:
    """Run one-vs-rest Scattertext analysis for authors"""

    corpus = (
        st.CorpusFromPandas(
            author_data,
            category_col="Full_name",
            text_col="Abstract_bigram_ws",
            nlp=st.whitespace_nlp,
        )
        .build()
        .compact(st.AssociationCompactor(2000))
    )

    for author in author_data["Full_name"].unique():
        print(f">>>> {author}")
        html = st.produce_scattertext_explorer(
            corpus,
            category=author,
            category_name=author,
            not_category_name="Other Authors",
            minimum_term_frequency=2,
            pmi_filter_thresold=4,
            transform=st.Scalers.dense_rank,
            width_in_pixels=1000,
            metadata=author_data["Title"],
            include_gradient=True,
            left_gradient_term=f"Less like {author}",
            right_gradient_term=f"More like {author}",
        )

        output_file = gen.OUTPUT_DIRECTORY / f"{author}_scattertext.html"
        with open(output_file, "wb") as outfile:
            outfile.write(html.encode("utf-8"))


def one_vs_rest_journals(journal_data) -> None:
    """Run one-vs-rest Scattertext analysis for journals"""

    corpus = (
        st.CorpusFromPandas(
            journal_data,
            category_col="Journal",
            text_col="Abstract_bigram_ws",
            nlp=st.whitespace_nlp,
        )
        .build()
        .compact(st.AssociationCompactor(2000))
    )

    for journal in journal_data["Journal"].unique():
        print(f">>>> {journal}")
        html = st.produce_scattertext_explorer(
            corpus,
            category=journal,
            category_name=journal,
            not_category_name="Other Journals",
            minimum_term_frequency=20,
            pmi_filter_thresold=4,
            transform=st.Scalers.dense_rank,
            width_in_pixels=1000,
            include_gradient=True,
            left_gradient_term=f"Less like {journal}",
            right_gradient_term=f"More like {journal}",
        )

        output_file = gen.OUTPUT_DIRECTORY / f"{journal}_scattertext.html"
        with open(output_file, "wb") as outfile:
            outfile.write(html.encode("utf-8"))


def citation_extremes(journal_data) -> None:
    """Scattertext of words associated with the most and fewest citations"""

    # No citations yet for 2024 articles
    journal_data = journal_data[journal_data["Pub Date"] < 2024]

    def get_most_least_cited(group) -> pd.DataFrame:
        threshold = group["Citations"].quantile(0.80)
        group["Most_cited"] = group["Citations"].apply(
            lambda x: "high" if x >= threshold else "not"
        )
        threshold = group["Citations"].quantile(0.20)
        group["Least_cited"] = group["Citations"].apply(
            lambda x: "low" if x <= threshold else "not"
        )
        return group

    journal_data = (
        journal_data.groupby("Pub Date")
        .apply(get_most_least_cited)
        .reset_index(drop=True)
    )

    corpus = (
        st.CorpusFromPandas(
            journal_data,
            category_col="Most_cited",
            text_col="Abstract_bigram_ws",
            nlp=st.whitespace_nlp,
        )
        .build()
        .compact(st.AssociationCompactor(2000, use_non_text_features=False))
    )

    html = st.produce_scattertext_explorer(
        corpus,
        category="high",
        category_name="Most Cited",
        not_category_name="Not Most Cited",
        minimum_term_frequency=20,
        pmi_filter_thresold=4,
        transform=st.Scalers.dense_rank,
        width_in_pixels=1000,
        include_gradient=True,
        left_gradient_term="Less likely to be most cited",
        right_gradient_term="More likely to be most cited",
    )

    output_file = gen.OUTPUT_DIRECTORY / "Most_cited_scattertext.html"
    with open(output_file, "wb") as outfile:
        outfile.write(html.encode("utf-8"))

    corpus = (
        st.CorpusFromPandas(
            journal_data,
            category_col="Least_cited",
            text_col="Abstract_bigram_ws",
            nlp=st.whitespace_nlp,
        )
        .build()
        .compact(st.AssociationCompactor(2000, use_non_text_features=False))
    )

    html = st.produce_scattertext_explorer(
        corpus,
        category="low",
        category_name="Least Cited",
        not_category_name="Not Least Cited",
        minimum_term_frequency=20,
        pmi_filter_thresold=4,
        width_in_pixels=1000,
        include_gradient=True,
        left_gradient_term="Less likely to be least cited",
        right_gradient_term="More likely to be most cited",
    )

    output_file = gen.OUTPUT_DIRECTORY / "Least_cited_scattertext.html"
    with open(output_file, "wb") as outfile:
        outfile.write(html.encode("utf-8"))


def main() -> None:
    """Main function for scattertext analysis"""

    print("=====Loading data files into memory=====")
    author_data, journal_data = gen.load_data_files()

    print("=====Running scattertext analyses=====")
    print(">> Authors...")
    one_vs_rest_authors(author_data)
    print(">> Journals...")
    one_vs_rest_journals(journal_data)
    print(">> Citation extremes...")
    citation_extremes(journal_data)

    print("*****Processing complete*****")
    print(f"Scattertexts saved to {gen.OUTPUT_DIRECTORY}")


if __name__ == "__main__":
    main()
