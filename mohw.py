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

table = parser.make2d(data)
print(table)

df = pd.DataFrame(data = table[1:],columns = table[0] )
df.to_csv(f'data/mohw.csv', index=False, encoding='utf-8-sig')
    

