import pandas as pd
import requests
import bs4 
from io import StringIO
import time

table_url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
url = 'https://fbref.com/en/comps/9/passing/Premier-League-Stats'
base_url = 'https://fbref.com'

html = requests.get(table_url)
bs_obj = bs4.BeautifulSoup(html.text,"lxml")
for table in bs_obj.findAll("table"):
    df_table = pd.read_html(StringIO(str(table)),extract_links ="all")[0].apply(lambda col: [base_url + v[1] if v[1] else v[0] for v in  col])
    df_table.columns = [tt[0] or tt[1] for tt in df_table.columns]
    df_table.to_csv("table.csv")
    break

html = requests.get(url)
bs_obj = bs4.BeautifulSoup(html.text,"lxml")
i = 0
for comment in bs_obj.findAll(string=lambda string:isinstance(string, bs4.Comment)):
    c_soup = bs4.BeautifulSoup(comment,"lxml")
    for table in c_soup.findAll("table"):
        df = pd.read_html(StringIO(str(table)),extract_links ="all")[0].apply(lambda col: [base_url + v[1] if v[1] else v[0] for v in  col])
        i+=1
        df.columns = [tt[1][0] or tt[1][1] or tt[0][0] or tt[0][1] for tt in df.columns]
        df = df[df.Rk != 'Rk']
        df.to_csv("df"+str(i)+".csv")

df = df_table.merge(df, how = 'left', on = 'Squad')

list_of_dfs = list()
for match_log_url in df.Matches:
    time.sleep(5)
    print("Getting " + match_log_url)
    html = requests.get(match_log_url)
    bs_obj = bs4.BeautifulSoup(html.text,"lxml")
    for table in bs_obj.findAll("table"):
        df_temp = pd.read_html(StringIO(str(table)),extract_links ="all")[0].apply(lambda col: [base_url + v[1] if v[1] else v[0] for v in  col])
        df_temp.columns = [tt[1][0] or tt[1][1] or tt[0][0] or tt[0][1] for tt in df_temp.columns]
        df_temp = df_temp[df_temp.Day != ""]
        df_temp["source"] = match_log_url
        print(df_temp.shape)
        list_of_dfs.append(df_temp)

main_df = pd.concat(list_of_dfs)
main_df.to_csv("main_df.csv")

j_df = df.merge(main_df, how = 'left', left_on = 'Matches', right_on = 'source')

j_df.to_csv("joined_df.csv")
