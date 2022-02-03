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
    def find_data(self,url,elem_func = False,program_page=""):
        self.html = requests.get(url+program_page).text
        self.htmlAll = bs(self.html,'html.parser')
        if elem_func == False:
            return 0
        self.finded_data = elem_func
        return self.finded_data

    
    ## dic, name_dic 변수에 데이터 추가
    def col_append_data(self, df, grogram_name_func, current_col=[], differ_col = []):
        if len(current_col) == 0:
            current_col = df.columns.tolist()

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
        result_df.to_csv('./{}.csv'.format(self.sitename), sep=',', na_rep='NaN',encoding="utf-8-sig", index=False)

    def sbsports(self):##서부재활체육센터
        sitename = "서부재활체육센터"
        my_columns = ["프로그램", "대상","참가요일","시간","회비"]
        url = "http://www.sbsports.or.kr/sub/wrcAble.do"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        df_list = self.find_data(url,pd.read_html(self.html,header=0))
        tb_name_list = [x.text.strip() for x in self.htmlAll.find_all("caption")]

        for i in range(len(df_list)):#len(df_list)
            ##현재 테이블의 컬럼 가져오기
            current_col = df_list[i].columns.tolist()
            for name in current_col:
                df_list[i]=df_list[i].rename({name:name.replace(" ","")},axis=1)
            current_col = df_list[i].columns.tolist()
            print(current_col)

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


s = Total_crawling()
s.sbsports()