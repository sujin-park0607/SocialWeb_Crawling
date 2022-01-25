from bs4 import BeautifulSoup
from django.http import response
import requests

url = 'https://www.mohw.go.kr/react/policy/index.jsp?PAR_MENU_ID=06&MENU_ID=06370109&PAGE=9'

response = requests.get(url)

html = response.text
soup = BeautifulSoup(html,'html.parser')
data = soup.find_all('tbody', {'class':'th_center'})

th = soup.select('tr > th')
td = soup.select('tr > td')
for i in th:
    print(i.get_text())

for j in td:
    print(j.get_text())
    

