import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
df = pd.read_csv('data/train.csv',header=None)
id_list = df[3]
for idx, page_id in enumerate(id_list):
    try:
        time.sleep(1)
        url = "https://news.livedoor.com/article/detail/{}/".format(page_id)
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        bs = BeautifulSoup(response.text, 'html.parser')
        data=[str(idx)]
        #summary
        bs_ul = bs.find('ul', class_='summaryList')
        for bs_li in bs_ul.find_all('li'):
            data.append(bs_li.text)
        #body
        body=[]
        bs_body = bs.find('div', class_='articleBody').find('span')
        for bs_p in bs_body.find_all('p'):
            if bs_p.find('a') is None:
                body.append(bs_p.text.replace('\t',''))
        data.append(''.join(body))
        print('\t'.join(data))
    except Exception as e:
        continue
