from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

url = 'http://ic-sports.or.kr/bbs/page.php?hid=cont_0301'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')

data = soup.find('table',{'class','clr_ct_tb01'})
table = parser.make2d(data)
for t in table:
    for i in range(7):
        t[i] = t[i].replace('\r\n\t\t\t\t','')

df = pd.DataFrame(data = table[1:], columns = table[0])
print(df)
df.to_csv('data/ic_sports.csv',encoding='utf-8-sig',index=False)