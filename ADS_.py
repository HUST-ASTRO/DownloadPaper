# -*- coding: utf-8 -*-
# @Time    : 18-1-28 下午1:55
# @Author  : YuLiu
# @Email   : 335992260@qq.com
# @File    : ADS.py
# @Software: PyCharm

"""
http://adsabs.harvard.edu/abs/~~~
Download paper from this website.
"""

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from ArXiv_ import ArXiv
import requests
import re


class ADS:
    def __init__(self, website):
        self.title = None
        self.authors = None
        self.abstract = None
        self.publication = None
        self.publicationDate = None
        self.keywords = None
        self.DOI = None
        self.pdf = None
        self.arXiv = None
        self.Bibtex = None
        self.ref = None
        self.similar = None
        self.format = None
        self.website = website
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"}

        self.open()

    @staticmethod
    def _check_website(website):
        assert 'http://adsabs.harvard.edu/' in website, "%s is not the ADS website" % website

    def get_information(self, bsObj):
        tdList = bsObj.findAll("td", {"valign": "top", "align": "left"})
        n = len(tdList)
        for i in range(0, n, 2):
            label = tdList[i].get_text()
            content = tdList[i+1].get_text()
            if label == 'Title:':
                self.title = content
            elif label == 'Authors:':
                self.authors = content
            elif label == 'Publication:':
                self.publication = content
            elif label == 'Publication Date:':
                self.publicationDate = content
            elif label == 'Astronomy Keywords:':
                self.keywords = content
            elif label == 'DOI:':
                self.DOI = content
            else:
                pass

        self.abstract = bsObj.findAll("h3", {"align": "center"})[0].next.next
        
        aList = bsObj.findAll("a")
        for a in aList:
            mark = a.get_text()
            try:
                Url = a.attrs['href']
            except KeyError:
                pass
            if mark == 'Full Refereed Journal Article (PDF/Postscript)':
                self.pdf = Url
            elif mark == 'arXiv e-print':
                self.arXiv = Url
            elif mark == 'Bibtex entry for this abstract':
                self.Bibtex = Url
            elif mark == 'Find Similar Abstracts':
                self.similar = Url
            elif mark == 'References in the article':
                self.ref = Url
            elif mark == 'Preferred format for this abstract':
                self.format = Url
            else:
                pass

    def open(self):
        self._check_website(self.website)

        # Looking like a human
        session = requests.Session()
        req = session.get(self.website, headers=self.headers)
        bsObj = BeautifulSoup(req.text, "lxml")
        try:
            bsObj.findAll("h3", {"align": "center"})[0]
        except IndexError:
            print("""No valid record indentifier specified. Please check the website %s.""" % self.website)
        else:
            self.get_information(bsObj)

    def download_pdf(self, path='/home/hust/Desktop/ArticleDownload/'):
        filename = self.authors.split(';')[0].split(',')[0] + self.publicationDate.split('/')[1] + '.pdf'
        savePath = path + filename
        if self.pdf is not None:
            urlretrieve(self.pdf, savePath)
            print("%s download in %s" % (filename, savePath))
        elif self.arXiv is not None:
            paper = ArXiv(self.arXiv)
            paper.download_pdf(path)
        else:
            print("website don't have full refereed journal article.")

    def bibtex(self, file='/home/hust/Desktop/ArticleDownload/bib.tex'):
        session = requests.Session()
        req = session.get(self.Bibtex, headers=self.headers)
        bsObj = BeautifulSoup(req.text, "lxml")
        regular = re.compile(r"@(INPROCEEDINGS|ARTICLE){.*\}", re.S)
        content = re.search(regular, bsObj.body.p.get_text()).group()
        with open(file, 'a') as f:
            f.write('\n')
            f.write(content)


if __name__ == '__main__':
    article = ADS('http://adsabs.harvard.edu/abs/2018MNRAS.475..266Z')
    article.download_pdf()
    article.bibtex()
