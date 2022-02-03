from cgitb import lookup
import time
from unittest import result
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from crawlingutil import CrawlingUtill

cutil = CrawlingUtill('생활체육정보센터')
def __init__(self):
    self.columns = ['년도','번호','지역','클럽명','활동시간','종목','기타종목','장애유형','승인일']
    self.years = [2022]#2020,2021,
    self.dic={}
    self.year = 0
    ## dic 초기화
    for col in self.columns:
        self.dic[col] = list()

## selenium 실행
def openSelenium(self,year):
    self.year = year
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    self.driver = webdriver.Chrome('./chromedriver.exe')#options=chrome_options
    self.driver.implicitly_wait(10)

    self.driver.get("https://sports.koreanpc.kr/front/club/listClub.do;jsessionid=0E47FE540D3B9FC0C51A3B4D4B356314")
    return self.lookup(self.year)

##등록년도 조회
def lookup(self, year):
    self.input_text = self.driver.find_element_by_id('searchYear')
    self.input_text.clear()
    self.input_text.send_keys(year)
    self.driver.find_element_by_class_name("btn_v6").click()
    return self.find_last_page()
    
##마지막 페이지 찾기
def find_last_page(self):
    self.page_bar = self.driver.find_elements_by_class_name("paging_area")[0]
    self.pages = self.page_bar.find_elements_by_tag_name('a')[-1].click()
    self.page_bar = self.driver.find_elements_by_class_name("paging_area")[0]
    self.last_page = self.page_bar.find_elements_by_tag_name('a')[-3].text
    return self.retrunfirst(int(self.last_page))
    

## 마지막 페이지 저장 후 처음으로 이동(초기 셋팅)
def retrunfirst(self,last_page):
    self.last_page = last_page
    self.page_bar = self.driver.find_elements_by_class_name("paging_area")[0]
    self.page_bar.find_elements_by_tag_name('a')[0].click()
    return self.crawling1()

#반복하여 페이지 이동
def crawling1(self):
    BARCOUNT = 2
    while(True):
        self.current_page = int(self.driver.find_element_by_class_name("current").text)
        self.page_index = self.current_page%10+BARCOUNT
        self.page_bar = self.driver.find_elements_by_class_name("paging_area")[0]
        self.page_bar.find_elements_by_tag_name('a')[self.page_index].click()       

        ##데이터 추가 
        self.html = self.driver.page_source
        self.result = bs(self.html, 'lxml') #==html.parser
        self.result1 = self.result.find_all('td',{'data-cell-header':self.columns})
        self.result2 = list(map(lambda x : x.text.strip(),self.result1))
        self.count = 1
        self.dic[self.columns[0]].append(self.year) ## 년도 추가
        for i in range(len(self.result2)):
            if i > 0 and i % 8 == 0:
                self.dic[self.columns[0]].append(self.year) ## 년도 추가
                self.count -= 8
            self.dic[self.columns[self.count]].append(self.result2[i])## 홈페이지의 데이터 추가
            self.count+=1

        if self.current_page % 10 == 0:    ## 모든 함수 수행 후 실행해야 함
            self.page_bar = self.driver.find_elements_by_class_name("paging_area")[0]
            self.page_bar.find_elements_by_tag_name('a')[-2].click()
        
        if self.current_page >= self.last_page:
            return True
            
            
        
    #dataFrame 만들기       
def make_df(self):
    self.dic['센터명'] = ['생활체육정보센터']*len(self.dic['번호'])
    self.fir_df = pd.DataFrame(self.dic,columns=self.dic.keys(), index=self.dic['번호'])
    # self.fir_df = self.fir_df.sort_values('번호', ascending = True)##인덱스 제거로 인한 정렬 불필요
    self.fin_df= self.fir_df.drop('번호',axis=1)
    self.fin_df.to_csv('./{}.csv'.format(cutil.sitename), sep=',', na_rep='NaN',encoding="CP949", index=False)
    print('-'*30+"dataFrame CSV파일로 저장 중"+'-'*30)
    return self.fin_df


#시작
def run(self):
    self.columns = ['년도','번호','지역','클럽명','활동시간','종목','기타종목','장애유형','승인일']
    self.years = [2022]#2020,2021,
    self.dic={}
    self.year = 0
    
    ## dic 초기화
    for col in self.columns:
        self.dic[col] = list()

    self.checkFirst = False
    for year in self.years:
        print('-'*30+"생활체육정보센터 "+str(year)+"년도 검색중"+'-'*30)
        if self.checkFirst == False:
            self.checkFirst = self.openSelenium(year)
        else:
            self.lookup(year)
        print('-'*30+"생활체육정보센터 "+str(year)+"년도 검색완료"+'-'*30)
    self.driver.quit()
    return self.make_df()

if __name__ =="__main__":
    run()