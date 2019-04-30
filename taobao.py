#taobao.py
import requests
import re
from bs4 import BeautifulSoup

def gethtmltext(url):
    kv={'authority':'s.taobao.com',
    'method':'GET',
    'path':'/search?q=%E5%87%80%E5%8C%96%E5%99%A8',
    'scheme':'https',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cache-control':'max-age=0',
    'cookie':'cna=hcPAE6rRl08CAdIMOD1bWLkG; tracknick=ygjbuaa; tg=0; enc=d%2FoXDLBr3%2B8icLLZjSrkQe69EiO393EmCCc6I3Q6W9S8slfgJ%2FmsDWb0fq%2BGC1yOmJwlwgcXdnuB4odUivlYfw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; _cc_=U%2BGCWk%2F7og%3D%3D; miid=1035998601356806373; t=d20a37db86a4845b9523face981da4a6; cookie2=3a43f6b8eb28b8e6be185dee22e5b20e; v=0; _tb_token_=3097e5e6ed775; JSESSIONID=29E91E8D3E336429689116DE5B2280D6; l=bB_YzmcVvxRijOGEBOCN5uIRZd7OSIRYouPRw4Avi_5BZ6L_kwbOlw4RdFp6Vj5Rs0LB402lRpJ9-etki; isg=BJubr7ofQ51SpLiYowqaRpRwKv_F2GcD8_Tpm43YdxqxbLtOFUA_wrnuAozHygdq',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'}

    try:
        r=requests.get(url,headers=kv,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""
def parsePage(ilt,html):
    try:
        plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt=re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            ilt.append([price,title])
    except:
        print("")
def printgoodslist(ilt):
    tplt="{:4}\t{:8}\t{:16}"
    print(tplt.format("序号","价格","品名"))
    count=0
    for g in ilt:
        count=count+1
        print(tplt.format(count,g[0],g[1]))
def main():
    goods='净化器'
    depth=2
    start_url='https://s.taobao.com/search?q='+goods
    infolist=[]
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=gethtmltext(url)
            parsePage(infolist,html)
        except:
            continue
    printgoodslist(infolist)
main()