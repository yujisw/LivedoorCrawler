import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
df = pd.read_csv('data/train2.csv',header=None)
id_list = df[3]
with open('data.tsv','w') as f:
    for idx, page_id in enumerate(id_list):
        try:
            time.sleep(0.01)
            if '.' in page_id:
                page_id = page_id.split('.')[0]
            print(idx,'/',len(id_list), page_id)
            url = "https://news.livedoor.com/article/detail/{}/".format(page_id)
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            bs = BeautifulSoup(response.text, 'html.parser')
            data=[str(idx)]
            #summary
            # print('summary')
            bs_ul = bs.find('ul', class_='summaryList')
            for bs_li in bs_ul.find_all('li'):
                data.append(bs_li.text)
            #body
            # print('body')
            body=[]
            if bs.find('p', class_='topicsTxt') is not None:
                if bs.find('p', class_='topicsTxt').text == '提供社の都合により、削除されました。概要のみ掲載しております。':
                    # print('提供社の都合により、削除されました。概要のみ掲載しております。')
                    continue
            bs_body = bs.find('div', class_='articleBody').find('span')
            if bs_body.find_all('p') == []:
                body.append(bs_body.text.replace('\t',''))
            else:
                for bs_p in bs_body.find_all('p'):
                    if bs_p.find('a') is None:
                        body.append(bs_p.text.replace('\t',''))
            data.append(''.join(body))
            f.write('\t'.join(data)+'\n')
        except Exception as e:
            print(url)
            print(e)
            continue
