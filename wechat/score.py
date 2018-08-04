# -*- encoding=utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS

def delete_rnt(list):
    for i in range(len(list)):
        list[i] = list[i].strip()
    return list

def get_scores(username, password):
    url = "http://ids.xidian.edu.cn/authserver/login?service=http://yjsxt.xidian.edu.cn/login.jsp"
    headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"en-US,en;q=0.5",
                "Connection":"keep-alive",
                "Content-Length":"151",
                "Content-Type":"application/x-www-form-urlencoded",
                #"Cookie":"route=c5302bceb0583fac097de84b2ac8504c; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en; UM_distinctid=161fb1ceeeb4a2-022f5535d13f3f-7c2d6751-100200-161fb1ceeec51d; JSESSIONID=uGIiTzsgNFUxBh1QrSvfJJgWLvcZc3bCB3Tf_HxDB3cVq3ZRKaKN!-327570731; BIGipServeridsnew.xidian.edu.cn=2541319626.20480.0000",
                #"Host":"ids.xidian.edu.cn",
                "Referer":"http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fyjsxt.xidian.edu.cn%2Flogin.jsp",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
    }


    s = requests.Session()
    r = s.get(url)
    content = r.text
    bs = BS(content, "html.parser")
    lt = bs.find(attrs={"name":"lt"})['value']
    exe = bs.find(attrs={"name":"execution"})['value']
    data = {
            "_eventId":"submit",
            "execution":exe,
            "lt":lt,
            "password":password,
            "rmShown":"1",
            "submit":"",
            "username":username
    }
    res = s.post(url, data=data,  headers=headers)
    res = s.get('http://yjsxt.xidian.edu.cn/queryScoreByStuAction.do')
    datas = BS(res.text, 'html.parser')
    tabs = datas.find_all("table", attrs={"class": "list_caption"})

    names = []
    scores = []

    for index, tab in enumerate(tabs):
        trs = tab.find_all('tr')
        for idx, tr in enumerate(trs):
            tds = tr.find_all('td') 
            if idx != 0:
                names.append(tds[2].text)
                scores.append(tds[5].text)

    names = delete_rnt(names)
    scores = delete_rnt(scores)
    
    return names,scores
