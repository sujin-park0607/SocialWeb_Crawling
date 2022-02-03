import pandas as pd
import time

class CrawlingUtill():
    def __init__(self,sitename = "[사이트이름]"):
        self.sitename = sitename

    ##실행시간 측정
    def runningTime(func):
        def inner(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print("실행시간: {}".format(end_time - start_time))
            return result
        return inner

    ##html.<table> -> table로 변환
    def crawlingHtml_to_table(self,parserhtml):
        htmlTable = parserhtml.find_all("table")
        table_html = str(htmlTable)
        table_df_list = pd.read_html(table_html)
        return table_df_list

    ##table -> csv로 변환
    def table_list_to_csv(self,table_df_list,program_name_list):
        if len(table_df_list)>len(program_name_list) :
            for _ in range(len(table_df_list)-len(program_name_list)):
                program_name_list.append(["이름 없음"])
        self.count = 0 
        for num in range(len(table_df_list)):
            self.count +=1
            table_df_list[num]["센터명"] = [self.sitename] * len(table_df_list[num]) 
            table_df_list[num].index = table_df_list[num].index + 1
            table_df_list[num].index.name = program_name_list[num]
            table_df_list[num].to_csv('./'+self.sitename+str(self.count)+'.csv', sep=',', na_rep='NaN')
