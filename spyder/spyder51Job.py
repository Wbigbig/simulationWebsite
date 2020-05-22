#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/31 16:38
# Author  : W 
# FileName: spyder51Job.py

import requests
import re
from pyquery import PyQuery as pq

def Spyder51Job(page=True):
    url = "https://search.51job.com/list/080200,000000,0000,01%252C38%252C31%252C32%252C39,9,99,%2B,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "search.51job.com",
        "Referer": "https://search.51job.com/list/080200,000000,0000,01%252C38%252C31%252C32%252C39,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    responselist = []
    for i in range(1,5):
        url = url.replace(re.findall(",\d\.html?",url)[0],",%s.html?" % str(i))
        res = requests.get(url, headers=headers)
        res.encoding = res.apparent_encoding
        response = res.text
        doc = pq(response)
        doc("#resultList").children(".el.title").remove()
        resultlist = doc("#resultList").children(".el").items()
        for item in resultlist:
            temdict = {}
            temdict["jobname"] = item.children("p").text()
            temdict["companyname"] = item.children("span:nth-child(2)").text()
            temdict["workplace"] = item.children("span:nth-child(3)").text()
            temdict["salary"] = item.children("span:nth-child(4)").text()
            temdict["puttime"] = item.children("span:nth-child(5)").text()
            temdict["link"] = item.children("p").children("span a").attr("href")
            responselist.append(temdict)
    return responselist

if __name__ == '__main__':
    Spyder51Job()
