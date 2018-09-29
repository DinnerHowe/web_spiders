#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Howe.  All rights reserved.
This program is free software;
you can redistribute it and/or modify it
spdier for images from website
"""
import urllib
import re
import os
def getHTML(url):
    print u"获取网址: %s..."%url
    page = urllib.urlopen(url)
    html_code = page.read()
    return html_code

def defineRegularFormuler(html, reg):
    reg_ = re.compile(reg)
    reg_list = reg_.findall(html)
    return reg_list

def downLoadImge(webside):
    html_code = getHTML(webside)
    reg_jpg = r'src="(.+?\.jpg)"'
    print u"网页图片抓取..."
    img_list_jpg = defineRegularFormuler(html_code, reg_jpg)
    reg_png  = r'src="(.+?\.png)"'
    img_list_png = defineRegularFormuler(html_code, reg_png)
    img_list = []
    img_list.extend(img_list_jpg)
    img_list.extend(img_list_png)
    path = os.getcwd() + "/imgs/"
    if not os.path.exists(path):
        os.makedirs(path, mode=0o777)
    page_file = open(path + 'image_list.txt', 'w')
    x = 1
    print u"下载图片，从%s..."%webside
    page_file.writelines("IMAGES LIST: \n")
    for i in img_list:
        if "</" not in i:
            print i
            name_str  = i.split("sign=")
            name = name_str[-1].split(".jpg")[0].split("/")[-1]
            urllib.urlretrieve(i, path+'%s.jpg'%name)
            page_file.writelines("%d: "%x + i)
            page_file.writelines("\n")
            x += 1
    page_file.close()
    print u"完成..."

if __name__ == "__main__":
    # url_input = raw_input("请输入网址连接：")
    # if url_input.split("://")[0] != "https" and url_input.split(":")[0] != "www":
    #     print url_input.split("://")[0]
    #     print u"网页输入错误，未检测到http://???"
    #     url_input = raw_input("请再次输入网址连接：")
    # print u"解析网址..."
    # reg = r'https.\.html'
    # url_link_list = defineRegularFormuler(url_input, reg)
    # print u"获取网址list: "
    # print url_link_list
    # for url_link in url_link_list:
    #     downLoadImge(url_link)
    downLoadImge("https://www.cnblogs.com/Axi8/p/5757270.html")