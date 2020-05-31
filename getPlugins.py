import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
import threading
import random
import time
baseurl = "https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins"


def download(href : str):
    try:
        print(href)
        pluginsdir = os.getcwd()+os.sep+"plugins"
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)
        filename = href.split("/")[-1]
        if filename == "qBittorrent-plugins":
            return
        r = requests.get(href)
        r.raise_for_status()
        with open(pluginsdir+os.sep+filename,'wb') as f:
            f.write(r.content)
            print("success")
    except Exception as identifier:
        print(href+"  fail")
    

if __name__ == "__main__":
    # try:
        r = requests.get(baseurl)
        if r.status_code == 200 :
            r.encoding = r.apparent_encoding
            html = r.text
            soup = BeautifulSoup(html,"html.parser")
            trs = soup.table.find_all("tr")
            pool = ThreadPoolExecutor(10)
            for tr in range(1,len(trs)):
                a = trs[tr].find_all("a")[2]
                href : str= a.get("href")
                download(href)
                # pool.submit(download,href)
                # threading.Thread(target=download,args=[href,]).start()
                
            # pool.shutdown()
    # except Exception as e:
    #     print()
    #     pass
    # pass
