from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

def to_dict(table):
    programs = []
    content = []
    for col in range(1,len(table)):
        con = ''
        for row in range(len(table[0])):
            if row == 0:
                programs.append(table[col][row])
            else:
                con += table[col][row] + '\n'
        content.append(con)
    print(programs)
    print(content)
    return programs, content
    
url = 'http://dasadgym.or.kr/menu03_06.php'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')

data = soup.find_all('table',{'class':'exercise_main'})
info = soup.find('div',{'id':'ft_add'}).get_text().split('│')

tel = info[2].replace('Tel : ','')
company = info[0]

table1 = parser.make2d(data[0])
table2 = parser.make2d(data[1])

programs1, content1 = to_dict(table1)
programs2, content2 = to_dict(table2)

dict1 = {'Programs':programs1,'Content':content1,'Company':company,'Tel':tel,'Name':None,'Applicant':None,'Apply':None,'Url':url}
dict2 = {'Programs':programs2,'Content':content2,'Company':company,'Tel':tel,'Name':None,'Applicant':None,'Apply':None,'Url':url}

df1 = pd.DataFrame(dict1)
df2 = pd.DataFrame(dict2)

df = pd.concat([df1,df2])
print(df)
df.to_csv('data/dasadgym.csv',encoding='utf-8-sig',index=False)
