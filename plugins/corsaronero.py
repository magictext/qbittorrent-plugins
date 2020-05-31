# VERSION: 1.9
# AUTHORS: mauricci

from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
import re

class corsaronero(object):
    url = 'http://ilcorsaronero.gratis'
    name = 'Il Corsaro Nero'
    supported_categories = {'all': '0'}
    # maximum number of pages to search in
    max_page = 7

    class MyHTMLParser():
        def __init__(self):
            self.url = 'http://ilcorsaronero.gratis'
            self.fullResData = []
            self.pageResSize = 0
            self.singleResData = self.getSingleData()

        def getSingleData(self):
            return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def feed(self, html):
            self.pageResSize = 0
            url_titles = self.searchTitles(html)
            for c in range(len(url_titles)):
                self.pageResSize = len(url_titles)
                data = self.getSingleData()
                data['desc_link'] = url_titles[c][0]
                data['name'] = url_titles[c][1]
                prettyPrinter(data)
                self.fullResData.append(data)

        def searchTitles(self, html):
            data = []
            divs = re.findall(r'<div class="title">.*?</div>', html)
            for div in divs:
                url_titles = re.search(r'<a href="(.+?)">(.+?)</a>', div)
                if url_titles:
                    data.append([url_titles.group(1), url_titles.group(2)])
            return data

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace(' ', '+')
        currCat = self.supported_categories[cat]
        parser = self.MyHTMLParser()
        # analyze six page of results (thre are 40 entries)
        for currPage in range(1, self.max_page):
            url = self.url + '/page/{1}/?s={0}'.format(what, currPage)
            print(url)
            html = retrieve_url(url)
            parser.feed(html)
            # if there are results go with next page
            if parser.pageResSize <= 0:
                break
        # data = parser.fullResData
        # print(data)

    def download_torrent(self, info):
        """ Downloader """
        html = retrieve_url(info)
        m = re.search('<a.*? href="(.*?magnet.*?)"', html)
        if m and len(m.groups()) > 0:
            magnetLink = m.group(1)
            if magnetLink:
                print(magnetLink + ' ' + info)


if __name__ == "__main__":
    c = corsaronero()
    c.search('l\'alba%20dei%20morti%20dementi')
