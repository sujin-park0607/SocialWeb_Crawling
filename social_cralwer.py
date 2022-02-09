from bs4 import BeautifulSoup 
import bs4
from django.http import response
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import numpy as np

class DataCrawler():
    def __init__(self):
        pass

    #selenium webdriver 
    def webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        wd =  webdriver.Chrome('chromedriver',options=chrome_options)
        wd.implicitly_wait(10)
        return wd

    #beautifulSoup html parser
    def parser_soup(self,url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        return soup

    def to_dict(self,table):
        programs = []
        content = []
        for col in range(1,len(table)):
            con = ''
            for row in range(len(table[0])):
                if row == 0:
                    programs.append(table[col][row])
                else:
                    con += table[col][row] + '\n'
            content.append(con)
        print(programs)
        print(content)
        return programs, content

    #대구광역시장애인 국민 체육센터
    def dasadgym(self):
        url = 'http://dasadgym.or.kr/menu03_06.php'
        soup = self.parser_soup(url)

        data = soup.find_all('table',{'class':'exercise_main'})
        info = soup.find('div',{'id':'ft_add'}).get_text().split('│')

        tel = info[2].replace('Tel : ','')
        company = info[0]

        table1 = parser.make2d(data[0])
        table2 = parser.make2d(data[1])

        programs1, content1 = self.to_dict(table1)
        programs2, content2 = self.to_dict(table2)

        dict1 = {'프로그램명':programs1,'설명':content1,'담당자이름':None,'담당기관':company,'담당자연락처':tel,'신청자격':None,'연결URL':url,'신청방법':None}
        dict2 = {'프로그램명':programs2,'설명':content2,'담당자이름':None,'담당기관':company,'담당자연락처':tel,'신청자격':None,'연결URL':url,'신청방법':None}

        df1 = pd.DataFrame(dict1)
        df2 = pd.DataFrame(dict2)

        df = pd.concat([df1,df2])
        df.to_csv('data/대구광역시장애인국민체육센터.csv',encoding='utf-8-sig',index=False)
        return df
        

    def nrc(self):
        url = 'http://www.nrc.go.kr/hospital/html/content.do?depth=pr&menu_cd=02_03_02_02'
        company = "보건복지부 국립재활원"

        soup = self.parser_soup(url)
        data = soup.find('table')

        info = soup.find_all('span',{'class':'fa_number'})[2].get_text()
        tel = info.replace('TEL. ',"").replace(')','').replace('- ','')

        table = parser.make2d(data)

        table = np.array(table)
        table = table.transpose()
        # print(table)

        programs = []
        content = []
        applicant = []

        for col in range(1,len(table)):
            con = ''
            for row in range(len(table[0])):
                if row == 0:
                    programs.append(table[col][row])
                elif row == 1:
                    applicant.append(table[col][row])
                else:
                    con += table[col][row] + '\n'
            content.append(con)
        
        dict = {'프로그램명':programs,'설명':content,'담당자이름':None,'담당기관':company,'담당자연락처':tel,'신청자격':applicant,'연결URL':url,'신청방법':None}
        df = pd.DataFrame(dict)

        df.to_csv(f'data/보건복지부국립재활원.csv',encoding='utf-8-sig',index=False)
        return df




    #인천광역시장애인 국민체육센터
    def ic_sports(self):
        url = 'http://ic-sports.or.kr/bbs/page.php?hid=cont_0301'

        soup = self.parser_soup(url)
            #기관, 위치, 전화번호
        info = soup.find('ul',{'class':'infos'}).get_text().split('\n')
        company = info[1]
        tel = info[5].replace('Tel','')

        data = soup.find('table',{'class','clr_ct_tb01'})
        table = parser.make2d(data)
        for t in table:
            for i in range(7):
                t[i] = t[i].replace('\r\n\t\t\t\t','')

        programs = []
        content = []
        applicant = []

            #데이터 컬럼에 맞게 넣기
        for col in range(1,len(table)):
            con = ''
            for row in range(len(table[0])):
                if row == 2:
                    programs.append(table[col][row])
                elif row == 3:
                    applicant.append(table[col][row])
                elif row != 1 and row !=0:
                    con += table[col][row] + '\n'
            content.append(con)
        dict = {'프로그램명':programs,'설명':content,'담당자이름':None,'담당기관':company,'담당자연락처':tel,'신청자격':applicant,'연결URL':url,'신청방법':None}
        df = pd.DataFrame(dict)
        df.to_csv('data/인천광역시장애인국민체육센터.csv',encoding='utf-8-sig',index=False)

    #보건복지부 장애인정책 
    def mohw(self):
        url = 'https://www.mohw.go.kr/react/policy/index.jsp?PAR_MENU_ID=06&MENU_ID=06370109&PAGE=9'
        soup = self.parser_soup(url)
        data = soup.find('table')

        info = soup.find('div',{'class':'f_address'}).get_text().split("/")
        tel = info[1].replace("당직실 : ","")
        company = "보건복지부"
        table = parser.make2d(data)

        programs = []
        content = []
        applicant = []

        for col in range(1,len(table)):
            con = ''
            for row in range(len(table[0])):
                if row == 0:
                    programs.append(table[col][row])
                elif row == 1:
                    applicant.append(table[col][row])
                else:
                    con += table[col][row] + '\n'
            content.append(con)
        dict = {'프로그램명':programs,'설명':content,'담당자이름':None,'담당기관':company,'담당자연락처':tel,'신청자격':applicant,'연결URL':url,'신청방법':None}
        df = pd.DataFrame(dict)
        df.to_csv(f'data/보건복지부장애인정책 .csv', index=False, encoding='utf-8-sig')
        return df

    #대구광역시 -컬럼 분할함수 
    def sk_to_dict(self,w_content,table):
        content = []
        for col in range(len(table)):
            con = '{}\n'.format(w_content)
            for row in range(len(table[0])):
                con += table[col][row] + '\n'
            content.append(con)
        return content

    #대구광역시 서구건강체력관 
    def skwelfare(self):
        url = 'http://www.skwelfare.or.kr/~swimming#'
        soup = self.parser_soup(url)

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
        content = self.sk_to_dict(w_content,table1)

        table2 = parser.make2d(table_data[1])
        content2 = self.sk_to_dict(w_content,table2)

        table3 = parser.make2d(table_data[2])
        content3 = self.sk_to_dict(w_content,table3)

        content = content + content2 + content3

        dict = {'프로그램명':programs,'설명':content,'담당자이름':None,'담당기관':company,'담당자연락처':tel,'신청자격':None,'연결URL':url,'신청방법':None}
        df = pd.DataFrame(dict)
        df.to_csv(f'data/대구서구건강체력관.csv',encoding='utf-8-sig',index=False)
    
    #경기도 장애인 복지 종합 지원센터 누림-실행함수 
    def nurim_run(self):
        wd = self.webdriver()

        #재활 페이지
        url1 = "https://www.ggnurim.or.kr/main/uss/olp/faq/FaqListInqire.do?qestnCn=8"
        #신체건강 페이지
        url2 = "https://www.ggnurim.or.kr/main/uss/olp/faq/FaqListInqire.do?qestnCn=10"


        df1 = self.nurim(wd,url1)
        df2 = self.nurim(wd,url2)
        df = pd.concat([df1, df2])

        df.to_csv(f'data/경기도지원센터누림.csv',encoding='utf-8-sig',index=False)
        wd.close()
        return df

    #누림 - 데이터수집 및 문자열처리 
    def nurim(self,wd, url):

        #데이터프레임 생성
        df = pd.DataFrame(columns = ('프로그램명','설명','담당자이름','담당기관','담당자연락처','신청자격','연결URL','신청방법'))

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
            df.loc[i] = [program,content,name,company,tel,applicant,url,apply]

        
        return df


    #방승철
    #------------------------------------------------------------------
    #selenium setting
    def openSelenium(self,year):
        self.year = year
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')
        chrome_options.add_argument("--start-maximized") # add
        chrome_options.add_argument("--window-size=1024,763") # add
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)#
        self.driver.implicitly_wait(15)
        self.url = "https://sports.koreanpc.kr/front/club/listClub.do;jsessionid=0E47FE540D3B9FC0C51A3B4D4B356314"
        self.driver.get(self.url)
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
        return self.koreanpc()

    #반복하여 페이지 이동
    def koreanpc(self):
        BARCOUNT = 2
        while(True):
            self.current_page = int(self.driver.find_element_by_class_name("current").text)
            self.page_index = self.current_page%10+BARCOUNT
            self.page_bar = self.driver.find_elements_by_class_name("paging_area")[0]
            self.page_bar.find_elements_by_tag_name('a')[self.page_index].click()       

            ##데이터 추가 
            self.html = self.driver.page_source
            self.result = BeautifulSoup(self.html, 'lxml') #==html.parser
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
        # self.fin_df.to_csv('data/생활체육정보센터.csv', sep=',', na_rep='NaN',encoding="CP949", index=False)
        return self.remk_df(self.fin_df)
    

    #데이터 형식 맞추기
    def remk_df(self,df):
        sitename = "생활체육정보센터"        
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]#,"담당기관","담당자연락처","연결URL"
        url = self.url
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        siteNumber = self.htmlAll.find("p",{"class":"footer_info"}).text.split("\n")[2].split()[-1]

        for i in range(len(df)):#len(df_list)
            ##현재 테이블의 컬럼 가져오기
            current_col = df.columns.tolist()

            merge_cols = ["종목","지역","활동시간"]##["참가요일","시간","회비"] => 설명 컬럼에 병합해서 넣기
            for col in current_col:
                if col == "클럽명":
                    df=df.rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "장애유형":
                    df=df.rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
            
            ## 설명 컴럼 추가
            current_col.append("설명")
            df['설명'] =df[merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))

            self.col_append_data(df,sitename,siteNumber,url, current_col = inter_col, differ_col = differ_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()


    #생활체육정보센터 -실행함수 
    def koreanpc_run(self):
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
        koreanpc_df = self.make_df()
        # print(koreanpc_df)
        return koreanpc_df

    ##초기 변수 셋팅
    def initial_setting(self,sitename,col_list):
        self.dic={}
        self.my_columns = col_list
        for col in self.my_columns:
            self.dic[col]=list()
        self.name_dic={"담당기관":[],"담당자연락처":[],"연결URL":[]}
        self.sitename = sitename


    ## 프로그램 사이트 url 찾기
    def find_data(self,url,program_page=""):
        self.html = requests.get(url+program_page).text
        self.htmlAll = BeautifulSoup(self.html,'html.parser')

    
    ## dic, name_dic 변수에 데이터 추가
    def col_append_data(self, df, site_name,siteNumber,siteURL, current_col=[], differ_col = []):
        for col in current_col:
            for value in df[col]:
                self.dic[col].append(value)
        if len(differ_col) != 0:
            for differ in differ_col:
                for _ in range(len(df[col])):
                    self.dic[differ].append("")
        for _ in range(len(df[current_col[0]].values)):
            self.name_dic["담당기관"].append(site_name)
            self.name_dic["담당자연락처"].append(siteNumber)
            self.name_dic["연결URL"].append(siteURL)
    
    def dic_to_csv(self):
        sort_columns = list(self.my_columns)
        sort_columns.insert(3,"담당기관")
        sort_columns.insert(4,"담당자연락처")
        sort_columns.insert(-1,"연결URL")
        result_df = pd.DataFrame(self.dic)
        result_df = result_df[sort_columns]
        result_df.to_csv('data/{}.csv'.format(self.sitename), sep=',', na_rep='NaN',encoding="utf-8-sig", index=False)

    def sbsports(self):##서부재활체육센터
        sitename = "서부재활체육센터"        
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]#,"담당기관","담당자연락처","연결URL"
        url = "http://www.sbsports.or.kr/sub/wrcAble.do"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        siteNumber = self.htmlAll.find("ul",{"class":"clearfix"}).find_all("li")[1].text[5:-2]
        df_list = pd.read_html(self.html,header=0)
        # tb_name_list = [x.text.strip() for x in self.htmlAll.find_all("caption")]

        for i in range(len(df_list)):#len(df_list)
            ##현재 테이블의 컬럼 가져오기
            current_col = df_list[i].columns.tolist()
            for name in current_col:
                df_list[i]=df_list[i].rename({name:name.replace(" ","")},axis=1)
            current_col = df_list[i].columns.tolist()

            merge_cols = []##["참가요일","시간","회비"] => 설명 컬럼에 병합해서 넣기
            for col in current_col:
                if col == "비고":
                    current_col.remove(col)
                if col == "구분" or col == "프로그램":
                    df_list[i]=df_list[i].rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "참가요일 및 시간" or col == "참가요일":
                    df_list[i]=df_list[i].rename({col:"참가요일"},axis=1)
                    merge_cols.append("참가요일")
                    # current_col.remove(col)
                    # current_col.append("참가요일")
                    current_col.remove(col)
                if col == "정원":
                    current_col.remove(col)
                if col == "프로그램.1":
                    current_col.remove(col)
                if col == "대상":
                    df_list[i]=df_list[i].rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
                if col == "시간":
                    merge_cols.append("시간")
                if col == "회비":
                    merge_cols.append("회비")
            
            ## 설명 컴럼 추가
            current_col.append("설명")
            df_list[i]['설명'] =df_list[i][merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))

            self.col_append_data(df_list[i],sitename,siteNumber,url, current_col = inter_col, differ_col = differ_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()
    
    
    def sbsd(self):#서부산권장애인스포츠센터
        sitename = "서부산권장애인스포츠센터"
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]
        url = "https://www.sbsd.kr/Home/"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        program_page = self.htmlAll.find("li",{"class":"cd1 cd1c4"}).find("a")["href"].split("/")[-1]
        self.find_data(url,program_page=program_page)
        siteNumber = " ".join(self.htmlAll.find("address",{"class":"foot_in"}).find("span").text.split()[2:4])
        pages = self.htmlAll.find('nav',{"class":"tabmenu"}).find_all("li",{"class":"cd3"})
        programURLs = []
        
        for elem in pages:
            programURLs.append(elem.find("a")["href"].split("/")[-1])   ## 페이지 넘버
        for i in range(len(programURLs)):
            self.find_data(url,program_page = programURLs[i])
            initial_df = pd.read_html(self.html,header=0)[0]
            current_col = initial_df.columns.tolist()
            merge_cols = []
            for col in current_col:
                if col == "프로그램":
                    initial_df = initial_df.rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "교육일":
                    current_col.remove(col)
                    merge_cols.append("교육일")
                if col == "대상":
                    initial_df = initial_df.rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
                if col == "시간":
                    current_col.remove(col)
                    merge_cols.append("시간")
                if col == "사용료":
                    current_col.remove(col)
                    merge_cols.append("사용료")
                if col == "정원":
                    current_col.remove(col)
                    merge_cols.append("정원")
            current_col.append("설명")
            initial_df['설명'] =initial_df[merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))
            self.col_append_data(initial_df,sitename,siteNumber,url+programURLs[i], current_col = inter_col,differ_col=differ_col)
            # for col in current_col:
            #     for value in initial_df[col]:
            #         self.dic[col].append(value)
            # for _ in range(len(initial_df[current_col[0]].values)):
            #     self.name_dic["담당기관"].append(sitename)
            #     self.name_dic["담당자연락처"].append(siteNumber)
            #     self.name_dic["연결URL"].append(url)
        self.dic.update(self.name_dic)
        self.dic_to_csv()
    
    
    def bisco(self):#부산한마음스포츠센터
        sitename = "부산한마음스포츠센터"
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]
        url = "http://hmsports.bisco.or.kr"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        program_page = self.htmlAll.find_all("li",{"class":"mn_li1"})[1].find("a")["href"]
        self.find_data(url,program_page=program_page)
        siteNumber = ""
        pages = self.htmlAll.find_all("ul",{"class":"depth2"})[-1].find_all("a")
        programURLs = [url["href"] for url in pages]
        del programURLs[-1]## 통합방과후학교 삭제
        del programURLs[4]## 실내골프연습장 삭제
        del programURLs[2]## 피트니스실 삭제      
        for purl in programURLs:
            self.find_data(url,program_page=purl)
            initial_df = pd.read_html(self.html,header=0)[0]
            current_col = initial_df.columns.tolist()
            merge_cols = ["반","교육일","시간"]
            for col in current_col:
                if col == "프로그램":
                    initial_df = initial_df.rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "대상":
                    initial_df = initial_df.rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
            current_col.append("설명")
            initial_df['설명'] =initial_df[merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))
            self.col_append_data(initial_df,sitename,siteNumber,url+purl, current_col = inter_col,differ_col=differ_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()


if __name__=='__main__':
    crawler = DataCrawler()
    print(crawler.dasadgym())
    print(crawler.ic_sports())
    print(crawler.mohw())
    print(crawler.nrc())
    print(crawler.nurim_run())
    print(crawler.skwelfare())
    print(crawler.koreanpc_run())
    print(crawler.bisco())
    print(crawler.sbsports())
    print(crawler.sbsd())