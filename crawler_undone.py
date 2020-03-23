import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+|\r|\n|\t| |　|"
script_str = 'varamp_med=\'2000689\';varamp_site=\'2000850\';varamp_frame=\'2007958\';varamp_rurl=document.referrer;varamp_send=location.protocol+\'//ads.adjust-net.jp/adserver/ad/ads_v.js?\'+Math.random();document.write(\"<scr\"+\"ipttype=\'text/javascript\'src=\'\"+amp_send+\"\'></scr\"+\"ipt>\");'

df_done = pd.read_table('data.tsv',header=None,index_col=0)
df_done = df_done.dropna(how='any')
done_list = df_done.index.values

df = pd.read_csv('data/train2.csv',header=None)
id_list = df[3]
with open('data_undone.tsv','w') as f:
    for idx, page_id in enumerate(id_list):
        try:
            if str(idx) in done_list:
                continue
            time.sleep(1)
            if '.' in page_id:
                page_id = page_id.split('.')[0]
            print(idx,'/',len(id_list), page_id)
            url = "https://news.livedoor.com/article/detail/{}/".format(page_id)
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            bs = BeautifulSoup(response.text, 'html.parser')
            
            if bs.find('p', class_='topicsTxt') is not None:
                if bs.find('p', class_='topicsTxt').text == '提供社の都合により、削除されました。概要のみ掲載しております。':
                    print('提供社の都合により、削除されました。概要のみ掲載しております。')
                    continue

            data=[str(idx)]
            #summary
            print('summary')
            bs_ul = bs.find('ul', class_='summaryList')
            for bs_li in bs_ul.find_all('li'):
                data.append(bs_li.text)
            if len(data)!=4:
                continue
            #body
            print('body')
            bs_body = bs.find('div', class_='articleBody').find('span')
            data.append(bs_body.text)
            script_str = 'varamp_med=\'2000689\';varamp_site=\'2000850\';varamp_frame=\'2007958\';varamp_rurl=document.referrer;varamp_send=location.protocol+\'//ads.adjust-net.jp/adserver/ad/ads_v.js?\'+Math.random();document.write(\"<scr\"+\"ipttype=\'text/javascript\'src=\'\"+amp_send+\"\'></scr\"+\"ipt>\");'
            data = [re.sub(pattern,'',txt).replace(script_str,'') for txt in data]
            f.write('\t'.join(data)+'\n')
            print('\t'.join(data))
        except Exception as e:
            print(url)
            print(e)
            continue
