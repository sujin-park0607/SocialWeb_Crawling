from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

sitename = "부산한마음스포츠센터"
name_dic={"구분":[]}
##program 페이지 찾기
html = requests.get("http://hmsports.bisco.or.kr/").text
htmlAll = bs(html,'html.parser')
program_page = htmlAll.find_all("li",{"class":"mn_li1"})[1].find("a")["href"]

##컬럼 지정
my_columns = ["프로그램","반","대상","교육일","시간","정원","교육비","비고"]
dic = {}
for col in my_columns:
    dic[col]=list()

## 각 프로그램의 url 찾기
html = requests.get("http://hmsports.bisco.or.kr/"+program_page).text
htmlAll = bs(html,'html.parser')
pages = htmlAll.find_all("ul",{"class":"depth2"})[-1].find_all("a")
programURLs = [url["href"] for url in pages]
del programURLs[-1]## 통합방과후학교 삭제
del programURLs[4]## 실내골프연습장 삭제
del programURLs[2]## 피트니스실 삭제

for url in programURLs:
    html = requests.get("http://hmsports.bisco.or.kr"+url).text
    htmlAll = bs(html,'html.parser')
    initial_df = pd.read_html(html,header=0)[0]  #표 df로 변환
    current_col = initial_df.columns.tolist()
    for col in current_col:
        for value in initial_df[col]:
            dic[col].append(value)
    for _ in range(len(initial_df[current_col[0]].values)):
        name_dic["구분"].append(htmlAll.find("div",{"id":"print"}).find('h4',{'class':'ctit'}).text)
dic.update(name_dic)

sort_columns = list(my_columns)
sort_columns.insert(0,"구분")
result_df = pd.DataFrame(dic)
result_df = result_df[sort_columns]
result_df = result_df.dropna(axis=0)# 결측값 행 제거

result_df.to_csv('./{}.csv'.format(sitename), sep=',', na_rep='NaN',encoding="CP949", index=False)