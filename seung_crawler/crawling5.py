from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

sitename = "서부산권장애인스포츠센터"
## 페이지 url 확인
html = requests.get("https://www.sbsd.kr/Home").text
htmlAll = bs(html,'html.parser')
programpage = htmlAll.find("li",{"class":"cd1 cd1c4"}).find("a")["href"].split("/")[-1]

## '프로그램' 페이지 접근
html = html = requests.get("https://www.sbsd.kr/Home/"+programpage).text
htmlAll = bs(html,'html.parser')
pages = htmlAll.find('nav',{"class":"tabmenu con_tab four no_pdt"}).find_all("li",{"class":"cd3"})

##프로그램 페이지url 저장
programURLs = []
for elem in pages:
    programURLs.append(elem.find("a")["href"].split("/")[-1])   ## 페이지 넘버
name_dic={"구분":[]}

## 컬럼 지정
my_columns = ["프로그램", "시간", "대상", "요일", "사용료", "정원"]
## dic 초기화
dic={}
for col in my_columns:
    dic[col]=list()

##데이터 가져오기
for i in range(len(programURLs)):
    html = requests.get("https://www.sbsd.kr/Home/"+programURLs[i]).text
    htmlAll = bs(html,'html.parser')
    # 표 df로 변환
    initial_df = pd.read_html(html,header=0)[0]
    #현재 테이블 컬럼 가져오기
    current_col = initial_df.columns.tolist()
    for col in current_col:
        if col == "교육일":
            initial_df = initial_df.rename({col:"요일"},axis=1)
            col = "요일"
        for value in initial_df[col]:
            dic[col].append(value)
    for _ in range(len(initial_df[current_col[0]].values)):
        name_dic["구분"].append(htmlAll.find('div',{'class':'s_subject'}).find("p").text)
dic.update(name_dic)

##df 생성 및 컬럼 순서 변경
sort_columns = list(my_columns)
sort_columns.insert(0,"구분")
result_df = pd.DataFrame(dic)
result_df = result_df[sort_columns]
result_df = result_df.dropna(axis=0)# 결측값 행 제거

result_df.to_csv('./{}.csv'.format(sitename), sep=',', na_rep='NaN',encoding="CP949", index=False)