from bs4 import BeautifulSoup
from urllib import request
import re
import os
import datetime
import json

msg = []

def out(data1, key1, now_time):
    out_data = sorted(data1, key = lambda i: i[key1])
    name = "output_" + now_time + ".json"
    fd = os.open(name, os.O_RDWR|os.O_CREAT)
    fo = os.fdopen(fd, "w+")
    out_end = {}
    out_end["name"] = "武大要闻"
    out_end["order"] = key1
    out_end["generated_at"] = now_time
    out_end["data"] = out_data
    json_out = json.dumps(out_end, indent=4, sort_keys=True, ensure_ascii=False)
    fo.write(json_out)
    
    

def get_pages(url, mx):

    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')

    response1 = request.urlopen(req)
    data = response1.read()

    soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
    links = soup.find_all('a', {"class" : "gray"})
    clicks = soup.find_all('div', {"class" : "clicknum"})

    all_num = len(links)
    cnt = 0
    for linktmp in links:
        new_msg = {}

        new_msg['title'] = linktmp.get_text()

        url2 = "https://news.whu.edu.cn/" + linktmp['href']
        new_msg['link'] = url2

        req2 = request.Request(url2)
        req2.add_header('User-Agent', 'Mozilla/5.0')
        response2 = request.urlopen(req2)
        data2 = response2.read()
        soup2 = BeautifulSoup(data2, 'html.parser', from_encoding='utf-8')
        message = soup2.find('div', {"class" : "news_attrib"})
        
        tmp = message.get_text()
        tmp_B = tmp.replace(" ", "T")
        new_msg['time'] = tmp_B[11:27]

        tmp_A = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", tmp)
        new_msg['source'] = tmp_A[25:-7]
        msg.append(new_msg)

        cnt = cnt + 1
        if cnt == mx:
            break




url1 = "https://news.whu.edu.cn/wdyw.htm"
nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
nowTime = nowTime.replace(" ", "T")

nms = input("请输入需要提取的抓取的新闻总数（1～30））\n")
#时间来不及了就没有做多个页面的 我反省）
val = input("请输入排序关键字：time \ source \ title\n")

get_pages(url1, int(nms))
out(msg, val, nowTime)

print("抓取完毕！")