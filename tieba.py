#tieba.py
import requests
from bs4 import BeautifulSoup
def gethtml(url):
    r=requests.get(url,timeout=30)
    r.raise_for_status()
    r.encoding='utf-8'
    return r.text
    
def getcontent(html,comments):
    soup=BeautifulSoup(html,'html.parser')
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    for li in liTags:
        comment={}
        comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
        comment['link'] = "http://tieba.baidu.com/"+li.find(
                'a', attrs={'class': 'j_th_tit '})['href']
        comment['name'] = li.find(
                'span', attrs={'class': "tb_icon_author "}).text.strip()
        comment['time'] = li.find(
                'span', attrs={'class': "pull-right is_show_create_time"}).text.strip()
        comment['replyNum'] = li.find(
                'span', attrs={'class': "threadlist_rep_num center_text"}).text.strip()
        comments.append(comment)
    return comments
def out2file(dict):
    with open('tiebajinghuaqi.txt','a+',encoding="utf-8") as f:
        for comment in dict:
            f.write('标题:{} \t 链接:{} \t 发帖人:{} \t 发帖时间:{} \t 回复数量:{}\n'.format(comment['title'],comment['link'],comment['name'],comment['time'],comment['replyNum']))
        print('当前页面爬取完成')
def main(goods):
    base_url='http://tieba.baidu.com/f?kw='+goods
    url_list=[]
    for i in range(0,2):
        url_list.append(base_url+'&pn='+str(i*50))
    print('所有网页已下载到本地,开始筛选信息')
    for url in url_list:
        gethtml(url)
        html=gethtml(url)
        comments=[]
        getcontent(html,comments)
        dict=getcontent(html,comments)
        out2file(dict)
goods='净化器'
main(goods)