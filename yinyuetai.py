#yinyuetai.py

import requests
from bs4 import BeautifulSoup
import time

def get_html(url,code='utf-8'):
    '''kv = {
    'Referer':'http://vchart.yinyuetai.com/vchart/trends?area=ML',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'}'''
    
    r = requests.get(url,timeout=30)
    r.raise_for_status()
    r.encoding = code
    return r.text
    
def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    music_list = soup.find_all('li',class_='vitem J_li_toggle_date ')
    for m in music_list:
        top_num = m.find('div',class_="top_num").text
        if m.find('h3',class_="asc_score"):
            score = m.find('h3',class_="asc_score").text
        else:
            score = m.find('h3',class_="desc_score").text
        mvname = m.find('a',class_="mvname").text
        singer = m.find('a',class_="special").text
        t = m.find('p',class_="c9").text
        print('排名:{}\t分数:{}\t歌名:{}\t歌手:{}\t发布时间:{}\n'.format(top_num,score,mvname,singer,t))
        
def main():
    start_url = 'http://vchart.yinyuetai.com/vchart/trends?area='
    url_list = ['ML','HT','US','JP','KR']
    for area in url_list:
        url = start_url+area
        print (area)
        get_html(url)
        get_content(url)
    
main()