# -*- coding: utf-8 -*-
# @Time    : 18-1-29 上午11:15
# @Author  : YuLiu
# @Email   : 335992260@qq.com
# @File    : ArXiv.py
# @Software: PyCharm

"""
https://arxiv.org/abs/~~~
Download paper from this website.
"""

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests


class ArXiv:
    def __init__(self, website):
        self.title = None
        self.author = None
        self.abstract = None
        self.publicationDate = None
        self.publication = None
        self.pdf = None
        self.postscript = None
        self.OtherFormats = None
        self.website = website
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"}

        self.open()

    @staticmethod
    def _check_website(website):
        assert 'https://arxiv.org/abs/' or 'http://adsabs.harvard.edu/' in website, "%s is not the ArXiv website" % website

    def get_information(self, bsObj):
        self.title = bsObj.findAll("h1", {"class": "title mathjax"})[0]
        self.author = bsObj.find("div", {"class": "authors"}).a.get_text()
        self.abstract = bsObj.find("blockquote", {"class": "abstract mathjax"}).get_text()
        self.publicationDate = bsObj.find("div", {"class": "dateline"}).get_text()
        self.publication = bsObj.find("td", {"class": "tablecell comments"}).get_text()

        aList = bsObj.find("div", {"class": "full-text"}).ul.findAll("a")
        for a in aList:
            label = a.get_text()
            Url = a.attrs['href']
            if label == 'PDF':
                self.pdf = "https://arxiv.org" + Url
            elif label == 'PostScript':
                self.postscript = "https://arxiv.org" + Url
            elif label == 'Other formats':
                self.OtherFormats = "https://arxiv.org" + Url
            else:
                pass

    def open(self):
        self._check_website(self.website)

        # Looking like a human
        session = requests.Session()
        req = session.get(self.website, headers=self.headers)
        bsObj = BeautifulSoup(req.text, "lxml")
        try:
            bsObj.findAll("h1", {"class": "title mathjax"})[0]
        except IndexError:
            print("""No valid record indentifier specified. Please check the website %s.""" % self.website)
        else:
            self.get_information(bsObj)

    def download_pdf(self, path='/home/hust/Desktop/ArticleDownload/'):
        filename = self.author + '(' + self.publicationDate.split(' ')[-1] + '.pdf'
        savePath = path + filename
        if self.pdf is not None:
            urlretrieve(self.pdf, savePath)
            print("%s download in %s" % (filename, savePath))
        else:
            print("website don't have full refereed journal article. Please check the website %s." % self.website)


if __name__ == '__main__':
    article = ArXiv('https://arxiv.org/abs/1801.08540')
    article.download_pdf()
