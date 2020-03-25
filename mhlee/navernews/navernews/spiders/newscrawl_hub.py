# -*- coding: utf-8 -*-
import scrapy
from navernews.items import NavernewsItem
from datetime import timedelta, date, datetime
import re
import requests


class NewscrawlHubSpider(scrapy.Spider):
    name = 'newscrawl_hub'
    pre_url = 'https://news.naver.com/'

    startdate = date.today()
    enddate = date.today()

    def start_requests(self):
        self.enddate = getattr(self, 'end', self.enddate)
        self.startdate = getattr(self, 'start', self.enddate)
        self.startdate = datetime.strptime(self.startdate, "%Y-%m-%d")
        self.enddate = datetime.strptime(self.enddate,"%Y-%m-%d")
        print("basedate" + "-" * 100)
        print("{} ~ {}".format(self.startdate, self.enddate))
        print("basedate" + "-" * 100)
        sid1 = getattr(self, 'sid1', 100)
        sid2 = getattr(self, 'sid2', 269)

        def daterange(start_date, end_date):
            for n in range(int ((end_date - start_date).days+1)):
                yield start_date + timedelta(n)

        for d in daterange(start_date=self.startdate, end_date=self.enddate) :
            url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1={}&sid2={}&date={}&page=1".format(sid1, sid2, d.strftime("%Y%m%d"))
            yield scrapy.Request(url=url
                , callback=self.parse_list
                , meta={'date':d.strftime("%Y-%m-%d")})

    def parse_list(self, response):
        for url in response.css('div.list_body ul li dl dt:not(.photo) a::attr(href)').getall() :
            yield scrapy.Request(url=url
                    , callback=self.parse
                    , meta={'date':response.meta['date'], 'category2':response.xpath("//div[@class='snb']/ul/li[@class='on']//a/text()").get().strip()})

        nextpage = int(re.search(r"(page=[0-9]*)", response.url).group().split('=')[1]) + 1        
        for page in response.css('div.paging a') :
            nextpageurl = int(re.search(r"(page=[0-9]*)", page.attrib['href']).group().split('=')[1])
            if nextpageurl == nextpage:                
                yield scrapy.Request(url=self.pre_url + "main/list.nhn" + page.attrib['href']
                    , callback=self.parse_list
                    , meta={'date':response.meta['date']})
                print("nextpage" + "*"*100)
                print(self.pre_url + page.attrib['href'])

    def parse(self, response):
        url = response.url
        category1 = response.xpath("//div[@class='lnb_menu']/ul/li[@class='on']//span[@class='tx']//text()").get()   
        category2 = response.meta['category2']
        date = response.meta['date']
        title = response.xpath("//h3[@id='articleTitle']/text()").get().replace('"','')
        if title :
            title = title.replace('"','').replace("'","")
        media = response.xpath("//div[@class='press_logo']/a/img/@alt").get()    
        inputdate = response.xpath("//div[@class='article_info']//span[@class='t11']/text()").get()
        summary = response.xpath("//strong[@class='media_end_summary']//text()").get()
        if summary :
            summary = summary.replace('"','').replace("'","")
        cont = response.xpath("//div[@id='articleBodyContents']//text()").getall()   
        cont = ' '.join([item.strip() for item in cont ]) #좌우 공백 제거
        cont = cont[cont.find('{}')+3:] #javascript 함수 제거
        cont = re.sub(r"(\(.*\=)|(\[.*\=)|(\[.*\])","",cont) #기자 매체명 삭제
        #cont = cont[:cont.find(r'▶')] #특수문자
        #cont = cont[:cont.find(r'☞')] #특수문자
        cont = re.sub(r"(\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3}))","",cont) #이메일 삭제
        cont = cont.replace('"','').replace("'","")


        oricategory = response.xpath("//em[@class='guide_categorization_item']//text()").get()   

        oid = re.search(r"(oid=[0-9]*)", response.url).group().split('=')[1]
        aid = re.search(r"(aid=[0-9]*)", response.url).group().split('=')[1]
        react_resp=requests.get('https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&q=NEWS%5Bne_{0}_{1}%5D%7CNEWS_SUMMARY%5B{0}_{1}%5D%7CNEWS_MAIN%5Bne_{0}_{1}%5D&isDuplication=false'.format(oid,aid))
        warm = 0
        like = 0
        want = 0
        angry = 0
        sad = 0
        for react in react_resp.json()['contents'][0]['reactions']:
            if react["reactionType"] == "want" : want = int(react["count"])
            if react["reactionType"] == "like" : like = int(react["count"])
            if react["reactionType"] == "warm" : warm = int(react["count"])
            if react["reactionType"] == "angry" : angry = int(react["count"])
            if react["reactionType"] == "sad" : sad = int(react["count"])

        comment_resp = requests.get('https://news.naver.com/api/comment/listCount.json?resultType=MAP&ticket=news&lang=ko&country=KR&objectId=news{0},{1}'.format(oid,aid))
        comment = comment_resp.json()['result']["news{0},{1}".format(oid,aid)]["comment"]

        updatedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        yield {
            'url' : url,
            'category1' : category1,
            'category2' : category2,
            'date' : date,
            'title' : title,
            'media' : media,
            'inputdate' : inputdate,
            'summary' : summary,
            'content' : cont,
            'oricategory' : oricategory,
            'comment' : comment,
            'updatedate' : updatedate,
            "want" : want,
            "like" : like,
            "warm" : warm,
            "angry" : angry, 
            "sad" : sad
        }

