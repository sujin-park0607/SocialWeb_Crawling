from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd
import numpy as np

url = 'http://www.nrc.go.kr/hospital/html/content.do?depth=pr&menu_cd=02_03_02_02'
company = "보건복지부 국립재활원"

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')
data = soup.find('table')

info = soup.find_all('span',{'class':'fa_number'})[2].get_text()
tel = info.replace('TEL. ',"").replace(')','').replace('- ','')


table = parser.make2d(data)

table = np.array(table)
table = table.transpose()
# print(table)

programs = []
content = []
applicant = []

for col in range(1,len(table)):
    con = ''
    for row in range(len(table[0])):
        if row == 0:
            programs.append(table[col][row])
        elif row == 1:
            applicant.append(table[col][row])
        else:
            con += table[col][row] + '\n'
    content.append(con)

dict = {'Programs':programs,'Content':content,'Company':company,'Tel':tel,'Name':None,'Applicant':applicant,'Apply':None,'Url':url}

df = pd.DataFrame(dict)

df.to_csv(f'data/nrc.csv',encoding='utf-8-sig',index=False)