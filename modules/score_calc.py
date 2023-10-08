import pandas as pd
import numpy as np
from underthesea import pos_tag, word_tokenize
import requests
import regex
import json


def clean_test_dat(text):
    '''
    Clean the input text data
    
    Input: text (string) - raw text to be cleaned
    Output: cleaned_text (string) - the text after cleaning
    '''
    cleaned_text = text.lower().strip()
    cleaned_text = regex.sub(r'[^\p{Latin}\s]+', u'', cleaned_text)
    return cleaned_text


def remove_items(test_list, item):
    '''
    Remove all occurrences of an item from the list test_list
    
    Input:
    + test_list (list): the list to remove items
    + item: the item to remove
    Output: res (list) - the result list after removing all occurrences of item
    '''
    res = [i for i in test_list if i != item]
    return res


def vn_pos_tag(tag):
    '''
    Return corresponding Vietnamese word type in Tra Tu dictionary from inputted English POS tag
    
    Input: tag (string) - English POS tag
    Output: vn_tag (string) - corresponding Vietnamese POS tag
    '''
    pos_dict = {
               ('N', 'Np', 'Nc', 'Ny', 'Nu', 'M', 'L'): 'Danh từ',
               'A': 'Tính từ',
               ('V', 'Vy'): 'Động từ',
               'P': 'Đại từ',
               'R': 'Phụ từ', 
               'T': 'Trợ từ',
               'I': 'Cảm từ', 
                ('E', 'C', 'CC'): 'Kết từ', 
                ('Z', 'X'): 'Không rõ'
               }
    for (en_tag, vn_tag) in pos_dict.items():
        if (tag==en_tag) or (tag in en_tag):
            return vn_tag

    
def distance(w1, w2, word2vec_model):
    '''
    Return the Euclidean distance between 2 words given their word vectors
    
    Input: 
    + w1, w2 (string) - 2 words to calculate distance
    + word2vec_model: trained Word2Vec model
    Output: dist (float) - Euclidean distance between 2 given words
    '''
    dist = np.linalg.norm(word2vec_model.wv[w1] - word2vec_model.wv[w2])
    return dist


def vector_score_calc(text, examples, word2vec_model):
    '''
    Return the word vector scores between context sentence and example sentences for each meaning
    
    Input: 
    + text (string): context sentence
    + examples (list of list of string): list of example sentences for each meaning
    + word2vec_model: trained Word2Vec model
    Output: scores (list of float) - list of word vector scores between context sentence and example sentences of each meaning
    '''
    n = len(examples) # number of meanings
    scores = np.array([None]*n)
    
    for i in range(n):
        ex_score = []
        ex_i = examples[i]
        ex_i = ex_i.split("\n")
        for ex in ex_i:
            ex = ex.split(" ")
            (ex_sum, ex_cnt) = (0, 0)
            for w in text:
                w_sum = []
                for w2 in ex:
                    try:
                        w_sum.append(distance(w, w2, word2vec_model))
                    except:
                        continue 
                if w_sum!=[]:
                    ex_sum+=min(w_sum)
                    ex_cnt+=1
            if (ex_cnt!=0):
                ex_score.append(ex_sum/ex_cnt)
        if ex_score!=[]:        
            scores[i] = min(ex_score)
  
    try:
        norm = np.linalg.norm(np.array(scores)[scores!=None])
        for i in range(n):
            if (scores[i]):
                scores[i] = scores[i]/norm
        return scores
    
    except:
        return scores    


def co_occur_score_calc(text, meanings, w_dict, co_matrix):
    '''
    Return the co-occurrence score between context sentence and each meaning
    
    Input: 
    + text (string): context sentence
    + examples (list of string): list of meanings
    + w_dict (dict): dictionary of all words in the trained corpus
    + co_matrix (numpy matrix): trained word co-occurrence matrix
    Output: scores (list of float) - list of co-occurrence scores between context sentence and each meaning
    '''
    n = len(meanings)
    sums = [0]*n
    cnt = [0]*n
    scores = []
    
    for w in text:
        try:
            w_idx = w_dict[w]
            for i in range(n):
                mn = meanings[i]
                for w2 in mn:
                    try:
                        w2_idx = w_dict[w2]
                        sums[i] += int(co_matrix[w_idx, w2_idx]) + int(co_matrix[w2_idx, w_idx])
                        cnt[i] += 1
                    except:
                        continue
        except:
            continue   
    
    for i in range(n):
        if cnt[i]==0:
            scores.append(None)
        elif sums[i]==0:
            scores.append(10)
        else:
            scores.append(cnt[i]/sums[i])
    try:
        norm = np.linalg.norm(np.array(scores)[scores!=None])
        for i in range(n):
            if (scores[i]):
                scores[i] = scores[i]/norm
        return scores
    
    except:
        return scores    

    
