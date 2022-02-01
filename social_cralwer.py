from bs4 import BeautifulSoup
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

class DataCrawler():
    def __init__(self):
        pass

    def parser_soup(self,url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        return soup
        

    def dasadgym(self):
        url = 'http://dasadgym.or.kr/menu03_06.php'
        soup = self.parser_soup(url)

        data = soup.find_all('table',{'class':'exercise_main'})

        table1 = parser.make2d(data[0])
        table2 = parser.make2d(data[1])

        df1 = pd.DataFrame(data=table1[1:], columns=table1[0])
        df2 = pd.DataFrame(data=table2[1:], columns=table2[0])


        gym_df = pd.concat([df1,df2])
        return gym_df
        # df.to_csv('data/dasadgym.csv',encoding='utf-8-sig',index=False)

    def nrc(self):
        url = 'http://www.nrc.go.kr/hospital/html/content.do?depth=pr&menu_cd=02_03_02_02'
        soup = self.parser_soup(url)

        data = soup.find('table')
        table = parser.make2d(data)

        df = pd.DataFrame(data = table[1:], columns = table[0])
        nrc_df = df.transpose()

        # df.to_csv(f'data/nrc.csv',encoding='utf-8-sig',index=False)
        return nrc_df


    def ic_sports(self):
        url = 'http://ic-sports.or.kr/bbs/page.php?hid=cont_0301'

        soup = self.parser_soup(url)

        data = soup.find('table',{'class','clr_ct_tb01'})
        table = parser.make2d(data)
        for t in table:
            for i in range(7):
                t[i] = t[i].replace('\r\n\t\t\t\t','')

        ic_sports_df = pd.DataFrame(data = table[1:], columns = table[0])
        # df.to_csv('data/ic_sports.csv',encoding='utf-8-sig',index=False)
        return ic_sports_df


    def mohw(self):
        url = 'https://www.mohw.go.kr/react/policy/index.jsp?PAR_MENU_ID=06&MENU_ID=06370109&PAGE=9'

        soup = self.parser_soup(url)
        data = soup.find('table')

        table = parser.make2d(data)

        mohw_df = pd.DataFrame(data = table[1:],columns = table[0] )
        # df.to_csv(f'data/mohw.csv', index=False, encoding='utf-8-sig')
        return mohw_df


if __name__=='__main__':
    crawler = DataCrawler()
    print(crawler.dasadgym())
    print(crawler.ic_sports())
    print(crawler.mohw())
    print(crawler.nrc())