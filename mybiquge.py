#biquge.py

import requests
from bs4 import BeautifulSoup
import re

def get_soup(url):

    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status
        r.encoding='utf-8'
        html=r.text
        return BeautifulSoup(html,'html.parser')
    except:
        return ""

def get_novel_url(soup):
    '''
    从get_html里获取小说排名，名称和链接地址
    '''
    url_list=[]
    category_list=soup.find_all('div',class_="index_toplist mright mbottom")
    history_finished_list=soup.find_all('div',class_="index_toplist  mbottom")
    for cate in category_list:
        name=cate.find('div',class_="toptab").span.string
        with open('novel_list.csv','a+') as f:
            f.write("\n小说种类:{}\n".format(name))
        general_list=cate.find(style='display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link='https://www.qu.la'+book.a['href']
            title=book.a['title']
            url_list.append(link)
            with open('novel_list.csv','a') as f:
                f.write("小说名:{:<} \t 小说地址:{:<} \n".format(title,link))
    for cate in history_finished_list:
        name=cate.find('div',class_="toptab").span.string
        with open('novel_list.csv','a') as f:
            f.write("\n小说种类:{}\n".format(name))
        general_list=cate.find(style='display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link='https://www.qu.la'+book.a['href']
            title=book.a['title']
            url_list.append(link)
            with open('novel_list.csv','a') as f:
                f.write("小说名:{:<} \t 小说地址:{:<} \n".format(title,link))
    return url_list
def get_chapter_url(soup):
    url_list=[]
    lisa=soup.find_all('dd')
    h1=soup.find('h1')
    txt_name=h1.text
    with open('D:/python/code/crawl/biquge小说/{}.txt'.format(txt_name),'a+',encoding='utf-8') as f:
        f.write('小说标题:{}\n'.format(txt_name))
    for u in lisa:
        c_url=u.a['href']
        if re.match(r'/.*html',c_url):
            url_list.append('https://www.qu.la'+c_url)
        else:
            continue
    return url_list,txt_name
def get_one_txt(soup,txt_name):
    
    #从get_chapter_url中的地址里获取每个小说每个章节的文本,并存到上述函数中产生的对应文件中
    
    try:
        txt=soup.find('div',id='content').text.replace('chaptererror();','')
        title=soup.find('title').text
        with open('D:/python/code/crawl/biquge小说/{}.txt'.format(txt_name),'a',encoding='utf-8') as f:
            f.write(title+'\n\n')
            f.write(txt)
            print('当前小说:{} 当前章节:{}已下载完毕'.format(txt_name,title))
    except:
        print("something wrong")
            
def main():
    basic_url='https://www.qu.la/paihangbang/'
    basic_soup=get_soup(basic_url)
    novel_url_list=get_novel_url(basic_soup)
    novel_url_list=list(set(novel_url_list))
    for novel_url in novel_url_list:
        novel_soup=get_soup(novel_url)
        chapter_url_list,novel_name=get_chapter_url(novel_soup)
        for chapter_url in chapter_url_list[:1]:
            chapter_soup=get_soup(chapter_url)
            get_one_txt(chapter_soup,novel_name)
            print('当前进度{}% '.format(novel_url_list.index(novel_url)/len(novel_url_list)*100))
main()