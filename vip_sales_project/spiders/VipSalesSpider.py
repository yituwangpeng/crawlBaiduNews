# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from vip_sales_project.items import VipSalesProjectItem
#导入re模块
import re
import time

class MySpider(scrapy.Spider):
    name = 'VipSalesSpider'
    allowed_domains = ['baidu.com']
    start_urls = [
        'http://news.baidu.com/ns?word=%E5%94%AF%E5%93%81%E4%BC%9A'
    ]

    def parse(self, response):
        # self.log('A response from %s just arrived!' % response.url)
        #
        self.log('A response from %s just arrived!' % response.body)

        bodystr = response.xpath('//body')[0].xpath('string(.)').extract_first()

        print "bodystr = %s" % (bodystr)
        print "len bodystr = %d" % (len(bodystr))
        print "len bodystr = %d" % (len(u''))
        #请求数据为空时 重新请求retry
        if len(bodystr)==0:
            print 'response.body is Noneresponse.body is Noneresponse.body is Noneresponse.body is None'

            time.sleep(1)

            r = scrapy.Request(response.url, callback=self.parse, dont_filter=True)
            yield r
            return

        #解析节点信息
        for sel in response.xpath('//div[@class="result"]'):
            print "find the key word!"

            item = VipSalesProjectItem()

            titles = sel.xpath('h3[@class="c-title"]/a')
            item['title'] = titles[0].xpath('string(.)').extract()
            item['url'] = sel.xpath('h3[@class="c-title"]/a/@href').extract()
            dess = sel.xpath('div')
            item['des'] = dess[0].xpath('string(.)').extract()

            sites = sel.xpath('div/p[@class="c-author"]/text()').extract()
            if len(sites) > 0:
                print 11
            else:
                sites = sel.xpath('div/div[last()]/p[@class="c-author"]/text()').extract()

            strlist = sites[0].split() #采用不带参数的split()，它会把所有空格（空格符、制表符、换行符）当作分隔符
            #i = 0
            # timestr = ""
            # for value in strlist:  # 循环输出列表值
            #     if i==0:
            #         item['site'] = value
            #     else:
            #         timestr += value
            #
            #     i=i+1

            item['site'] = strlist[0]

            strlistLen = len(strlist)
            if strlistLen==2:
                item['time'] = time.strftime('%Y年%m月%d日',time.localtime(time.time()))
            elif strlistLen==3:
                item['time'] = strlist[1]

            yield item

        #下一页 递归
        next_url = response.xpath('//p[@id="page"]/a[last()]/@href').extract_first()
        next_str = response.xpath('//p[@id="page"]/a[last()]/text()').extract_first()

        print "next_url = %s %s" % (next_url,next_str)

        pos = next_str.find(u'下一页')
        if pos!=-1 and len(next_url) > 0:
           new_url = "http://news.baidu.com" + next_url

           print "[parse]new_url = %s" % (new_url)
           # 创建对应的页面的Request对象，设定回调函数为parse，利用parse处理返回的页面
           r = scrapy.Request(new_url, callback=self.parse, dont_filter=True)
           yield r


