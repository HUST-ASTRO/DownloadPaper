# -*- coding:utf-8 -*-
# @Author  : Yu Liu
# @Email   : yuliumutian@gmail.com
# @Software: PyCharm


from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from ADS_ import ADS
import requests
import re


class ADSSearch:
    def __init__(self, author, year):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"}
        self.url = "http://adsabs.harvard.edu/abstract_service.html"
        assert isinstance(author, str)
        assert isinstance(year, str)
        self.author = author
        self.year = year
        self.params = {
                      'author': self.author,
                      'start_mon': '00',
                      'start_year': self.year,
                      'end_mon': '12',
                      'end_year': self.year
                     }

        r = requests.post(self.url, headers=self.headers, data=self.params)
        self.bsObj = BeautifulSoup(r.text, "lxml")


    def search(self, regular=None):
        targetList = self.bsObj.findAll("td", {"valign": "baseline", "align": "left", "width": "5%"})
        for target in targetList:
            Url = target.a.attrs['href']
            article = ADS(Url)
            print(article.title)
            print(article.abstract)
            # re.search(regular, article.title)


if __name__ == '__main__':
    author = '^Gosachinskiĭ'
    year = '1985'
    article = ADSSearch(author, year)
    article.search()