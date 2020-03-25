# -*- coding: utf-8 -*-
import scrapy
from navernews.items import NavernewsItem
from datetime import timedelta, date, datetime
import re
import requests
import time


class NewscrawlSpider(scrapy.Spider):
    name = 'newscrawl'
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
                , meta={'date':d.strftime("%Y-%m-%d"), 'sid1':sid1, 'sid2':sid2})

    def parse_list(self, response):
        curpage = int(re.search(r"(page=[0-9]*)", response.url).group().split('=')[1])
        if curpage == int(response.css('div.paging strong::text').get()) :
            for url in response.css('div.list_body ul li dl dt:not(.photo) a::attr(href)').getall() :
                yield scrapy.Request(url=url
                        , callback=self.parse
                        , meta={'date':response.meta['date'], 'category2':response.xpath("//div[@class='snb']/ul/li[@class='on']//a/text()").get().strip()})

            nextpage = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1={}&sid2={}&date={}&page={}".format(
                response.meta['sid1']
                , response.meta['sid2']
                , response.meta['date'].replace("-","")
                , curpage+1)            
            yield scrapy.Request(url=nextpage
                    , callback=self.parse_list
                    , meta={'date':response.meta['date'], 'sid1':response.meta['sid1'], 'sid2':response.meta['sid2']})

    def parse(self, response):
        item = NavernewsItem()
        item['url'] = response.url
        item['category1'] = response.xpath("//div[@class='lnb_menu']/ul/li[@class='on']//span[@class='tx']//text()").get()   
        item['category2'] = response.meta['category2'] 
        item['date'] = response.meta['date']
        item['title'] = response.xpath("//h3[@id='articleTitle']/text()").get().replace('"','')        
        item['media'] = response.xpath("//div[@class='press_logo']/a/img/@alt").get()    
        item['inputdate'] = response.xpath("//div[@class='article_info']//span[@class='t11']/text()").get()
        item['summary'] = response.xpath("//strong[@class='media_end_summary']//text()").get()
        item['content'] = response.xpath("//div[@id='articleBodyContents']//text()").getall()
        item['oricategory'] = response.xpath("//em[@class='guide_categorization_item']//text()").get()   
        # oid = re.search(r"(oid=[0-9]*)", response.url).group().split('=')[1]
        # aid = re.search(r"(aid=[0-9]*)", response.url).group().split('=')[1]
        # react_resp=requests.get('https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&q=NEWS%5Bne_{0}_{1}%5D%7CNEWS_SUMMARY%5B{0}_{1}%5D%7CNEWS_MAIN%5Bne_{0}_{1}%5D&isDuplication=false'.format(oid,aid))
        # for react in react_resp.json()['contents'][0]['reactions']:
        #    item[react["reactionType"]] = int(react["count"])
        # comment_resp = requests.get('https://news.naver.com/api/comment/listCount.json?resultType=MAP&ticket=news&lang=ko&country=KR&objectId=news{0},{1}'.format(oid,aid))
        # item['comment'] = comment_resp.json()['result']["news{0},{1}".format(oid,aid)]["comment"]
        item['updatedate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield item
