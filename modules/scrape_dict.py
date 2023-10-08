from bs4 import BeautifulSoup
import requests

def web_scraping(word, results):
    '''
    Scrape dictionary database for the searched keyword
    
    Input: 
    + word (string): keyword to search
    + results (list): result list to update the browsed results
    Output: results (list) - updated result list after appending results of the searched keyword
    '''
    src_url='http://tratu.soha.vn/dict/vn_vn/'
    word_searched = '_'.join(str(word).lower().split(" "))
    url = src_url + word_searched
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,"lxml")
    
    summary = soup.find('div',{'id':'bodyContent'})
    sections = summary.find_all('div', {'id': 'content-3'})
    
    for i in range(len(sections)):
        word_type = sections[i].find('span', {'class': 'mw-headline'}).get_text().strip()
        meanings = sections[i].find_all('div', {'class': 'section-h5'})
        for j in range(len(meanings)):
            mn = meanings[j].find('span', {'class':'mw-headline'}).get_text().strip()
            examples = meanings[j].find_all('i')
            exps = " \n ".join(list(map(lambda x: x.get_text().strip(), examples)))
            results.append([word, word_type, mn, exps])
            
