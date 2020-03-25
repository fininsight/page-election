import pandas as pd
import os
from os import path
import re
import requests
import json

import scrapy
from comment_crawler.items import CommentCrawlerItem
from datetime import timedelta, date, datetime

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

date_pattern = re.compile(r'(date=)(\d{8})')

class CommentSpider(scrapy.Spider):
    name = "comment_naver"

    startdate = str(date.today())
    enddate = str(date.today())

    start_urls = []
    
    comment_url = 'https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=view_politics&pool=cbox5&lang=ko&country=KR&objectId=news{}%2C{}&categoryId=&pageSize={}&indexSize=10&groupId=&listType=OBJECT&pageType=more&page={}&initialize=true&userType=&useAltSort=true&replyPageSize=20&moveTo=&sort={}&cleanbotGrade=2&includeAllStatus=true'

    def __init__(self,  filename='', start= '', end=''):
        self.enddate =  datetime.strptime(self.enddate, "%Y-%m-%d") if end == '' else datetime.strptime(end, "%Y-%m-%d")
        self.startdate = datetime.strptime(self.startdate, "%Y-%m-%d") if start == '' else datetime.strptime(start, "%Y-%m-%d")
        

        filepath = os.path.join(os.getcwd(), filename)
        if not path.exists(filepath):
            print('can not find {}'.format(filepath))
            return 

        df = pd.read_csv(filepath)

        def daterange(start_date, end_date):
            for n in range(int ((end_date - start_date).days+1)):
                yield start_date + timedelta(n)

        for cur_date in daterange(start_date=self.startdate, end_date=self.enddate) :
            for i, row in df.iterrows() :
                dirName = 'comments/' + cur_date.strftime('%Y/%m/%d')

                if not os.path.exists(dirName):
                    os.makedirs(dirName)
                filename = "{}/{}_{}.json".format(dirName, cur_date.strftime('%Y%m%d'), row['filename'])
                url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1={}&sid2={}&date={}&page=1".format(row['sid1'], row['sid2'], cur_date.strftime("%Y%m%d"))

                
                self.start_urls.append(url)
        # raise StopIteration

    def start_requests(self):
        return (scrapy.Request(url, callback=self.parse_list) for url in self.start_urls)
    
    def parse_list(self, response):
        for url in response.css('div.list_body ul li dl dt:not(.photo) a::attr(href)').getall() :
            yield scrapy.Request(url=url
                    , callback=self.parse_page
                    , errback=self.errback_httpbin
                    , meta={'date':re.search(date_pattern, response.url).groups()[1], 'category2':re.sub('[/ ]', '', response.xpath("//div[@class='snb']/ul/li[@class='on']//a/text()").get().strip())})
        
        cur_page = int(re.search(r"(page=[0-9]*)", response.url).group().split('=')[1])
        for page in response.css('div.paging a') :
            nextpage = int(re.search(r"(page=[0-9]*)", page.attrib['href']).group().split('=')[1])
            if cur_page + 1 == nextpage:
                yield scrapy.Request(url=response.urljoin(page.attrib['href'])
                    , callback=self.parse_list
                    , errback=self.errback_httpbin)
        
    def _get_response(self,url, headers=None):
        try:
            if not headers:
                r = requests.get(url)
            else:
                r = requests.get(url, headers=headers)
            
            html = r.text
            html = html[10:-2]
            response = json.loads(html)
            # print(response['result'])
            return response
        except:
            return {}

    def parse_page(self, response):
        url = response.url
        category1 = response.xpath("//div[@class='lnb_menu']/ul/li[@class='on']//span[@class='tx']//text()").get()   
        category2 = response.meta['category2'] 
        date = response.meta['date']
        title = response.xpath("//h3[@id='articleTitle']/text()").get().replace('"','')  
        oid = re.search(r"(oid=[0-9]*)", response.url).group().split('=')[1]
        aid = re.search(r"(aid=[0-9]*)", response.url).group().split('=')[1]
        request_resp = self._get_response(self.comment_url.format(oid, aid, 10, 1, 'favorite'), headers={'Referer':response.url})
 
        n_comments = request_resp.get('result', {}).get('count', {}).get('comment', 0)
        max_page = round(n_comments/100 + 0.5)
        print('comment size : {}, max_page : {}'.format(n_comments, max_page))

        for page in range(0, max_page):
            yield scrapy.Request(url=self.comment_url.format(oid, aid, 100, page + 1, 'favorite')
                    , headers = {'Referer':response.url}
                    , callback=self.parse
                    , errback=self.errback_httpbin
                    , meta={
                            'url':url,
                            'title':title,
                            'date':date, 
                            'category2':category2,
                            'category1':category1,
                            'n_comments': n_comments,
                            'max_page': max_page
                            })

    def parse(self, response):
        html = response.text
        html = html[10:-2]
        request_resp = json.loads(html)
        for i, comment_json in enumerate(request_resp.get('result', {}).get('commentList', [])):
            content = comment_json['contents'].replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
            if not content:
                continue
            item = CommentCrawlerItem()
            item['url'] = response.meta['url']
            item['category1'] = response.meta['category1']  
            item['category2'] = response.meta['category2'] 
            item['date'] = response.meta['date']
            item['title'] = response.meta['title']
            item['contents'] = content
            item['antipathy_count'] = comment_json['antipathyCount']
            item['sympathy_count'] = comment_json['sympathyCount']
            item['reg_time'] = comment_json['regTime']
            yield item
                

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)