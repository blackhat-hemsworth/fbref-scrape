import pandas as pd
import requests
import bs4 
from io import StringIO

url = 'https://fbref.com/en/comps/9/passing/Premier-League-Stats'
base_url = 'https://fbref.com'

html = requests.get(url)
with open('checking.html', 'wb+') as f:
    f.write(html.content)


bs_obj = bs4.BeautifulSoup(html.text,"lxml")
i = 0
for comment in bs_obj.findAll(string=lambda string:isinstance(string, bs4.Comment)):
    c_soup = bs4.BeautifulSoup(comment,"lxml")
    for table in c_soup.findAll("table"):
        df = pd.read_html(StringIO(str(table)),extract_links ="all")[0].apply(lambda col: [base_url + v[1] if v[1] else v[0] for v in  col])
        i+=1
        df.to_csv("df"+str(i)+".csv")

tables = bs_obj.findAll("table") 
for table in tables:
    df = pd.read_html(StringIO(str(table)))[0]
    i+=1
    df.to_csv("df"+str(i)+".csv")



quit()

bs_obj = bs4.BeautifulSoup(html.text,"lxml")
tables = bs_obj.findAll('table') 
for table in tables:
    df = pd.read_html(StringIO(str(table)))
    print(df)


quit()

list_of_dfs = list()
for n in range(1,68):
    for ab in ['A','B']:
        url = f'https://electionresults.sos.mn.gov/results/Index?ErsElectionId=162&scenario=StateRepresentativePnp&DistrictCode={n}{ab}&show=Go'
        print(url)
        html = requests.get(url)
        bs_obj = bs4.BeautifulSoup(html.text,"lxml")
        tables = bs_obj.findAll('table') 
        for table in tables:
            df = pd.read_html(StringIO(str(table)))
            if len(df) != 0 and 'Democratic-Farmer-Labor' in df[0].columns: 
                df[0]["District"] = str(n)+ab
                list_of_dfs.append(df[0]) 

print(list_of_dfs)

main_df = pd.concat(list_of_dfs)
print(main_df)

main_df.to_csv("election-results.csv")