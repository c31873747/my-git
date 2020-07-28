# import urllib.request as req
# url = "https://www.ptt.cc/bbs/movie/index.html"

# request = req.Request(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"})

# with req.urlopen(request) as response:
#     data = response.read().decode("utf-8")

# import bs4
# soup = bs4.BeautifulSoup(data, "html.parser")
# # print(soup.title)
# titles = soup.find_all("div", class_ = "title")
# for title in titles:
#     if title.a != None:
#         print(title.a.string)

##安裝python3 的 request後的版本
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pprint

my_headers = {'cookie':'over18=1',
              'user agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
index = str(input("輸入想要爬的網址吧!!!"))
pages = eval(input("想爬幾頁呢???"))
not_exist = BeautifulSoup('<a>(本文已被刪除)</a>', 'lxml'). a
titles = []
dates = []
nextLink = ""

#爬一頁的method(for 頁數)
def getPttVersionPage(url):
    response = requests.get(url, headers = my_headers) #get網址的內容
    data = BeautifulSoup(response.text, 'html.parser')
    
    for i in data.find_all('div', class_ = 'r-ent'): #找出每個class是r-ent形式的div開頭,用for迴圈一個一個處理
        title = i.find('div', 'title', 'a') or not_exist #找出有title, a 的內容
        titles.append(title.a.string)

    link = "https://www.ptt.cc" + str(data.find('div', 'btn-group-paging').find_all('a', 'btn wide')[1].get('href')) #找到上一頁的網址
    nextLink = link

    return nextLink

for i in range(pages):
    index = getPttVersionPage(index)

with open("pttGossipTitle.txt", mode = 'w', encoding = 'utf-8') as file:
    for i in range(len(titles)):
        file.write(titles[i] + "\n")

#爬一天的method
def getPttVersionDate(url, todayDate):
    response = requests.get(url, headers = my_headers)
    data = BeautifulSoup(response.text, 'lxml')

    for i in data.find_all('div', class_ = 'r-ent'):
        date = i.find('div', class_ = 'date')
        if date.string.strip() == todayDate:
            dates.append(date.string)
            if i.a != None:
                titles.append(i.a.string)
        else:
            break
    
    link = "https://www.ptt.cc" + str(data.find('div', 'btn-group-paging').find_all('a', 'btn wide')[1].get('href'))
    nextLink = link
    
    return nextLink

#取得今天的日期
from datetime import datetime

tmp = datetime.now().strftime('%m/%d')
if tmp[0] == '0':
    date = tmp[1::]
else:
    date = tmp

#八卦版100頁
for i in range(100):
    index = getPttVersionDate(index, date)

with open("pttGossipTitle.txt", mode = 'w', encoding = 'utf-8') as file:
    for j in range(len(dates)):
        content = str(j + 1) + dates[j] + titles[j] + '\n'
        file.write(content)