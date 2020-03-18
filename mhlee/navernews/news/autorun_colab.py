import os
import pandas as pd
import sys

args = sys.argv[1:]

df = pd.read_csv('./cate_list.csv')

for date in pd.date_range(args[0],args[1]) :
    for i, row in df.iterrows() :
        dirName = '/content/drive/My Drive/10 Insight Page/202003 21대 총선분석 프로젝트/데이터 수집/news/' + date.strftime('%Y/%m/%d')

        if not os.path.exists(dirName):
            os.makedirs(dirName)
        filename = "{}/{}_{}.json".format(dirName, date.strftime('%Y%m%d'), row['filename'])
        
        if not os.path.exists(filename):
            print(filename)
            cmd = "scrapy crawl newscrawl -o '%s' -a sid1=%s -a sid2=%s -a end='%s'"%(filename, row['sid1'], row['sid2'], date.strftime('%Y-%m-%d'))
            print(cmd)
            os.system(cmd)