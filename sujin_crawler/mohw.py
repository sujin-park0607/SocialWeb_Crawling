from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

url = 'https://www.mohw.go.kr/react/policy/index.jsp?PAR_MENU_ID=06&MENU_ID=06370109&PAGE=9'

response = requests.get(url)

html = response.text
soup = BeautifulSoup(html,'html.parser')
data = soup.find('table')

info = soup.find('div',{'class':'f_address'}).get_text().split("/")
tel = info[1].replace("당직실 : ","")
company = "보건복지부"

table = parser.make2d(data)

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
df.to_csv(f'data/mohw.csv', index=False, encoding='utf-8-sig')
    

