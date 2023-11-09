

import numpy as np
import pandas as pd
import requests

#pip install beautifulsoup4

from bs4 import BeautifulSoup as bs

url= "https://chartink.com/screener/process"

"""with requests.session() as s:
  raw_data= s.get(url)
  print(raw_data)

response 200 means it's working

with requests.session() as s:
  raw_data= s.get(url)
  print(raw_data.text)
"""



"""to extract data from html we need bs4

with requests.session() as s:
  raw_data= s.get(url)
  soup= bs(raw_data.content, "lxml")
  meta= soup.find_all("meta", {"name" : "csrf-token"}) #csrf-token is present in meta
  print(meta)
"""

with requests.session() as s:
  raw_data= s.get(url)
  soup= bs(raw_data.content, "lxml")
  meta= soup.find("meta", {"name" : "csrf-token"}) #csrf-token is present in meta
  csrf_token=meta['content']

csrf_token

#copy Header key content  form website
header = {"X-Csrf-Token" : csrf_token}

# we need to pass conditions (Payload) in data
condition = { "scan_clause" : "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) ) )" }

# data will be returned in a JSON format
data = s.post(url, headers= header, data= condition).json()
print(data)

data.keys()

pd.DataFrame(data['data'])







