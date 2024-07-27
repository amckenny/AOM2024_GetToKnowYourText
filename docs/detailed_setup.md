# Detailed setup instructions
Not a coder? No problem! This document provides detailed instructions on how to set up your computer to run the code associated with my presentation.

**Please note that these instructions are written for Windows users.** If you are using a Mac or Linux, you may need to adjust the instructions slightly. If you run into trouble, please try your university's IT support and Google before reaching out to me. I'm happy to help, but when this is being shared with the world, it would become overwhelming to provide detailed support to everyone. (Also, I'm of no use whatsoever for Mac users - sorry, I've only ever worked with Windows and Linux!)

I provide video links to help with several of the steps if my written descriptions are insufficient. These videos are not mine, but they are publicly available on YouTube. I hope they help you get started!

## Step 1: Install Python

I use Python for my analyses, so you'll need to have Python installed on your computer to run the code. I used [Python 3.11](https://www.python.org/downloads/release/python-3119/) for this presentation, but I suspect any relatively recent version will work fine.

[Here is a video](https://www.youtube.com/watch?v=YYXdXT2l-Gg&pp=ygUcY29yZXkgc2NoYWZlciBweXRob24gaW5zdGFsbA%3D%3D) on how to install Python on Windows or Mac.

Note: *Take note of the directory/file folder where Python is installed on your computer. You'll need this later.* For my example, this will be `C:\Users\amckenny\AppData\Local\Programs\Python\Python311`

## Step 2: Clone this GitHub repository to your computer (and if you find it helpful, maybe give it a star on GitHub?)

Cloning a GitHub repository basically means that you want to take the code you see here on the Internet and make a clone (copy) of it on your computer. There's more to it than that, but for our purposes, we'll leave it at that.

The way you do this will depend on your personal preferences:

* If you like dragging-and-dropping things rather than using a terminal/command-line interface, you may prefer to use the [GitHub Desktop application](https://desktop.github.com/).
    - Here is a video on how to clone a repository using GitHub Desktop: [Watch the video](https://www.youtube.com/watch?v=PoZNIbs_wx8)

* If you're comfortable with the terminal/command line interface, you can use the lighter-weight [git SCM](https://git-scm.com/downloads) instead.
    - Here is a video on how to clone a repository using git SCM: [Watch the video](https://www.youtube.com/watch?v=EhxPBMQFCaI)

Note: *Whichever path you take, note the directory/file folder where you cloned the repository on your computer. You'll need this later.* For my example, this will be `C:\Users\amckenny\Desktop\AOM2024_GetToKnowYourText`

## Step 3: Create a virtual environment in a "venv" subdirectory

Now we have Python installed and the code on our computer. The next step is to create a virtual environment. A virtual environment is a self-contained directory that contains a Python installation custom-tailored for a particular project. This way, you can have different projects with different Python versions and packages without them interfering with each other.

1. Open a terminal/command line interface (Run `cmd` from the Start menu)
2. Navigate to the directory where you cloned this repository.
   - For example, I would type `cd 'C:\Users\amckenny\Desktop\AOM2024_GetToKnowYourText'` ('cd' stands for change directory) and press Enter
3. Recall the path to Python on your computer
   - Remember the directory where Python is installed from Step 1? Add `\python.exe` to the end of that directory to get the full path to Python.
   - In my case, that will be `C:\Users\amckenny\AppData\Local\Programs\Python\Python311\python.exe` (but don't do anything with that yet)
4. While still in the cloned repository directory (you didn't change directories when looking for Python, right?), create a virtual environment by typing the following command in the terminal and pressing Enter:
   - `'{path to Python}' -m venv venv`
   - So for me, that would be `'C:\Users\amckenny\AppData\Local\Programs\Python\Python311\python.exe' -m venv venv`

Mac/Linux users: [Here is a video](https://www.youtube.com/watch?v=Kg1Yvry_Ydk&pp=ygUTY3JlYXRlIGEgdmVudiBsaW51eA%3D%3D) of how to create+activate a virtual environment. It's not catered to my materials, but it captures the same process generally.

## Step 4: Activate the virtual environment and install the required packages

Now that we have a virtual environment, we need to activate it and install the packages required to run the code.

1. Make sure you're still in the cloned repository directory in the terminal.
    - For me, that would be `C:\Users\amckenny\Desktop\AOM2024_GetToKnowYourText`
    - If you're not there, revisit Steps 3.1-3.2 to navigate to the correct directory.
2. Activate the virtual environment by running the following command in the terminal and pressing Enter:
   - `.\venv\Scripts\activate`
   - The period '.' at the beginning is important. It tells the terminal to look in the current directory for the 'venv' subdirectory.
   - The terminal prompt should change to indicate that you are now in the virtual environment. For me, it looks like `(venv) C:\Users\amckenny\Desktop\AOM2024_GetToKnowYourText>`
3. Install the required packages by running the following commands in the terminal:
    - `python.exe -m pip install --upgrade pip setuptools wheel` (press Enter)
        - This command tells Python to update the package manager (pip) and the package installer (setuptools) to the latest versions.
    - `pip install -r requirements.txt` (press Enter)
        - This command tells Python to install the packages listed in the `requirements.txt` file in the repository.
        - It is a good practice to take a look at the `requirements.txt` file to make sure you know and trust what you're installing. You can open it in a text editor like Notepad or Word. Just be careful when changing anything, these files are sensitive to formatting changes.

## (Optional) Step 5: Install GPU-enabled spaCy

By default, the packages in the `requirements.txt` file are set up to work with a CPU. If you have a Nvidia CUDA-enabled GPU and would like to use it to speed up the computations, you can install the GPU-enabled version of spaCy.

1. Make sure the virtual environment is still activated.
    - If you see `(venv)` at the beginning of your terminal prompt, you're good to go.
    - If not, revisit Steps 4.1-4.2 to activate the virtual environment.
2. Verify that you have a compatible GPU and the necessary drivers installed.
    - Type `nvidia-smi` in the terminal and press Enter. If you see information about your GPU, you're good to go. If you get an error, you may need to install the necessary drivers or may not have a compatible GPU installed.
    - Take note of the CUDA version listed in the output. You'll need this for the next step.
3. Install the GPU-enabled spaCy package by visiting the [spaCy](https://spacy.io/usage) website and selecting the appropriate options for your system.
    - Your options:
        - Operating System: Choose your OS (Windows, Linux, MacOS)
        - Platform: Choose your processor type (for many of us, this will be "x86", but check with your IT folks if you're not sure)
        - Package Manager: Choose "pip"
        - Hardware: Choose "GPU" and from the dropdown, choose the highest CUDA version that is less than or equal to the CUDA version you noted in Step 5.2
        - Configuration - for the code I provide, you do not need to check either text box
        - Trained pipelines: "English"
        - Select pipeline for: "efficiency"
    - You should see two resulting commands like these... run them in the terminal:
        - `pip install -U 'spacy[cuda12x]'` (Press Enter)
            - If your computer is like mine, it may not like the apostrophes around the package name. If that is the case, you can remove them and run the command without them.
            - So, I would run `pip install -U spacy[cuda12x]`
        - `python -m spacy download en_core_web_sm`

## Step 5: Install `ollama` and download the `nomic-embed-text` embedding model

`Ollama` is an open-source tool for running large language models on your local computer. This is nice for several reasons:
1. Data security - locally hosting the model means the text stays on your computer rather than being sent to a third-party, which is good for IRB purposes and for sensitive texts.
2. Cost - It's open-source... no per-token API fee like with OpenAI/Google's models.
3. Controllable - Unless you overwrite the model or change the model, the model won't change on you. If you rely on a third-party API, they *could* (hopefully they wouldn't) change the model on you, potentially leading to unexpected results when comparing old analyses to new analyses.

OK, sales pitch over. Let's get it installed.

1. Visit [the ollama website](https://ollama.com/download). Download and install the appropriate version for your system.
2. Once installed, in the terminal, download the `nomic-embed-text` embedding model by running the following command:
    - `ollama pull nomic-embed-text` (press Enter)
    - This will download the model to your computer. It's a big file, so it may take a little while depending on your internet connection.
4. Verify that the model was downloaded successfully by running the following command:
    - `ollama list` (press Enter)
    - You should see `nomic-embed-text` in the list of available models.

## Step 6: Modify the `settings.json` file (carefully!)

This file makes it so you don't have to edit the Python code to tweak the analyses to your liking. However, be very careful not to change the formatting of the file. JSON files are very sensitive to formatting changes, and even a misplaced comma can cause the file to be unreadable. *Maybe create a backup of the file before editing it?*

**There is one change that *must* be made:** Replace "YourEmailHere" with your email address in the Crossref -> User-Agent field. This is used to identify you to the CrossRef API when you collect the article abstracts.

Details about the settings file are provided in the [configuration.md](configuration.md).

Here is a [video about json files](https://www.youtube.com/watch?v=GpOO5iKzOmY&t=8s&pp=ygUNanNvbiB0dXRvcmlhbA%3D%3D) that may help you understand the structure of the file.

## Setup Complete!

[<-- Back to main page](../README.md)
