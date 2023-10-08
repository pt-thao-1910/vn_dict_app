# Import libraries
import streamlit as st
import numpy as np
import json
from gensim.models import word2vec
import modules.scrape_dict as sd
import modules.score_calc as sc

# Import necessary data
co_matrix = np.load('trained_logs/M_matrix_final.npy')

decoder = json.JSONDecoder()
with open('trained_logs/dict_final.json', encoding='utf-8') as user_file:
    w_dict, _ = decoder.raw_decode(user_file.read())

word2vec_mod = word2vec.Word2Vec.load("trained_logs/word2vec_100dim_50000.model")

# Set up page
st.set_page_config(layout="wide")

st.markdown("""
<style>
.small-font {
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# Set up the session state
if st.session_state.get('step') is None:
     st.session_state['step'] = 0

# Homepage Content

user = st.sidebar.text_input('Username')
with st.sidebar.expander("Contact Us"):
    st.markdown('<p class="small-font">📧 pt.thao.1910@gmail.com</p>', unsafe_allow_html=True)

# Title
st.title('📖 Intelligent Vietnamese Dictionary')

with st.expander('About this app'):
  st.write('🙇‍♀️ This is a Vietnamese dictionary which provides list of ordered meaning based on the context sentence.')

with st.expander('For non-Vietnamese users to try out the application:'):
    st.write('You may try this pair of keyword - context sentence: "rơi" - "Tôi đâu ngờ rằng mình sẽ rơi vào hoàn cảnh trớ trêu thế này".')

# Input form
st.header('Input form')
context = st.text_input('Context Sentence')
word = st.text_input('Keyword')

if st.button('Submit'):
     # Calculate scores for each meaning of the keyword and print out the results
     res_list = sc.score_calc_phraser(word, context, co_matrix, w_dict, word2vec_mod, [1,2], sd.web_scraping)
     if isinstance(res_list, str):
          st.write("⚠️" + res_list)
          st.session_state['step'] = 0
          
     else:
          print_list = res_list[['word', 'word_type', 'meaning', 'examples', 'score']]
          st.header('Output')
          st.markdown(f'''
             You have entered:
             - Keyword: `{word}`
             - Context sentence: `{context}`
             ''')
          st.dataframe(print_list)
          st.session_state['step'] = 1
          st.session_state['print_list'] = print_list

# To browse results for other keywords
if st.session_state['step']==1:
     st.header('Continue browsing for the meaning of another keyword ⬇️')
     submitted = st.button("Click here!")

     if submitted:
          st.session_state['step']=0
          st.experimental_rerun()
