#  Configuring the code to run *your* analyses

I have created this repository in such a way as to make it somewhat difficult to 'break' and easy to 'restore' if/when you do break something. I do this by creating a `settings.json` file that is used to configure the analyses that are run in this repository. You should not need to edit the code itself to run the analyses you want. Instead, you can edit the `settings.json` file to specify the data sources, the analyses to run, and the settings for the analyses.

## What is what in the settings.json file?
1. "CrossRef" > "User-Agent" - this is used to identify who you are and what you are doing when you access the CrossRef API. You should change this to your own email address (in fact, the code will not run if you leave it as "YourEmailHere").
2. "Custom Stopwords" - this is a list of words that you want to exclude from the analyses. You can add or remove words from this list as you see fit.
3. "Ollama Model" - This is the LLM model that is used to generate embeddings. This model must be in the 'models' list on [Ollama.com](https://ollama.com/library) and must have already been downloaded to your computer.
4. "Scholars" - This is the sampling frame for the first corpus used in the analyses (scholar-by-scholar publication data). Each scholar needs to have:
    - "first_name" - Their first name as it appears in the publication data
    - "last_name" - Their last name as it appears in the publication data
    - "start_year" - The year that you want to start collecting data for this scholar (their first publication year) - used to filter possible false positives
    - *Note: This isn't a precise way of getting scholar data - there could be multiple scholars with the same name, or the same scholar could have multiple names. This is just a way to get a rough idea of what the data looks like.*
5. "ISSNs" - This is the set of journals and ISSNs to use for the first corpus (scholar-by-scholar corpus) - if the author has publications outside of this list, they will not be included in the analysis. This is done because the likelihood of having two scholars with the same name increases a lot when you move outside of one research field. Each entry needs to have:
    - the name of the journal as the key
    - the list of that journal's ISSNs as the value (if there is only one ISSN, it is still entered as a list, but a list with only one item)
6. "Journal Pub Sample" - This is the sampling frame for the second corpus used in the analyses (journal-by-journal publication data). There should be two entries:
    - "journals" - a list of journal names that you want to include in the analysis. These journals **MUST** match verbatim one of the entries in the ISSNs list above (case-sensitive).
    - "start_year" - The year that you want to start collecting data for this corpus
7. "Non-content Regexes" - This is a list of regular expressions that are used to identify non-content text in the publication data. This is used to filter out things like copyright statements that appear in some journals abstracts. You can add or remove regular expressions from this list as you see fit. However, regular expressions can be tricky, so be careful. If you don't know what you're doing here, maybe leave it be.
    - Note: This set of regular expressions are the result of a huge trial-and-error process from a different project. They may not capture everything in this dataset (or your dataset) and there are very likely unneeded/redundant regular expressions in this list.
8. "Test Abstracts" - This is a list of fields and abstracts used for illustrative purposes to show how text embeddings of abstracts not in the dataset can be compared to the dataset. You can add or remove entries from this list as you see fit. Each list entry should have two elements:
    - Field - The field of the abstract (e.g., "Entrepreneurship", "Astrophysics", etc.)
    - Abstract - The text of the abstract
9. "Test Query" - This is a sample question you might ask of your dataset. For example, "What is the role of institutions in entrepreneurship". This is used to show how the embeddings don't necessarily have to be of an abstract to retrieve relevant texts from the dataset. You can change this to whatever you want.

## Uh oh... I broke something.

Oh geez... (just kidding). Easy peasy to fix things here so long as you didn't change the actual Python code. Just delete the `settings.json` file in your cloned directory, go back to the GitHub repository online, and download the `settings.json` file again. You can then edit the file as needed and run the analyses again.

### A couple of suggestions:
* Create a back-up of the `settings.json` file before you start making new edits to it. This way, if you make a mistake, you can just copy the back-up file back into the repository.
* If you're new to JSON files, you can use a JSON validator to check your edits before running the code. Such as [this one](https://jsonlint.com/).
    - You can even make your edits incrementally in this tool, checking after each modification to make sure you haven't broken anything.
* If you're new to regular expressions and you want to try your hand at editing it, you can use a regex tester to check your regular expressions before running the code. Such as [this one](https://regex101.com/).
* Try changing one thing at a time and making sure that the code still runs before moving on to the next change. This way, if something breaks, you know exactly what change caused the break.

[<-- Back to main page](../README.md)