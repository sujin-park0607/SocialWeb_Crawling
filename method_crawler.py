from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

class Total_crawling():
    def __init__(self):
        # self.dic={}
        # self.name_dic={}
        # self.my_columns = []
        # self.sitename = ""
        pass
    
    ##초기 변수 셋팅
    def initial_setting(self,sitename,col_list):
        self.dic={}
        self.my_columns = col_list
        for col in self.my_columns:
            self.dic[col]=list()
        self.name_dic={"구분":[]}
        self.sitename = sitename


    ## 프로그램 사이트 url 찾기
    def find_data(self,url,program_page=""):
        self.html = requests.get(url+program_page).text
        self.htmlAll = bs(self.html,'html.parser')

    
    ## dic, name_dic 변수에 데이터 추가
    def col_append_data(self, df, grogram_name_func, current_col=[], differ_col = []):
        for col in current_col:
            for value in df[col]:
                self.dic[col].append(value)
        if len(differ_col) != 0:
            for differ in differ_col:
                for _ in range(len(df[col])):
                    self.dic[differ].append("")
        for _ in range(len(df[current_col[0]].values)):
            self.name_dic["구분"].append(grogram_name_func)
    
    def dic_to_csv(self):
        sort_columns = list(self.my_columns)
        sort_columns.insert(0,"구분")
        result_df = pd.DataFrame(self.dic)
        result_df = result_df[sort_columns]
        # result_df = result_df.dropna(axis=0)# 결측값 행 제거
        result_df.to_csv('data/{}.csv'.format(self.sitename), sep=',', na_rep='NaN',encoding="utf-8-sig", index=False)

    def sbsports(self):##서부재활체육센터
        sitename = "서부재활체육센터"
        my_columns = ["프로그램", "대상","참가요일","시간","회비"]
        url = "http://www.sbsports.or.kr/sub/wrcAble.do"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        df_list = pd.read_html(self.html,header=0)
        tb_name_list = [x.text.strip() for x in self.htmlAll.find_all("caption")]

        for i in range(len(df_list)):#len(df_list)
            ##현재 테이블의 컬럼 가져오기
            current_col = df_list[i].columns.tolist()
            for name in current_col:
                df_list[i]=df_list[i].rename({name:name.replace(" ","")},axis=1)
            current_col = df_list[i].columns.tolist()

            for col in current_col:
                if col == "비고":
                    current_col.remove(col)
                elif col == "구분":
                    df_list[i]=df_list[i].rename({col:"프로그램"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램")
                elif col == "참가요일 및 시간":
                    df_list[i]=df_list[i].rename({col:"참가요일"},axis=1)
                    current_col.remove(col)
                    current_col.append("참가요일")
                elif col == "정원":
                    current_col.remove(col)
                elif col == "프로그램.1":
                    current_col.remove(col)
        
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))

            self.col_append_data(df_list[i],tb_name_list[i][:-3]+"프로그램" if tb_name_list[i].find("테이블")!=-1 else tb_name_list[i], current_col = inter_col, differ_col = differ_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()
    
    
    def sbsd(self):#서부산권장애인스포츠센터
        sitename = "서부산권장애인스포츠센터"
        my_columns = ["프로그램", "시간", "대상", "요일", "사용료", "정원"]
        url = "https://www.sbsd.kr/Home/"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        program_page = self.htmlAll.find("li",{"class":"cd1 cd1c4"}).find("a")["href"].split("/")[-1]
        self.find_data(url,program_page=program_page)
        pages = self.htmlAll.find('nav',{"class":"tabmenu"}).find_all("li",{"class":"cd3"})
        programURLs = []
        for elem in pages:
            programURLs.append(elem.find("a")["href"].split("/")[-1])   ## 페이지 넘버
        for i in range(len(programURLs)):
            self.find_data(url,program_page = programURLs[i])
            initial_df = pd.read_html(self.html,header=0)[0]
            current_col = initial_df.columns.tolist()
            for col in current_col:
                if col == "교육일":
                    initial_df = initial_df.rename({col:"요일"},axis=1)
                    col = "요일"
                for value in initial_df[col]:
                    self.dic[col].append(value)
            for _ in range(len(initial_df[current_col[0]].values)):
                self.name_dic["구분"].append(self.htmlAll.find('div',{'class':'s_subject'}).find("p").text)
        self.dic.update(self.name_dic)
        self.dic_to_csv()
    
    
    def bisco(self):#부산한마음스포츠센터
        sitename = "부산한마음스포츠센터"
        my_columns = ["프로그램","반","대상","교육일","시간","정원","교육비","비고"]
        url = "http://hmsports.bisco.or.kr"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        program_page = self.htmlAll.find_all("li",{"class":"mn_li1"})[1].find("a")["href"]
        self.find_data(url,program_page=program_page)
        pages = self.htmlAll.find_all("ul",{"class":"depth2"})[-1].find_all("a")
        programURLs = [url["href"] for url in pages]
        del programURLs[-1]## 통합방과후학교 삭제
        del programURLs[4]## 실내골프연습장 삭제
        del programURLs[2]## 피트니스실 삭제      
        for purl in programURLs:
            self.find_data(url,program_page=purl)
            initial_df = pd.read_html(self.html,header=0)[0]
            current_col = initial_df.columns.tolist()
            self.col_append_data(initial_df,self.htmlAll.find("div",{"id":"print"}).find('h4',{'class':'ctit'}).text,current_col=current_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()

s = Total_crawling()
s.sbsports()
s.sbsd()
s.bisco()