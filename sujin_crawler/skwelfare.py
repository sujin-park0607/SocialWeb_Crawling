import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
from django.http import response
from html_table_parser import parser_functions as parser



def parser_soup(url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        return soup

def sk_to_dict(w_content,table):
        content = []
        for col in range(len(table)):
            con = '{}\n'.format(w_content)
            for row in range(len(table[0])):
                con += table[col][row] + '\n'
            content.append(con)
        return content

url = 'http://www.skwelfare.or.kr/~swimming#'
soup = parser_soup(url)

data = soup.find('div' , {'class':'tabZone'})
info = data.find_all('p')

programs = []
h3 = data.find_all('h3')
for i in h3:
        programs.append(i.get_text())
tel = soup.find('a',{'class':'tel'}).get_text().replace('(','').replace(')',' ').replace('-',' ')
company = "대전광역시 서구건강체력관"
user = info[3].get_text()
w_content = info[1].get_text()
table_data = soup.find_all('table')

table1 = parser.make2d(table_data[0])
content = sk_to_dict(w_content,table1)

table2 = parser.make2d(table_data[1])
content2 = sk_to_dict(w_content,table2)

table3 = parser.make2d(table_data[2])
content3 = sk_to_dict(w_content,table3)

content = content + content2 + content3


dict = {'Programs':programs,'Content':content,'Company':company,'Tel':tel,'Name':None,'Applicant':user,'Apply':None,'Url':url}
df = pd.DataFrame(dict)
df.to_csv(f'data/대구서구건강체력관.csv',encoding='utf-8-sig',index=False)




