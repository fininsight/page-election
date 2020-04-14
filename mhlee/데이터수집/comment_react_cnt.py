import warnings
warnings.filterwarnings('ignore')

import requests
import re
import os
import pandas as pd
from pathlib import Path
import unicodedata
from tqdm import tqdm_notebook as tqdm

class CollectNewsCommentReactCnt :
    @staticmethod
    def collect(filefolder) :
        
        for path in Path(filefolder).rglob("*.csv"):
            try : 
                #print(path)
                df = pd.read_csv(open(path, "r", encoding="utf8"))
                
                for i in tqdm(range(df.shape[0]), desc=os.path.basename(path)) :
                    if (pd.isnull(df['angry'][i])) & (pd.isnull(df['warm'][i])) & (pd.isnull(df['like'][i])) & (pd.isnull(df['want'][i])) & (pd.isnull(df['comment'][i])) :

                        oid = re.search(r"(oid=[0-9]*)", df['url'][i]).group().split('=')[1]
                        aid = re.search(r"(aid=[0-9]*)", df['url'][i]).group().split('=')[1]
                        comment_url = 'https://news.naver.com/api/comment/listCount.json?resultType=MAP&ticket=news&lang=ko&country=KR&objectId=news{0},{1}'.format(oid,aid)
                        react_url='https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&q=NEWS%5Bne_{0}_{1}%5D%7CNEWS_SUMMARY%5B{0}_{1}%5D%7CNEWS_MAIN%5Bne_{0}_{1}%5D&isDuplication=false'.format(oid, aid)

                        react_resp=requests.get(react_url)
                        for react in react_resp.json()['contents'][0]['reactions']:
                            df[react["reactionType"]][i] = int(react["count"])
                        comment_resp = requests.get(comment_url)
                        df["comment"][i] = comment_resp.json()['result']["news{0},{1}".format(oid,aid)]["comment"]

                df.to_csv(path, index=False)
                #print(path)
            except Exception as e:
                print("Error file : {}".format(path))
                print("Error message : {}".format(str(e)))
                
            #break


path_li = []
for d in pd.date_range('2019-03-01', '2020-03-31') :
    path_li.append("../../../krayon/crawler/scrapy_crawler/data/news_naver/{}/{}/{}".format(d.strftime('%Y'), d.strftime('%m'), d.strftime('%d')))
   
    
import multiprocessing as mp
num_cores = 8#mp.cpu_count() - 5
print(num_cores)
print(len(path_li))

for i in range(0, len(path_li), num_cores) :
    #CollectNewsCommentReactCnt.collect(path_li[i])
    pool = mp.Pool(processes = num_cores)
    pool.map(CollectNewsCommentReactCnt.collect, path_li[i:i+num_cores])
    pool.close()
    pool.join() 