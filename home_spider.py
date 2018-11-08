#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Howe.  All rights reserved.
This program is free software;
you can redistribute it and/or modify it
spdier for images from website
"""
import urllib2
import re
import os
import scrapy

class HomeSpider():
    def getLink(self, url):
        headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
        opener = urllib2.build_opener()
        opener.addheaders = [headers]
        urllib2.install_opener(opener)
        file = urllib2.urlopen(url).read()
        file = file.decode('utf-8')
        pattern = '(https?://[^\s)";]+(\.(\w|/)*))'
        link = re.compile(pattern).findall(file)
        #去重
        link = list(set(link))
        return link

    def parse(self, response):
        houses = response.xpath(".//ul[@class='sellListContent']/li")
        for house in houses:
            attention = ''
            visited = ''
            publishday = ''
            try:
                attention = house.xpath(".//div[@class='followInfo']/text()").re("\d+")[0]
                visited = house.xpath(".//div[@class='followInfo']/text()").re("\d+")[1]
                # 因为发布日期中可能单位不是天，所以我做了简单的转化。
                if u'月' in house.xpath(".//div[@class='followInfo']/text()").extract()[0].split('/')[2]:
                    number = house.xpath(".//div[@class='followInfo']/text()").re("\d+")[2]
                    publishday = '' + int(number) * 30

                elif u'年' in house.xpath(".//div[@class='followInfo']/text()").extract()[0].split('/')[2]:
                    number = house.xpath(".//div[@class='followInfo']/text()").re("\d+")[2]
                    publishday = '365'
                else:
                    publishday = house.xpath(".//div[@class='followInfo']/text()").re("\d+")[2]
            except:
                print "These are some ecxeptions"
            else:
                pass
            yield {
                'region': house.xpath(".//div[@class='houseInfo']/a/text()").extract(),
                'url': house.xpath(".//a[@class='img ']/@href").extract(),
                'houseInfo': house.xpath(".//div[@class='houseInfo']/text()").extract(),
                'unitPrice': house.xpath(".//div[@class='unitPrice']/span").re("\d+.\d+"),
                'totalPrice': house.xpath(".//div[@class='totalPrice']/span").re("\d+.\d+"),
                'attention': attention,
                'visited': visited,
                'publishday': publishday
            }
        page = response.xpath("//div[@class='page-box house-lst-page-box'][@page-data]").re("\d+")
        p = re.compile(r'[^\d]+')
        # 这里是判断有没有下一页，毕竟不是所有区都是有第100页的，不能for循环到100
        if len(page) > 1 and page[0] != page[1]:
            next_page = p.match(response.url).group() + str(int(page[1]) + 1)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

if __name__ == "__main__":
    url_input = "https://bj.lianjia.com"
    print u"解析网址..."
    my_home = HomeSpider()
    url_link_list = my_home.getLink(url_input)
    print u"获取网址list: %d"%len(url_link_list)
    for url_link in url_link_list:
        print url_link
        # downLoadInfo(url_link)
