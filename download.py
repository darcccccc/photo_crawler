from urllib.request import urlretrieve
import os
import time
import requests

def download_img(url,filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    req = requests.get(url, headers=headers, stream=True)
    if req.status_code == 200:
        with open(name_dir,'wb') as file:
            file.write(req.content)
        print(name+' downloaded')
        time.sleep(5)
    del req
if __name__ == '__main__':
    person_list = os.listdir('images')
    for person in person_list:
        person_dir = 'images/'+person 
        filelist = os.listdir(person_dir)
        set_list = [x for x in filelist if 'txt' in x] 
        for set_ in set_list:
            filename = set_.split('[')[0].strip()
            set_dir = person_dir+'/'+set_
            filename_dir = person_dir+'/'+filename
            if filename not in os.listdir(person_dir):
                os.mkdir(filename_dir) # make a folder for set_
            with open(set_dir,'r') as file:
                is_running = True
                while is_running:
                    info = file.readline().split('=')
                    if len(info) > 1:
                        name = info[0]
                        url = info[1]
                        name_dir = filename_dir+'/'+name+'.jpg'
                        download_img(url=url,filename=name_dir)
                    else:
                        is_running = False
                
