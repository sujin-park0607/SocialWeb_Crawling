from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

url = 'http://www.nrc.go.kr/hospital/html/content.do?depth=pr&menu_cd=02_03_02_02'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')
data = soup.find('table')

table = parser.make2d(data)

df = pd.DataFrame(data = table[1:], columns = table[0])
df = df.transpose()

df.to_csv(f'data/nrc.csv',encoding='utf-8-sig',index=False)