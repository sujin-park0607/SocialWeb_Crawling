from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

url = 'http://ic-sports.or.kr/bbs/page.php?hid=cont_0301'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')

    #기관, 위치, 전화번호
info = soup.find('ul',{'class':'infos'}).get_text().split('\n')
company = info[1]
tel = info[5].replace('Tel','')

data = soup.find('table',{'class','clr_ct_tb01'})
table = parser.make2d(data)
for t in table:
    for i in range(7):
        t[i] = t[i].replace('\r\n\t\t\t\t','')

programs = []
content = []
applicant = []

    #데이터 컬럼에 맞게 넣기
for col in range(1,len(table)):
    con = ''
    for row in range(len(table[0])):
        if row == 2:
            programs.append(table[col][row])
        elif row == 3:
            applicant.append(table[col][row])
        elif row != 1 and row !=0:
            con += table[col][row] + '\n'
    content.append(con)

dict = {'Programs':programs,'Content':content,'Company':company,'Tel':tel,'Name':None,'Applicant':applicant,'Apply':None,'Url':url}

df = pd.DataFrame(dict)

df.to_csv('data/ic_sports.csv',encoding='utf-8-sig',index=False)