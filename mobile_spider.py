# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urlparse import urljoin
class MobileSpiderSpider(scrapy.Spider):
    name = 'mobile_spider'
    allowed_domains = ['flipkart.com']
    start_urls = ['https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=clp_metro_expandable_1_4.metroExpandable.METRO_EXPANDABLE_realme_mobile-phones-store_25DMXHG2C5AT_wp3&fm=neo%2Fmerchandising&iid=M_26111f68-fa56-4e5a-ac19-6406a8fcad57_4.25DMXHG2C5AT&ppt=clp&ppn=mobile-phones-store&ssid=1bmc88y93k0000001578059513819&page=1']

    def parse(self, response):
        mobile_url=response.xpath('//*[@class="_31qSD5"]/@href').extract()
        for url in mobile_url:
            absolute_url=urljoin("https://www.flipkart.com/",url)
            yield Request(absolute_url,callback=self.mobile_data,dont_filter=True)
        lt=response.xpath("//*[@class='_3fVaIS']/@href").extract()
        if(len(lt)==2):
            absolute_url=urljoin("https://www.flipkart.com/",lt[1])
            yield Request(absolute_url,callback=self.parse,dont_filter=True)
        else:
            lt1=response.xpath("//*[@class='_3fVaIS']/span/text()").extract()
            if(lt1[0]=='Next'):
                absolute_url=urljoin("https://www.flipkart.com/",lt[0])
                yield Request(absolute_url,callback=self.parse,dont_filter=True)
                
    def mobile_data(self,response):
        lt=response.xpath("//*[@class='_35KyD6']/text()").extract()
        if(len(lt)>1):
            for i in lt[1:]:
                lt[0]=lt[0]+i
        s=response.xpath("//*[@class='_1vC4OE _3qQ9m1']/text()").extract()[0]
        return {"product_name":lt[0],"product_price":s} 
