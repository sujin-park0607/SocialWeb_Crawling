from bs4 import BeautifulSoup 
import bs4
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

wd =  webdriver.Chrome('chromedriver',options=chrome_options)
wd.implicitly_wait(10)

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

print(temp_list)