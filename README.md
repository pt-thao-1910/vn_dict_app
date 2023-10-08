# Vietnamese intelligent dictionary application
This is a Vietnamese dictionary which provides list of ordered meaning based on the context sentence.
We aim to enhance your experience when using online dictionaries by reducing the time needed to be spent on finding out the right meaning among a long list of meanings and explanations.

## Project Motivation
One of the most common problem for current online dictionaries we observe nowadays is the lack of consideration for context. When searching for a keyword, the dictionary simply returns a list of meanings regardless of what context the keyword is in. Therefore, when browsing for the correct meaning of a word, dictionary users often have to read through the whole explanation for the keyword, which can be very time consuming and inconvenient, especially when the keyword has multiple meanings and word types. To solve the problem, we hope to build an intelligent dictionary that can present meanings based on the the context sentence using some simple natural language processing methods.

## How the application works
The general idea is to find out the correct meaning by calculating a similarity score between each meaning and corresponding example sentences provided by the dictionary with the context sentence (provided by user) through:
1/ Co-occurrence score: similarity between meaning – context sentence
2/ Word vector score: similarity between example sentences – context sentence
We also use POS tagger to make sure the meaning have the correct word type (noun, verbs, etc.) based on the context sentence.

## Files structure:
1/ modules: Python files containing all functions used
a. score_calc.py: functions to score all meanings based on keyword - context sentence
b. scrape_dict.py: functions to scrape the dictionary database
2/ pages:
a. About.py: 
b. Analysis.py: 
c. Evaluation.py:
d. images: all images used in the rendered pages
e. analysis_data:
   + test_100.xlsx: testing dataset to evaluate the model performance
3/ trained_logs:
a. M_matrix_final.npy: the trained word co-occurrence matrix
b. dict_final.json: the final word corpus
c. word2vec_100dim_50000.model: the trained Word2Vec model
4/ Home.py: the homepage where we input keyword-context pair to browse results
5/ requirements.txt: all libraries required to run the application

## Results
The final dictionary application we built has shown potential to improve the user experience of current traditional dictionaries: less time is required to read explanations for meanings, and a final score is given as a reference for users to analyze the role of a keyword in the context. We can further use this application for other purposes, for example, to improve the dictionary function of Kindle or dictionary plugins currently used on browsers. We believe this application has many potentials worthy to be further explored and utilized.
