# Import libraries
import streamlit as st
import os
import numpy as np
import pandas as pd
from PIL import Image

path = os.path.dirname(__file__)

# Set up page
st.set_page_config(layout="wide")

st.title('Model Results Evaluation')

# Overview of results evaluation
with st.expander('Overview ⬇️'):
  st.write('Since there are no available testing methods to evaluate the performance of the application, the testing data had to be created from scratch.')
  st.write('Due to the time limit, we created a testing dataset containing 100 pairs of keywords - context sentences with the correct meaning in each case.')
  test_data_image = Image.open(path+'/images/test_data.png')
  st.image(test_data_image, caption='Example: Test dataset (100 records)')
  st.write('On this testing dataset, the accuracy of predicting keyword meaning is considered the main metric.')
  st.write('''As the number of testing samples is small, these results should only be used as a reference to roughly evaluate how our “intelligent” dictionary application works, 
           not to draw any definitive conclusions about its performance.''')

# All metrics
with st.expander('Metrics ⬇️'):
  metrics_image = Image.open(path+'/images/metrics.png')
  st.image(metrics_image, caption='List of all metrics used')

  # Metric explanations
  st.write('We used accuracy and absolute accuracy to evaluate how well the model is predicting the correct meaning of keywords in test dataset.')
  st.write('Apart from accuracy, we also used prediction score and ratio score, which are defined as below:')
  st.write('''1. Prediction score is defined as the average of the “meaning index” for the correct meaning considering the ordered list of meanings produced by the application. 
           This score would try to estimate the average number of efforts we need to make to reach the correct meaning using this application. ''')        
  st.write('2. The ratio score is similar to the prediction score; however, it also takes the number of meanings for the keyword into consideration.')
  
# Evaluation Results
with st.expander('Evaluation Results ⬇️'):
  results_eval_image = Image.open(path+'/images/results_eval.png')
  st.image(results_eval_image, caption='Results evaluation on testing data (100 records)')
  st.write('''The accuracy and absolute accuracy are quite low for all models (47% and 60.26%); 
           however, as the model got a low prediction score, the correct meaning was ranked in the top of the predicted list of meanings.
           On average, users only need to read 2.48 meanings to find out the correct meaning of the keyword in provided context.
           Moreover, the average amount of time taken for a prediction to be made is 0.05s, 
           which is good enough for users as they would not feel any long delay while waiting for the result.''')
  
# Result Justification
with st.expander('Justification ⬇️'):
  st.write('The low accuracy score of the application may be attributed to various reasons.')
  st.write('''
          A reason behind this result is the low accuracy of the POS tagger model from “underthesea”. 
          This model only managed to predict the POS tag of the keyword correctly in 78 out of 100 testing samples, heavily affecting the performance of our application. 
          False predictions of this POS tagger model often came from sentences with confusing or complex grammatical structures, 
          for example ones in which the keyword is included in a noun clause, or when the keyword is an abbreviated form of a longer word. 
          The POS tagger model would be easily tricked in these cases, causing the dictionary application to sort the final ordered list of meanings. 
          The inconsistency between the system of POS tags used by the POS tagger model of “underthesea” library and 
          the word types in the dictionary database can be another factor affecting the performance of our application.''')
  st.write('''
          The second main problem lies in the dictionary database which we scraped from “Tra Từ” dictionary.
           For some examples of the keyword – context sentence pair, we observed that the meaning list provided by the dictionary did not have the correct meaning for that keyword considering the context. 
           This is especially obvious when the keyword is used in informal conversations, or in dialogues between young people on social media.''')
  st.write('''
          Apart from those external factors, the limitations in our training process also have some negative impacts on the performance of the final application. 
          With the limited RAM resource of our computer, the amount of raw text data we may train is small compared to other readily-built NLP models. 
          The process of training the word co-occurrence matrix also suffers from degradation of accuracy due to the measures 
          we utilized to make up for the lack of memory resources (for example, reducing the size of word co-occurrence matrix).
          Therefore, the word co-occurrence matrix and word vectors we trained may fail to catch a lot of patterns in Vietnamese words and grammar, 
          lowering the accuracy and absolute accuracy of the final dictionary application.''')

# Reflection
with st.expander('Reflection ⬇️'):
  # Conclusion
  st.write('''The final dictionary application we built has shown potential to improve the user experience of current traditional dictionaries: 
             less time is required to read explanations for meanings, 
             and a final score is given as a reference for users to analyze the role of a keyword in the context. 
             We can further use this application for other purposes, for example, 
             to improve the dictionary function of Kindle or dictionary plugins currently used on browsers. 
             We believe this application has many potentials worthy to be further explored and utilized.
             ''')
  # Improvement
  st.write('''To enhance the dictionary's performance, various improvements may be conducted. 
             These improvements can be categorized into three groups: improving external factors, transforming the model, and utilizing users' feedback.''')
  st.write('''The external factors, as previously summarized, regard the resources we used to build the intelligent dictionary: raw text data, dictionary database, and POS tagger model. 
             As the amount of trained raw text data and the resulting word co-occurrence matrix's accuracy is dependent on the available time, memory, and computing resources, 
             we may try to train data on Cloud or other services to increase the size of resources.
             Using readily-trained word vectors or word co-occurrence matrix might also be helpful.''')
  st.write('''Transforming the model, on the other hand, considers the structure and mathematics algorithm which constructs our model. 
             For example, the scoring algorithm may be further optimized to produce a final score which better reflects 
             the relationship between the context sentence and a meaning phrase, and between the context sentence and an example sentence.''')
  st.write('''The last potential improvement we proposed is to utilize users' feedback to create a self-improvement mechanism for the application. 
             This improvement might be achieved by adding a “feedback” form to the interface of our dictionary application. 
             When the application showed the ordered list of meanings, 
             users would be required to rate whether the application has made a correct prediction or not by inputting the index of the correct meaning.
             If the correct meaning is provided in the first position of the resulted list, 
             users would enter “0”, and the correct meaning's index in case the dictionary's prediction is wrong. 
             Using this feedback, the application may add new examples with the classified meaning provided by users to the dictionary database, 
             which would improve its prediction when a similar context sentence is inputted in the future.''')