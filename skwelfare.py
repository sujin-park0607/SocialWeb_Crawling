import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
from django.http import response
from html_table_parser import parser_functions as parser

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

# wd =  webdriver.Chrome('chromedriver',options=chrome_options)
# wd.implicitly_wait(10)

url = 'http://www.skwelfare.or.kr/~swimming#'

reponse = requests.get(url)
html = reponse.text
soup = BeautifulSoup(html,'html.parser')

data = soup.find('div' , {'class':'tabZone'})
p = data.find_all('p')
h3 = data.find_all('h3')

program = data.find('h2')
content = p[1]
user = p[3]

table_data = soup.find_all('table')

Column1 = ['요일','강습반명','시간','비용','프로그램']
table1 = parser.make2d(table_data[0])
table1[0].append(h3[0].text)

df1 = pd.DataFrame(data=table1, columns = Column1)
#print(df1)

Column2 = ['요일','강습반명','강습정원','시간','비용','프로그램']
table2 = parser.make2d(table_data[1])
table2[0].append(h3[1].text)
df2 = pd.DataFrame(data=table2, columns = Column2)
# print(df2)

Column3 = ['시간','비용','프로그램']
table3 = parser.make2d(table_data[2])
table3[0].append(h3[2].text)
df3 = pd.DataFrame(data=table3, columns = Column3)

df = pd.concat([df1,df2,df3])
print(df)

df.to_csv(f'data/skwlfare.csv',encoding='utf-8-sig',index=False)
# print(df)
# wd.find_element_by_xpath('//*[@id="tab1m2"]/a').click()
# wd.implicitly_wait(10)



