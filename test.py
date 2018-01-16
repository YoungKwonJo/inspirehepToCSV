from urllib.request import Request, urlopen
#from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

#url='http://inspirehep.net/search?ln=en&ln=en&p=find+j+%22Phys.Rev.Lett.%2C105*%22&of=xe&action_search=Search&sf=&so=d&rm=&rg=25&sc=0'
url='http://inspirehep.net/search?ln=en&ln=en&p=find+jy+2000+and+tc+p+and+cc+KR&of=xe&action_search=Search&sf=&so=d&rm=&rg=25&sc=0'
xmltext = urlopen(url).read()

root = ET.fromstring(xmltext)
rows =[]
for i in root.findall("records"):
    for j in i.findall("record"):
        row = {}
        for k in j.findall("contributors"):
            for l in k.findall("authors"):
                row["authors"]=""
                for m in l.findall("author"):
                    row["authors"] += m.text+";"
        for k in j.findall("titles"):
            for l in k.findall("title"):
                row["title"]=l.text
            for l in k.findall("secondary-title"):
                row["secondary-title"]=l.text
        for k in j.findall("pages"):
            row["pages"]=k.text
        for k in j.findall("volume"):
            row["volume"]=k.text
        for k in j.findall("abstract"):
            row["abstract"]=k.text
        rows.append( row ) 

import pandas as pd
df = pd.DataFrame(rows)

print(len(df))
df.to_csv("output.csv")
