#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from fjsen.items import FjsenItem
add = 0
class FjsenSpider(BaseSpider):
    name="fjsen"
    allowed_domains=["fjsen.com"]
    start_urls=['http://www.fjsen.com/j/node_94962_'+str(x)+'.htm' for x in range(2,11)]+['http://www.fjsen.com/j/node_94962.htm']
    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//ul/li')
        items=[]
        global add
        for site in sites:
            item=FjsenItem()
            add+=1
            item['id']=add
            item['title']=site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            item['addtime']=site.select('span/text()').extract()
            items.append(item)
        return items       
