import pandas as pd
import numpy as np
import requests
import bs4 
from io import StringIO
import time
import re

table_url = 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats'
url = 'https://fbref.com/en/comps/9/passing/Premier-League-Stats'
base_url = 'https://fbref.com'

def get_table(url: str) -> pd.DataFrame:
    print("getting table from " + url)
    html = requests.get(url)
    print(html)
    bs_obj = bs4.BeautifulSoup(html.text,"lxml")

    table = bs_obj.findAll("table")[0]
    df_table = pd.read_html(StringIO(str(table)),extract_links ="all")[0].apply(lambda col: [base_url + v[1] if v[1] else v[0] for v in  col])
    df_table.columns = [tt[0] or tt[1] for tt in df_table.columns]
    return df_table

def get_matches(url: str) -> pd.DataFrame:
    print("getting match stats from " + url)
    html = requests.get(url)
    bs_obj = bs4.BeautifulSoup(html.text,"lxml")
    for table in bs_obj.findAll("table"):
        df_temp = pd.read_html(StringIO(str(table)),extract_links ="all")[0].apply(lambda col: [base_url + v[1] if v[1] else v[0] for v in  col])
        df_temp.columns = [tt[1][0] or tt[1][1] or tt[0][0] or tt[0][1] for tt in df_temp.columns]
        df_temp = df_temp[df_temp.Day != ""]
        df_temp["source"] = url
        return df_temp

table = get_table(table_url)
table.to_csv("output/new_table.csv")

squads = table["Squad"].apply(lambda x: x.rsplit('/',1)[0] + '/matchlogs/c9/passing')

matches_list = list()
for squad in squads:
    time.sleep(5)
    matches_list.append(get_matches(squad))
matches_df = pd.concat(matches_list)
matches_df.to_csv("output/matches_long.csv")

col_cleaner = np.vectorize(lambda x: re.sub(".3$","_long",
                                            re.sub(".2$","_medium",
                                                   re.sub(".1$","_short",x))
                                            )
                          )
matches_df.columns = col_cleaner(matches_df.columns.values)
matches_df = matches_df.set_index("Date")

home = matches_df[matches_df.Venue=="Home"]
away = matches_df[matches_df.Venue=="Away"]
print(home.shape, away.shape)
matches_wide_df = home.join(away,how="left",lsuffix="_home",rsuffix="_away")
matches_wide_df.to_csv("output/matches_wide.csv")