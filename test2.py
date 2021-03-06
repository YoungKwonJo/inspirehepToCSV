import requests
import urllib
from bs4 import BeautifulSoup

result = []
req = requests.get('http://inspirehep.net/search?ln=en&ln=en&p=find+jy+1967+and+tc+p&of=hb&action_search=Search&sf=earliestdate&so=d&rm=&rg=250&sc=0')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
records = soup.findAll("div", {"class": "record_body"})
output=[]
#data = records.findAll("small")
for record in records:
    row = {}
    title = record.find("a", {"class":"titlelink"})
    row['titlelink']=title['href']
    row['title']=title.text
    published = record.find("b")
    row['published']=published.text
    authors = record.findAll("a",{"class":"authorlink"})
    #저자수는 10명이 넘지 않는 경우 가정
    for i in range(10):
        row['authorlink_'+str(i)] = ""
        row['author_'+str(i)] = ""  
    
    for i,author in enumerate(authors):
        row['authorlink_'+str(i)] = "inspirehep.net"+urllib.parse.unquote(author['href'])
        row['author_'+str(i)] =author.text
        if i>9: break

    #기관은 4개가 넘지 않는 경우 가정
    for i in range(4):
        row['afflink_'+str(i)] = ""
        row['aff_'+str(i)] = ""      
    afflinks = record.findAll("a",{"class":"afflink"})
    for i,afflink in enumerate(afflinks):
        row['afflink_'+str(i)] = "inspirehep.net"+urllib.parse.unquote(afflink['href'])
        row['aff_'+str(i)] =afflink.text
        if i>3: break

    a4doi = record.findAll("a")
    for i in a4doi:
        if "dx.doi.org" in i['href']:
            row['doi']=i['href']
    
    output.append(row)
import pandas as pd
df = pd.DataFrame(output)

print(df)
df.to_csv("output.csv")


