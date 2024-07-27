# Running the code in this repository

If you followed the steps in the [detailed setup instructions](detailed_setup.md), you should have a virtual environment set up with all the necessary packages installed. If you haven't done that yet, I recommend you do so before proceeding.

To run the code in this repository, you will need to run the Python scripts in the base folder of the cloned repository with the virtual environment activated. Instructions for activating the virtual environment are the same as in the [detailed setup instructions](detailed_setup.md).

To python scripts (in Windows): From the terminal, all you need to do is type `python` followed by the script name and press Enter. For example, to run the first script, you would type `python 1_collect_data.py` and press enter.

The scripts are numbered in the order they should be run. Here is a brief overview of each script:

1. `1_collect_data.py`: This script collects the two corpora used in the analyses. It will create a `data/` folder in the repository and populate it with the necessary data for future steps. This script should be run first and only needs to be run once.

Important notes:
- Before running the script, you need to have edited the `settings.json` file to replace "YourEmailHere" with your actual email address in the "Crossref" -> "User-Agent". This is the only *required* change to the settings file. You can make other changes if you want to customize the analyses.
- Other [settings](configuration.md) used by this file are:
    - "Scholars": The scholars to collect data for in corpus 1. By default, this is a handful of editors of Entrepreneurship journals.
    - "ISSNs": The ISSNs of the journals to collect data for in corpus 1. By default, this is a smattering of Entrepreneurship and Entrepreneurship-adjacent journals.
    - "Journal Pub Sample": The journals and start year to collect data for in corpus 2. By default, this is JBV, ET&P, and SEJ from 2000-present.
- For some reason, abstract data is not uniformly provided by all journals. Notably, JBV does not provide abstracts in the Crossref API. This means that the abstracts for JBV will be missing in the corpus if you rely only on Crossref data. This is a limitation of the data source, not the script.
    - My code does have a workaround for this, but it requires a manual step. If you have a dataframe with titles and abstracts in it, the file will try to use that dataframe to 'fill-in-the-blanks' as it were. I did this using Scopus data; however, those data are proprietary and cannot be shared. If you have access to Scopus or some other source of abstracts, you can use this feature by placing a `scopus_download.parquet` file in the `data` folder and running the script. The only two columns needed in the file are 'title' and 'abstract'.
    - If you don't have access to Scopus or another source of abstracts, you can still run the script without the `scopus_download.parquet` file. The script will still work, but the abstracts for some journals (including JBV) will be missing.

2. `2_preprocess_abstracts.py`: This script cleans and preprocesses the data collected in the previous step. No new files are created, but there are new columns created in the dataset for the preprocessed texts.

Important notes:
-  This script does a lot of heavy-lifting from a text analysis perspective. Text analyses are computationally expensive and will take much longer to run on a computer without a GPU than one with a GPU. If you have a GPU, make sure that you followed the setup instructions to install the GPU version of spaCy. If you don't have a GPU, you can still run the script, but it will take longer.
-  Fortunately, like the above, this script only needs to be done once. The preprocessed data will be saved in the `data/` folder and can be used in future scripts without needing to re-run this script.
-  [Settings](configuration.md) used by this file are:
   -  "Non-content Regexes": A list of regular expressions to remove from the text. By default, this is a list of common non-content text that appears in academic abstracts such as copyright statements.
   -  "Custom Stopwords": A list of custom stopwords to remove from the text. By default, this is a list of common stopwords that are not included in the default NLTK stopwords list, but are frequently used in academic abstracts.


3. `3_scattertext.py`: This script creates the scattertext visualizations used in the presentation. The figures are saved in the `output/` folder as HTML files that can be viewed in any mainstream browser.
    - This script creates scattertexts for both corpora.

4. `4_embeddings.py`: This script finds the text embeddings for all abstracts in both corpora and creates a vector database in the `data/` folder. These embeddings are then compared to a list of sample abstracts and a sample query drawn from the `settings.json` file. The results of these comparisons are printed directly to the screen rather than saved in a file. The code then uses the t-SNE algorithm to project the embeddings into two dimensions and create a scatterplot for visualization. This scatterplot is saved in the `output/` folder as an HTML file that can be viewed in any mainstream browser.

Important Notes:
- Ollama must be running *as a server* to generate the embeddings. Here's how to do that:
    - If the llama icon is in the status bar, right click it and click "Quit Ollama".
    - Open a new terminal (not the one you will run the Python code in), type `ollama serve`, and press Enter.
    - Ollama should now be running as a server. Do not close this terminal window until you have finished running the Python code.
    - To run the Python code, in **ANOTHER** terminal window (not the one running the Ollama server), run the Python code as described at the top of this page.
- This script creates embeddings ONLY for the journal corpus (corpus 2)
- [Settings](configuration.md) used by this file are:
    - "Ollama Model": The name of the language model to use for embeddings. By default, this is "nomic-embed-text".
    - "Test Abstracts": A list of fields and a sample abstract from that field
    - "Test Query": A sample query about the corpus' field

[<-- Back to main page](../README.md)