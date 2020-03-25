import os
import pandas as pd

for date in pd.date_range('2020-01-01','2020-03-14') :
    cmd = "scrapy crawl newsbycategory -o %s.json -a end='%s'"%(date.strftime('%Y%m%d'), date.strftime('%Y-%m-%d'))

    os.system(cmd)