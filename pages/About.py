# Import libraries
import streamlit as st
import os
import numpy as np
import pandas as pd
from PIL import Image

path = os.path.dirname(__file__)

# Set up page
st.set_page_config(layout="wide")

st.title('Intelligent Vietnamese Dictionary')

# About this app
with st.expander('About this app ⬇️'):
  st.write('This is a Vietnamese dictionary which provides list of ordered meaning based on the context sentence.')
  st.write('We aim to enhance your experience when using online dictionaries by reducing the time needed to be spent on finding out the right meaning among a long list of meanings and explanations.')

# Background of the application
with st.expander('Background ⬇️'):
  st.write('''One of the most common problem for current online dictionaries we observe nowadays is the lack of consideration for context. 
              Dictionaries we have today are built using databases with SQL-like code (most commonly used commands are SELECT and WHERE) 
              which only filter the searched keyword using some constraints. 
              In other words, they only consider the searched keyword, not its context sentence when distributing linguistics information regarding that keyword to users. 
              Therefore, when browsing for the correct meaning of a word, dictionary users often have to read through the whole explanation for the keyword, 
              which can be very time consuming and inconvenient, especially when the keyword has multiple meanings and word types. 
              To solve the problem, we hope to build an intelligent dictionary that can present meanings based on the the context sentence using some simple natural language processing methods.''')
  st.write('The desired output of our application is as follows:')
  app_output_image = Image.open(path+'/images/app_output.png')
  st.image(app_output_image, caption='Desired output')

# General idea of the application
with st.expander("General idea ⬇️"):
  st.write('When looking up the meaning of a keyword in the dictionary, we are provided with a list of meanings and example sentences for each of the meaning provided.')
  dict_image = Image.open(path+'/images/dict_image.png')
  st.image(dict_image, width=800, caption="Browsing results of keyword 'dependency' (Oxford's Learner Dictionary)")

  st.write('Having the context sentence "A complete dependency on gas and oil may have negative impacts in the long run.", we realized the correct meaning often have 2 characteristics:')
  st.write('1/ The meaning often have words co-occur with context sentence (share the same topic)')
  st.write('2/ The context examples for the meaning contain words having similar meaning to words in the context sentence.')
  st.write('Therefore, we find out the correct meaning by calculating a similarity score between each meaning and corresponding example sentences provided by the dictionary with the context sentence (provided by user) through:')
  st.write('1/ Co-occurrence score: similarity between meaning – context sentence')
  st.write('2/ Word vector score: similarity between example sentences – context sentence')
  st.write('We also use POS tagger to make sure the meaning have the correct word type (noun, verbs, etc.) based on the context sentence.')

# How the application works
with st.expander('How the application works ⬇️'):  
  st.write('''
          The application is constructed with 4 main components: dictionary database, text-processing model, keyword meaning's scoring model, and input-output channel. 
          
          Overall, the application would get input from users through the input-output channel. 
          After filtering the dictionary database using inputted pairs of a keyword-context sentence, the text-processing model would process the inputted texts from users. 
          The cleaned inputted text from the text-processing model, along with filtering results from the dictionary database, would then be used to calculate the scores by the keyword meaning’s scoring model. 
          Finally, with outputs from the keyword meaning’s scoring model, the output channel would provide users with a list of ordered meanings of the searched keyword in the considered context.
          ''')
  app_construction_image = Image.open(path+'/images/app_construction.png')
  st.image(image=app_construction_image, width=1000, caption='Construction of the application')

  st.header('Dictionary database')
  st.write('''We scraped the Vietnamese dictionary database from tratu.soha.vn.
            The dictionary database used in the application has the same basic structure as other current dictionary databases, 
            but considering the memory capacity, we limited the fields to “word id”, “word”, “word type”, “meaning” and “example”.''')
  scraped_dict_image = Image.open(path+'/images/scraped_dict.png')
  st.image(image=scraped_dict_image, caption='Example: The scraped dictionary database')

  st.header('Text-processing model')
  st.write('''The text-processing model is designed for two main functions: text cleaning and word tokenization. 
              We cleaned the input keyword and context sentence through various steps: remove all unnecessary spaces and unwanted characters (numbers and special characters), then lowercase all characters.
              After finishing the step of cleaning the raw text, we applied word tokenization to the cleaned text. 
              We used the tokenizer of “underthesea” library to tokenize text data into a list of text at the word level including unigrams, bigrams, and multi-grams.
           ''')
  
  st.header("Keyword meaning's scoring model")
  st.write("There are 3 main components: POS tagger, word co-occurrence matrix, and word vectors.")
  st.write('''
           The POS tagger model would tokenize the text and predict the word type of the keyword. 
           In case the keyword exists more than once in the context sentence, the model would give results based on the first occurrence of that keyword. 
           Using the predicted word type, we can filter the meanings scraped from the dictionary database with the corresponding word type. 
           ''')
  st.write('''
           The second component is the word co-occurrence matrix built from text data, which is used for calculating co-occurrence scores between pairs of a meaning - context sentence. 
           This word co-occurrence matrix is built along with the word dictionary which helps navigate the word corresponding to each index of the matrix. 
           ''')
  
  co_occurrence_score_image = Image.open(path+'/images/co_occurrence_score.png')
  st.image(image=co_occurrence_score_image, caption='Formula: Co-occurrence score between a pair of meaning - context sentence (w1: all words in context sentence, w2: all words in meaning)')
  st.write('''The last component, word vectors, generates the word vector score between pairs of example sentences - context sentence.
           To generate the word vector score, we built the word vectors for a Vietnamese corpus by applying word2vec. 
           Having readily-built word vectors, the formula of word vector score is as follows:''')
  
  word_vector_score_image = Image.open(path+'/images/word_vector_score.png')
  st.image(image=word_vector_score_image, caption='Formula: Word vector score between a pair of example sentence - context sentence (w1: all words in context sentence, w2: all words in example sentence)')
  st.write('''We then calculate the final score as a weighted average of the co-occurrence score and word vector score, which would be used to produce outputs.
              The smaller the final score is, the more likely that meaning is the correct meaning of the keyword based on its context.''')
  
  final_score_image = Image.open(path+'/images/final_score.png')
  st.image(image=final_score_image, caption='Formula: Final score of a meaning based on keyword - context sentence provided')

# Data sources
with st.expander('Data sources ⬇️'):
  st.write('1. Dictionary database source: http://tratu.soha.vn/')
  st.write('2. The word co-occurrence matrix and word vectors we used were trained on raw text data from the following sources:')
  text_data_source_image = Image.open(path+'/images/text_data_source.png')
  st.image(image=text_data_source_image, caption='Text data sources used')