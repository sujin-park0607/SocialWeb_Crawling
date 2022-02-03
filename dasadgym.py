from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

url = 'http://dasadgym.or.kr/menu03_06.php'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')

data = soup.find_all('table',{'class':'exercise_main'})

table1 = parser.make2d(data[0])
table2 = parser.make2d(data[1])

df1 = pd.DataFrame(data=table1[1:], columns=table1[0])
df2 = pd.DataFrame(data=table2[1:], columns=table2[0])


df = pd.concat([df1,df2])
print(df)
df.to_csv('data/dasadgym.csv',encoding='utf-8-sig',index=False)
