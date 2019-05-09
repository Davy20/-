#dianying2345.py


import requests
from bs4 import BeautifulSoup
import re

def get_html(url,code='gbk'):
    r=requests.get(url,timeout=30)
    r.raise_for_status()
    r.encoding=code
    return r.text
    
def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    movies_list = soup.find('ul',class_='picList clearfix')
    movies = movies_list.find_all('li')
    for movie in movies:
        img_url = 'http:'+re.findall(r'.*\.jpg',movie.find('img')['src'])[0]
        name = movie.find('span',class_='sTit').a.text
        actors = movie.find('p',class_='pActor').contents
        actor = ''
        for a in actors:
            actor = actor + a.string + '  '
        num_html = movie.find('i',class_='iNum iLightNum')
        if num_html!=None:
            num = num_html.text
        else:
            num = movie.find('i',class_='iNum ').text
        print('排名：{}\t片名：{}\n\n{}\n\n'.format(num,name,actor))
        with open('D:/python/code/crawl/dianying2345/'+name+'.jpg','wb') as f:
            f.write(requests.get(img_url).content)
def main():
    start_url='http://dianying.2345.com/top/'
    get_content(start_url)
main()