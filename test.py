from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import time
import requests

if __name__ == '__main__':
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    list_ = 'http://www.itmtu.net/tag/w%e9%bb%91%e7%b1%b3%e7%b2%a5w.html'
    req = requests.get(url=list_, headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    temp_url = bf.find_all(class_='page-numbers')
    person_url = bf.find(class_='demo2-large')  # Get the person's name
    person_name = person_url.get_text()[5:]
    if person_name not in os.listdir('images'):
        os.makedirs('images/'+person_name)  # make a folder for the person
        # Initialize pages_url by putting list_ as the first page url
    pages_url = [list_]
    for i in temp_url:
        if isinstance(i.get('href'), str):
            pages_url.append('http://www.itmtu.net' + i.get('href'))
    for page in pages_url:
        print(page)
        page_req = requests.get(url=page, headers=headers)
        page_req.encoding = 'utf-8'
        page_html = page_req.text
        page_bf = BeautifulSoup(page_html, 'lxml')
        del temp_url
        temp_url = page_bf.find_all(class_='meta-title')
        sets_url = []
        print(temp_url)
        for temp in temp_url:
            if isinstance(temp.get('href'), str) and isinstance(temp.get_text(), str):
                sets_url.append(temp.get_text() +
                                '=http://www.itmtu.net' + temp.get('href'))
        for set_ in sets_url:
            print(set_)
            set_url = set_.split("=")[1]
            set_name = set_.split("=")[0]
            set_req = requests.get(url=set_url, headers=headers)
            set_req.encoding = 'utf-8'
            set_html = set_req.text
            set_bf = BeautifulSoup(set_html, 'lxml')
            set_finalpage = set_bf.find(title="最后页")
            if set_finalpage != None:
                set_pagenum = set_finalpage.get_text()
            else:
                set_pagenum = 0
            pics_url = []
            for i in range(int(set_pagenum)):
                set_page_url = set_url+str(i+1)
                set_page_req = requests.get(url=set_page_url, headers=headers)
                set_page_req.encoding = 'utf-8'
                set_page_html = set_page_req.text
                set_page_bf = BeautifulSoup(set_page_html, 'lxml')
                pic_url = set_page_bf.find(class_='image_div')
                pics_url.append(pic_url.img.get('alt') +
                                '=' + pic_url.img.get('src'))
            filename = os.getcwd() + '/images/' + person_name + '/' + set_name + '.txt'
            with open(filename, 'w') as f:
                for item in pics_url:
                    f.write("%s\n" % item)
            print('finished downloading: ' + filename)
            