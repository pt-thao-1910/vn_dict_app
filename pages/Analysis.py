# Import libraries
import streamlit as st
import os
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px

path = os.path.dirname(__file__)

# Set up page
st.set_page_config(layout="wide")


# Title
st.title('Analysis: A simulation test')
st.write('This is an effort to quantify the need to use our intelligent dictionary application.')

# Step 1
st.header("Step 1: Test Samples Pick-up")
st.write('We used the list of 100 pairs of keyword - context sentence used in testing data.')  

# Step 2
st.header('Step 2: Generate values of “meaning index”')
st.write('''We would number each meaning in the result meaning list for the keyword provided by the dictionary and find the number of the right meaning considering the context. 
         This number is the value of the “meaning index”, which illustrates the number of attempts we need to make before reaching the correct meaning if reading the meaning list from top to bottom.''')
meaning_index_image = Image.open(path+'/images/meaning_index.png')
st.image(meaning_index_image, caption='Example: scraped meaning list for sample word “mua”')
st.write('''
         When the context sentence is “Chẳng ai muốn mua cái bực vào người” (No one wants to be provoked with anger), the meaning (4) is correct, 
         which means the “meaning index” should be set to 4. The result table for this keyword “mua” would look as below.''')
mua_result_image = Image.open(path+'/images/mua_result.png')
st.image(mua_result_image, caption='Example: format of the simulation test result table')

# Step 3
st.header("Step 3: Evaluation")
st.write('''Evaluation is made by calculating the mean of column “meaning index”. 
         The smaller this number is, the fewer attempts we have to make in reading the meaning list before reaching the correct meaning of the keyword considering the context sentence. ''')
st.write('The result looks as follows:')

df = pd.read_excel(path + "/analysis_data/test_100.xlsx", header=0)
df_cnt = df["meaning_index"].value_counts().reset_index()
df_cnt.columns = ["meaning_index", "count"]

fig = px.bar(df_cnt, x="meaning_index", y="count",
             title="Distribution of meaning index in test data (100 records)")
st.plotly_chart(fig)

st.write('''We may see that over 70% of cases, we need to read at least 2 meanings from top to bottom to find out the correct meaning in the dictionary.
         The average value of 'meaning_index' is around 5.8; which means that on average, you need to read 5.8 meanings from the top.
         There also exist an extreme case when we have to read 13 meanings to reach the correct one regarding the context sentence.''')
st.write("For these cases, the “intelligent” dictionary would be very useful and save us some minutes spent on reading unrelated information.")
st.write("Therefore, we conclude that the use of our dictionary would be beneficial for many dictionary users.")