from bs4 import BeautifulSoup 
import bs4
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def webdriver_g():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        wd =  webdriver.Chrome('chromedriver',options=chrome_options)
        wd.implicitly_wait(10)
        return wd
        

    #누림 - 데이터수집 및 문자열처리 
def nurim(wd, url):

    #데이터프레임 생성
    df = pd.DataFrame(columns = ('Programs','Content','Company','Tel','Name','Applicant','Apply','Url'))

    wd.get(url) 

    info = wd.find_element_by_xpath('//*[@id="footer"]/div/div[3]/address').text.split(' ')
    tel = info[9]
    company = info[0]
    for i in range(10):
        #창 클릭하기
        x_count = i+1
        xpath = '//*[@id="accordion"]/h3[{}]/a'.format(x_count)
        program = wd.find_element_by_xpath(xpath).text
        program = program.replace("Q.","")
        
        wd.find_element_by_xpath(xpath).click()
        wd.implicitly_wait(10)
        
        answer_box_id = 'an_0{}'.format(i)
        text = wd.find_element_by_id(answer_box_id).text

        #받아온 데이터 문자열처리하기 
        temp_list = text \
        .replace("□ 지원대상", "|T|") \
        .replace("□ 서비스대상","|T|") \
        .replace("□ 지원내용", "|T|") \
        .replace("□ 신청방법 및 문의", "|T|") \
        .replace("□ 출처:", "|T|") \
        .replace("□ 최종수정일:", "|T|") \
        .split("|T|")

        temp_list = [i.strip().replace("\n\n", "\n") for i in temp_list]
        temp_list[1:-1] = [i.strip().split("\n") for i in temp_list[1:-1]]
        temp_list[-1] = temp_list[-1].split(" ")[0]

        # #인덱스로 각자 필요한 항목 변수지정
        applicant = ''.join(t for t in temp_list[1]).replace('-','').replace('=','')
        content = ''.join(t for t in temp_list[2]).replace('-','').replace('=','')
        apply = ''.join(t for t in temp_list[3]).split('2)')[0].replace("1) 신청방법","").replace(":","")
        name = None
        # if len(temp_list)== 6:
        #     company = temp_list[4][0]
        # else: company = " "
        df.loc[i] = [program,content,company,tel,name,applicant,apply,url]

    
    return df

wd = webdriver_g()

#재활 페이지
url1 = "https://www.ggnurim.or.kr/main/uss/olp/faq/FaqListInqire.do?qestnCn=8"
#신체건강 페이지
url2 = "https://www.ggnurim.or.kr/main/uss/olp/faq/FaqListInqire.do?qestnCn=10"


df1 = nurim(wd,url1)
df2 = nurim(wd,url2)
df = pd.concat([df1, df2])

df.to_csv(f'data/경기도지원센터누림.csv',encoding='utf-8-sig',index=False)
wd.close()
