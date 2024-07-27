# AOM 2024: Get To Know Your [Text]

[![Powerpoint Presentation Slides](https://img.shields.io/badge/Powerpoint%20Slides-Download-blue)](./docs/AOM2024_GetToKnowYourText.pptx)

This repository shares the materials associated with my presentation "Get To Know Your [Text]" at the 2024 Academy of Management Conference. The presentation is part of the Professional Development Workshop (PDW) titled *Framing Novelty: New perspectives on language and communication in entrepreneurship and innovation research*.

While I provide high-level descriptions of how to get started with the materials, I cannot provide detailed support/instruction on how to use Python or implement these tools. For detailed support, I provide a list of [resources](#resources) that can help you get started with Python and the tools I introduce at the bottom of this document. At the same time, I am happy to answer questions within the scope of my presentation.

## High-Level Initial Setup Instructions

These instructions assume a bit of tech-savviness. If that's not you, or you get lost in one step or another, there are step-by-step details on the [detailed setup instructions](./docs/detailed_setup.md) page.

1. **Install Python**. I used Python 3.11, but any relatively recent version should work.
2. **Clone this GitHub repository to your computer**
3. **Suggested** Create and activate a virtual environment for this repository
4. **Install the required Python packages** from the `requirements.txt` file
    - If you want CUDA acceleration, you can upgrade the spaCy package following details on the [spaCy website](https://spacy.io/usage).
5. **Install `ollama` and download the `nomic-embed-text` embedding model**
6. **Modify the `settings.json` file** to customize the analyses to your needs. Details about the settings file are provided in the [configuration instructions](./docs/configuration.md).
    - At a minimum, you will need to replace "YourEmailHere" with your email address in the Crossref -> User-Agent field.

***Setup Complete!***

## High-Level Instructions for Running the Analyses

These instructions assume a bit of tech-savviness. If that's not you, or you get lost in one step or another, there are step-by-step details on the [running the code](./docs/detailed_run_code.md) page.

1. **Run `1_collect_data.py`** to collect the data from Crossref.
    - If you have not replaced the "YourEmailHere" in the settings file, you will need to do so before running this script.
    - Crossref is missing some abstracts (notably from JBV). If you have access to Scopus or some other source of abstracts and titles, you can create a `scopus_download.parquet` file in the `data/` folder with the missing abstracts (only 'title' and 'abstract' fields are needed). If present, the script will automatically use this file to fill in the blanks. If not present, the script will leave the abstracts blank and the next Python script will eliminate them as 'missing data'.
        - Unfortunately, I cannot provide you with my datafile from Scopus.
        - The code will work fine without filling in missing abstracts, but you will not have abstracts for some articles/journals (e.g., JBVs).
2. **Run `2_preprocess_abstracts.py`** to preprocess the abstracts.
3. **Run `3_scattertext.py`** to create the Scattertext visualizations.
    - The output will be saved in the `output/` folder.
4. **Run `4_embeddings.py`** to create the embeddings and t-SNE visualizations.
    - You will need to have the Ollama server running in a separate terminal window for this script to work.
    - The embedding similarity results will be displayed in the terminal.
    - The scatterplot output will be saved in the `output/` folder


## Repository Structure

- `data/`: Contains the data used in the analyses - this folder will be created by the code provided and does not need to be created manually. You generally do not need to modify the contents of this folder. One exception is for data collection, that is described in the [details on running the 1_collect_data.py code](./docs/detailed_run_code.md).
- `docs/`: Contains documentation for the repository. If you need detailed instructions on something, check here.
- `output/`: Contains the output of the analyses - this folder will be created by the code provided and does not need to be created manually.
- `src/`: Contains the 'behind-the-scenes' Python code used in the analyses. You generally do not need to modify the contents of this folder. However, you may benefit by looking at it if you want to see under the hood.
- `venv/`: Contains the virtual environment for this repository. You probably created this during the setup process, if you followed the [detailed setup instructions](./docs/detailed_setup.md).
- `settings.json`: Contains the settings for the analyses. Leave this as-is to run the analyses like I did for the presentation. Or, edit it to customize the analyses to your needs. Details about the settings file are provided in the [configuration instructions](./docs/configuration.md).
- `1_collect_data.py`, `2_preprocess_abstracts.py`, `3_scattertext.py`, `4_embeddings.py`: These Python scripts run the analyses. You can run them in order to replicate the analyses I presented. Details about running the code are provided in the [details on running the code](./docs/detailed_run_code.md).
    - 1 and 2 need to be run first and sequentially. 3 and 4 can be run in any order after 1 and 2 have been run.
- `__init__.py`, `.gitignore`, `LICENSE`, `README.md`, `requirements.txt`: These files are used to manage the repository and provide information about the repository.

## Resources

- Learn More About
    - **Git/GitHub**
        - Free ebook: [Pro Git](https://git-scm.com/book/en/v2)
        - Good Youtube video: [freeCodeCamp.org](https://www.youtube.com/watch?v=RGOj5yH7evk&pp=ygUDZ2l0)
    - **Python**
        - Free ebook: [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)
        - Good Youtube channel for Python content: [Corey Schafer](https://www.youtube.com/@coreyms)
    - **Scattertext**
        - [Scattertext documentation](https://github.com/JasonKessler/scattertext)
        - [Youtube Video](https://www.youtube.com/watch?v=H7X9CA2pWKo)
    - **Word Embeddings**
        - [Ollama documentation](https://www.ollama.com/)
        - [Langchain documentation](https://www.langchain.com/)
        - [IBM's description](https://www.ibm.com/topics/word-embeddings)
        - [Youtube video of basic ideas](https://www.youtube.com/watch?v=BGWQf0nY4uo)
        - [Brief tutorial on integrating Langchain and Ollama](https://www.youtube.com/watch?v=CPgp8MhmGVY)
- **Packages I use**
        - XML parsing: [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) with [lxml](https://lxml.de/)
        - Vector database: [Chroma](https://www.trychroma.com/)
        - Phrase extraction: [gensim](https://radimrehurek.com/gensim/)
        - Embedding/LLM integration framework: [langchain](https://www.langchain.com/)
        - Stop word corpus: [nltk](https://www.nltk.org/)
        - LLM integration package: [ollama](https://www.ollama.com/)
        - Data management: [pandas](https://pandas.pydata.org/)
        - Scatterplot visualizations: [plotly](https://plotly.com/python/)
        - API requests: [requests](https://docs.python-requests.org/en/master/)
        - Scattertext visualizations: [scattertext](https://github.com/JasonKessler/scattertext)
        - t-SNE implementation: [scikit-learn](https://scikit-learn.org/stable/)
        - NLP pipeline: [spaCy](https://spacy.io/)
- Data Sources/Models
    - **Article Abstracts**
        - Main: [Crossref](https://www.crossref.org/)
        - Fill-in-the-blanks: [Scopus](https://www.scopus.com/)
            - Note: Scopus requires a subscription or access through an institution. I cannot provide access to Scopus or the data I used.
    - **Embedding Model**
        - [nomic-embed-text](https://ollama.com/library/nomic-embed-text)

# A Final Note

I structured the repository this way to make it easy for you to tweak/run the analyses you want without having to dig into the code. However, I can't guarantee that the code will work perfectly for all tweaks because it's difficult to predict what people will want to tweak (and time-consuming to try to do so). It also may not be the most efficient way to do what you want to do - you may (will likely, is more like it) want to structure things differently on your research projects. So, please feel free to make whatever changes you want to the code/settings itself to make it work better for you.

## On Stars and Citations

If you do like/use this repository, **please consider giving it a "star" in GitHub** so that I know that people are using it.

If you use my code directly in your research, please cite my presentation at the Academy of Management Conference. If you just use this for inspiration, no citation is needed - just enjoy (a star on the repository is still appreciated though 😉)!

McKenny, A. F. (2024, August 10). *Get to know your [text]* [Conference Presentation]. Academy of Management Annual Meeting, Chicago, IL, United States.
