from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import base64
import pdb

#keywords = input('Search keyword: ')
keywords = "애플"

url = 'https://www.google.co.kr/search?q={}&tbm=nws&source=lnt&tbs=qdr:h'.format(keywords)

### 크롬 debug ###
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('chromedriver')
driver.get(url)
cur_url = driver.current_url
############

resp = requests.get(url)
soup = bs(resp.text, 'html5lib')

titles = []
links = []
texts = []

#soup.select('a[aria-label="다음 페이지"]')
for tag in soup.select('h3'):
    print(tag.text)
    tag_parent = tag.parent
    #href = 'https://news.google.com' + link.get('href')[1:]
    #href = 'https://www.google.com' + link_parent.get('href')
    href = tag_parent.get('href')
    news_url = href[href.find('http')::]
    title = tag.string
    titles.append(title)
    links.append(news_url)
    _resp = requests.get(news_url)
    _soup = bs(_resp.text, 'html5lib')
    text = ""
    for _tag in _soup.select('div'):
        #print(_tag.text)
        text += _tag.text\
                    .replace('\n','')\
                    .replace('\t','')\
                    .replace('{','')\
                    .replace('}','') + '\n'
    #print(text)
    #texts.append(_resp.text)
    #pdb.set_trace()

pdb.set_trace()

data = {'title': titles, 'link': links, 'text': texts}
data_frame = pd.DataFrame(data, columns=['title', 'link'])
data_frame.to_csv('./' + keywords + '.csv')
data_frame.to_excel('./' + keywords + '.xlsx')

print("Complete!")