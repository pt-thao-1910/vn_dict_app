# Vietnamese intelligent dictionary application
This is a Vietnamese dictionary which provides list of ordered meaning based on the context sentence. <br>
We aim to enhance your experience when using online dictionaries by reducing the time needed to be spent on finding out the right meaning among a long list of meanings and explanations. <br>
The application is deployed here:<br>
https://vndictapp-ek4r3xdf5irkysabnqhewt.streamlit.app/

## Project Motivation:
One of the most common problem for current online dictionaries we observe nowadays is the lack of consideration for context. When searching for a keyword, the dictionary simply returns a list of meanings regardless of what context the keyword is in. Therefore, when browsing for the correct meaning of a word, dictionary users often have to read through the whole explanation for the keyword, which can be very time consuming and inconvenient, especially when the keyword has multiple meanings and word types. To solve the problem, we hope to build an intelligent dictionary that can present meanings based on the the context sentence using some simple natural language processing methods.

## How the application works:
The general idea is to find out the correct meaning by calculating a similarity score between each meaning and corresponding example sentences provided by the dictionary with the context sentence (provided by user) through: <br>
1/ Co-occurrence score: similarity between meaning – context sentence <br>
2/ Word vector score: similarity between example sentences – context sentence <br>
We also use POS tagger to make sure the meaning have the correct word type (noun, verbs, etc.) based on the context sentence.

## Libraries:
In this project, we mainly utilized library "underthesea" to apply various NLP techniques and calculate the scores for list of meanings. <br>
As data scraping is required, we also applied "requests" and "bs4" to scrape and clean the text data. <br>
To host the application, we utilized library "streamlit".

## How to use the application:
You can use the application directly at the link provided above (deployed app: https://vndictapp-ek4r3xdf5irkysabnqhewt.streamlit.app/).<br>
The app can also be run locally by opening the "vn_dict" repository and running these codes in the command line:
```
python -m streamlit run Home.py
```

## Files structure:
1/ modules: Python files containing all functions used <br>
a. score_calc.py: functions to score all meanings based on keyword - context sentence <br>
b. scrape_dict.py: functions to scrape the dictionary database<br>

2/ pages: <br>
a. About.py: information about the application (general idea, how it works, data sources, etc.) <br>
b. Analysis.py: a simulation test to quantify the needs to use our application <br>
c. Evaluation.py: model results evaluation <br>
d. images: all images used in the rendered pages <br>
e. analysis_data: test_100.xlsx - testing dataset to evaluate the model performance <br>

3/ trained_logs: <br>
a. M_matrix_final.npy: the trained word co-occurrence matrix <br>
b. dict_final.json: the final word corpus <br>
c. word2vec_100dim_50000.model: the trained Word2Vec model <br>

4/ Home.py: the homepage where we input keyword-context pair to browse results <br>

5/ requirements.txt: all libraries required to run the application <br>

6/ report.pdf: a final report to summarize the project 

## Results
The final dictionary application we built has shown potential to improve the user experience of current traditional dictionaries: less time is required to read explanations for meanings, and a final score is given as a reference for users to analyze the role of a keyword in the context. We can further use this application for other purposes, for example, to improve the dictionary function of Kindle or dictionary plugins currently used on browsers. We believe this application has many potentials worthy to be further explored and utilized.


## Acknowledgements
- Data Sources: <br>
  + News Dataset Vietnamese: https://www.kaggle.com/datasets/phamtheds/news-dataset-vietnameses (owner: The Pham) <br>
  + Vietnamese Wikipedia corpus 2020: https://www.kaggle.com/datasets/89a41b1ac1ff10900b27fdd85da6528fd82b5f72e5b6c45d02213d034243fd8e (owner: Quy Nguyen) <br>
