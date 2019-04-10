# -*- coding: utf-8 -*-
import scrapy
from epub.items import EpubItem

class EpubdownloadSpider(scrapy.Spider):
    name = 'epubdownload'
    # allowed_domains = ['https://www.ixdzs.com/sort/1/index_0_2_0_1.html']
    start_urls = ['http://www.ixdzs.com/sort/1/index_0_2_0_'+str(i)+'.html/' for i in range(1,51)]

    def parse(self, response):
        href=response.xpath('//a[contains(@href,"/d") and contains(@href,"epub_down")]/@href').extract()
        for i in range(len(href)):
            url = 'http://www.ixdzs.com/'+href[i]
            yield scrapy.Request(url=url,callback=self.newparse)

    def newparse(self,response):
        item=EpubItem()
        link = response.xpath('//a[contains(@href,"down?id=") and contains(@href,"p=6")]/@href').extract()
        url='http://www.ixdzs.com/'+link[0]
        x=url.split('=')
        list=x[0:len(x)-1]
        newurl='='.join(list)+'='
        nam=response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        item['name']=nam[:len(nam)-5]
        item['down_url']=newurl
        yield item