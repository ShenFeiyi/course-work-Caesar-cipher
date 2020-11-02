# -*- coding:utf-8 -*-
import os
import re
import time
import requests
from bs4 import BeautifulSoup as BS

START = time.time()

base_url = 'https://www.cgtn.com/'
category = ['Business','Politics','Opinions','Culture','Sports','Travel','Nature']

save_path = 'text'

base_response = requests.get(base_url)
base_soup = BS(base_response.text,'html.parser')
for cate in category:
    with open(os.path.join('.',save_path,'`news` `'+cate.lower()+'` CGTN.txt'),'w') as file:
        base_result = base_soup.find_all('li',{'data-click-name':cate})
        for base_res in base_result:
            if not base_res is None:
                base_http = re.search('http',str(base_res))
                base_cate = re.search(cate.lower(),str(base_res))
                cate_url = str(base_res)[base_http.span()[0]:base_cate.span()[1]]
                cate_response = requests.get(cate_url)
                cate_soup = BS(cate_response.text,'html.parser')
                cate_result = cate_soup.find_all('h4')
                for cate_res in cate_result:
                    if not cate_res is None:
                        cate_http = re.search('http',str(cate_res))
                        cate_html = re.search('html',str(cate_res))
                        if (not cate_http is None) and (not cate_html is None):
                            news_url = str(cate_res)[cate_http.span()[0]:cate_html.span()[1]]
                            news_response = requests.get(news_url)
                            news_soup = BS(news_response.text,'html.parser')
                            news_result = news_soup.find_all('p')
                            for news_res in news_result:
                                news_head = re.search('<p>',str(news_res))
                                news_end = re.search('</p>',str(news_res))
                                if (not news_head is None) and (not news_end is None):
                                    news_almost = str(news_res)[news_head.span()[1]:news_end.span()[0]]
                                    inside = False
                                    for c in news_almost:
                                        if c == '<':
                                            inside = True
                                        if not inside:
                                            file.write(c)
                                        if c == '>':
                                            inside = False
                FINISH = time.time()
                print('{:.2f} seconds.'.format(FINISH-START))

FINISH = time.time()
print('Using {:.2f} seconds.'.format(FINISH-START))
