# 현재 신문사 종류 43개, 신문사 갯수가 추가되면 전처리 추가 
#'조선일보|뉴시스|아시아경제|이데일리|뉴스1|SBS|오마이뉴스|중앙일보|매일경제|문화일보|세계일보|머니투데이|서울경제|데일리안|KBS|MBN|YTN|프레시안|디지털타임스|국민일보(과거)|국민일보|헤럴드경제|한국일보|아이뉴스24|노컷뉴스|연합뉴스TV|서울일보|동아일보|한국경제|미디어오늘(과거)|미디어오늘|조세일보|파이낸셜뉴스|경향신문|채널A|머니S|TVCHOSUN|한겨례|전자신문|SBSCNBC|한국경제TV|조선비즈|ZDNetKorea'

import re
class PreprocessNews:
    def __init__(self,df):
        self.df = df
    def preprocess(self):
        df = self.df
        def pre_fx(text):
            # 이메일 등장하면, 그 뒷문장 모두 삭제 
            text = re.sub("[a-zA-Z0-9]+\@[a-zA-Z0-9]+\.[a-z]{1,3}.[a-z]{1,3}.+",'',text).strip()
            text = re.sub('\(.+?연합뉴스\)','',text).strip() # (서울=연합뉴스)
            text = re.sub('\(.+?연합인포맥스\)','',text).strip()
            text = re.sub('\(.+?이데일리\)','',text).strip()
            text = re.sub('\(.+?조선일보\)','',text).strip()
            text = re.sub('\(.+?뉴시스\)',' ',text).strip()
            text = re.sub('\(.+?뉴스1\)','',text).strip()
            text = re.sub('\(.+?SBS\)','',text).strip()
            text = re.sub('\(.+?오마이뉴스\)','',text).strip()
            text = re.sub('\(.+?중앙일보\)','',text).strip()
            text = re.sub('\(.+?매일경제\)','',text).strip()
            text = re.sub('\(.+?문화일보\)','',text).strip()
            text = re.sub('\(.+?세계일보\)','',text).strip()
            text = re.sub('\(.+?머니투데이\)','',text).strip()
            text = re.sub('\(.+?서울경제\)','',text).strip()
            text = re.sub('\(.+?데일리안\)','',text).strip()
            text = re.sub('\(.+?KBS\)','',text).strip()
            text = re.sub('\(.+?MBN\)','',text).strip()
            text = re.sub('\(.+?YTN\)','',text).strip()
            text = re.sub('\(.+?프레시안\)','',text).strip()
            text = re.sub('\(.+?디지털타임즈\)','',text).strip()
            text = re.sub('\(.+?국민일보(과거)\)','',text).strip()
            text = re.sub('\(.+?국민일보\)','',text).strip()
            text = re.sub('\(.+?헤드럴경제\)','',text).strip()
            text = re.sub('\(.+?한국일보\)','',text).strip()
            text = re.sub('\(.+?아이뉴스24\)','',text).strip()
            text = re.sub('\(.+?노컷뉴스\)','',text).strip()
            text = re.sub('\(.+?연합뉴스TV\)','',text).strip()
            text = re.sub('\(.+?서울일보\)','',text).strip()
            text = re.sub('\(.+?동아일보\)','',text).strip()
            text = re.sub('\(.+?한국경제\)','',text).strip()
            text = re.sub('\(.+?미디어오늘(과거)\)','',text).strip()
            text = re.sub('\(.+?미디어오늘\)','',text).strip()
            text = re.sub('\(.+?조세일보\)','',text).strip()
            text = re.sub('\(.+?파이낸셜뉴스\)','',text).strip()
            text = re.sub('\(.+?경향신문\)','',text).strip()
            text = re.sub('\(.+?채널A\)','',text).strip()
            text = re.sub('\(.+?머니S\)','',text).strip()
            text = re.sub('\(.+?TVCHOSUN\)','',text).strip()
            text = re.sub('\(.+?한겨례\)','',text).strip()
            text = re.sub('\(.+?전자신문\)','',text).strip()
            text = re.sub('\(.+?SBSCNBC\)','',text).strip()
            text = re.sub('\(.+?한국경제TV\)','',text).strip()
            text = re.sub('\(.+?조선비즈\)','',text).strip()
            text = re.sub('\(.+?ZDNetKorea\)','',text).strip()
            text = re.sub('\[.+?\]','',text).strip()
            text = re.sub('\(사진.+?\)','',text).strip()
            # 신문사 이름 삭제 
            text = re.sub('조선일보|뉴시스|아시아경제|이데일리|뉴스1|SBS|오마이뉴스|중앙일보|매일경제|문화일보|세계일보|머니투데이|서울경제|데일리안|KBS|MBN|YTN|프레시안|디지털타임스|국민일보(과거)|국민일보|헤럴드경제|한국일보|아이뉴스24|노컷뉴스|연합뉴스TV|서울일보|동아일보|한국경제|미디어오늘(과거)|미디어오늘|조세일보|파이낸셜뉴스|경향신문|채널A|머니S|TVCHOSUN|한겨례|전자신문|SBSCNBC|한국경제TV|조선비즈|ZDNetKorea','',text).strip()
            # 000 기자, 000  가자, 000기자 삭제
            text = re.sub('[ㄱ-힑]+ 기자|[ㄱ-힑]+  기자|[ㄱ-힑]+기자','',text).strip()    
            text = re.sub('[a-zA-Z0-9]{1,20}\@[a-zA-Z0-9]{1,20}\.[a-z]{1,20}.+','',text).strip()    

            return text
    
        df['content'] = df['content'].map(lambda x : pre_fx(x))
    
        # if filename !='':
        #     df.to_csv(filename,index = False)
        return df
