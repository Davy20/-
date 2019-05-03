# gupiao.py
'''
增加
if stockinfo == None:
                print(url)
如果输出为空，给出url，相应的股票代码可能有问题。

知识点：traceback.print_exc()
知识点：默认参数code='utf-8'提高代码效率
知识点：\r,end=''，end中间是空或者空格好像都行
知识点：文件路径用斜杠或者反斜杠好像都行

'''
import requests
from bs4 import BeautifulSoup
import traceback
import re

def get_html(url,code='utf-8'):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
        
def get_list(lst,s_url):
    html = get_html(s_url,'gb2312')
    soup = BeautifulSoup(html,'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            if re.findall(r"[s][hz][360]\d{5}",href)!='':
                lst.append(re.findall(r"[s][hz][360]\d{5}",href)[0])
        except:
            continue
def get_content(lst,baidu_url,fpath):
    count=0
    for stock in lst:
        url = baidu_url + stock + ".html"
        html = get_html(url)
        try:
            if html == '':
                continue
            infodict = {}
            soup = BeautifulSoup(html,'html.parser')
            stockinfo = soup.find('div',attrs={'class':'stock-bets'})
            if stockinfo == None:
                print(url)
            name = stockinfo.find_all('a',attrs={'class':'bets-name'})[0]
            infodict.update({'股票名称':name.text.split()[0]})
            keylist=stockinfo.find_all('dt')
            valuelist = stockinfo.find_all('dd')
            for i in range(len(keylist)):
                key = keylist[i].text
                val = valuelist[i].text
                infodict[key] = val
            with open(fpath,'a',encoding='utf-8') as f:
                f.write(str(infodict) + '\n')
                count = count+1
                print('\r当前进度：{:.2f}%'.format(count/len(lst)*100),end='')
        except:
            count = count+1
            print('\r当前进度：{:.2f}%'.format(count/len(lst)*100),end='')
            traceback.print_exc()
            continue
def main():
    start_url='http://quote.eastmoney.com/stock_list.html'
    stock_url = 'https://gupiao.baidu.com/stock/'
    out_file = 'D:/python/code/crawl/gupiao.txt'
    slist = []
    get_list(slist,start_url)
    get_content(slist,stock_url,out_file)
    
main()