def predict_pos_tag(text, word):
    '''
    Return the POS tag for the word in the context sentence
    
    Input: 
    + text (string): context sentence
    + word (string): keyword to find POS tag
    Output: word_type (string) - the Vietnamese POS tag for the keyword in the context sentence
    '''
    pos_res = pos_tag(text.lower())
    
    # Case 1: keyword is matched with 1 tokenized word
    for (w, w_type) in pos_res:
        if w==word:
            return vn_pos_tag(w_type)
        
    # Case 2: keyword is included in the tokenized word
    for (w, w_type) in pos_res:
        if word in w:
            pos_res2 = pos_tag(word)
            for (w2, w_type2) in pos_res2:
                if w2==word:
                    return vn_pos_tag(w_type2)               
            return vn_pos_tag(w_type)
        
    # Case 3: keyword includes 2 or more tokenized word
    idx = text.index(word)
    i=0
    check_len = 0
    while check_len<idx:
        check_len += len(pos_res[i][0]) + 1
        i+=1
    word_type = pos_res[i-1][1]
    word_type = vn_pos_tag(word_type)
    return word_type

    
def score_calc_phraser(word, text, co_matrix, w_dict, word2vec_model, weights, scrape):
    '''
    Return the list of ordered meanings for the keyword in the context sentence based on calculated final scores
    
    Input: 
    + word (string): keyword
    + text (string): context sentence
    + co_matrix (numpy matrix): trained word co-occurrence matrix
    + w_dict (dict): dictionary of all words in the trained corpus
    + word2vec_model: trained Word2Vec model
    + weights (list): weights of co-occurrence score and word vector scores in the calculation of final score
    + scrape (function): function to scrape the Vietnamese dictionary database
    Output: results (dataframe) - ordered list of meanings
    '''
    results = []
    scrape(word, results)
    results = pd.DataFrame(results, columns=['word', 'word_type', 'meaning', 'examples'])
    #print(results)
    
    # POS tagging
    results['pred_word_type'] = predict_pos_tag(text, word)
    
    # Clean text
    cleaned_text = clean_test_dat(text)
    word = "_".join(word.split(" "))
    w_idx = len(cleaned_text.split(word)[0].split(" "))
    cleaned_text = cleaned_text.replace(word, "")
    cleaned_text = remove_items(cleaned_text.split(" "), "")
    cleaned_text = cleaned_text[max(w_idx-8, 0):min(w_idx+8, len(cleaned_text))]
    results['cleaned_meaning'] = results['meaning'].map(lambda x: clean_test_dat(x))
    results['cleaned_examples'] = results['examples'].map(lambda x: clean_test_dat(x.replace(word, "")))
    
    # Tokenize text
    cleaned_text = word_tokenize(" ".join(cleaned_text))
    results['cleaned_meaning'] = results['cleaned_meaning'].map(lambda x: word_tokenize(x))
    results['cleaned_examples'] = results['cleaned_examples'].map(lambda x: " ".join(word_tokenize(x)))
        
    # Co-occurrence score
    meanings = list(results['cleaned_meaning'])
    co_occur_scores = co_occur_score_calc(cleaned_text, meanings, w_dict, co_matrix)
    results['co_occur_score'] = list(co_occur_scores)
    
    # Word vector score
    examples = list(results['cleaned_examples'])
    results['w_vector_score'] = list(vector_score_calc(cleaned_text, examples, word2vec_model))
    
    # Final score
    results['score'] = (results['co_occur_score'].fillna(1)*weights[0] + results['w_vector_score'].fillna(1)*weights[1])/sum(weights)    
    results['word_type_check'] = (results['word_type']!= results['pred_word_type'])
    results.sort_values(by=['word_type_check', 'score'], ascending=[True, True], inplace=True)
    results.reset_index(inplace=True)
    return results
