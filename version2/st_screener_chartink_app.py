import numpy as np
import pandas as pd
import requests
import lxml
import streamlit as st
import json
from streamlit_lottie import st_lottie
from bs4 import BeautifulSoup as bs

url= "https://chartink.com/screener/process"

#header customization
st.markdown("""
<style>
	[data-testid="stHeader"] {
		background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));
	}
</style>""",
unsafe_allow_html=True)

# Title and header
st.title("Stock Screener App v2 📈")

def lottieurl_load(url: str):
    r= requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
    
lottie_img = lottieurl_load("https://lottie.host/b9c12781-35cd-4369-a17e-2f74f8147a23/vPpe1iW4uP.json")   
with st.columns(3)[1]:
    st_lottie(lottie_img,speed=1,reverse=False,loop=True,quality="high",height=250,width=250,key=None)

with requests.session() as s:
  raw_data= s.get(url)
  soup= bs(raw_data.content, "lxml")
  meta= soup.find("meta", {"name" : "csrf-token"}) #csrf-token is present in meta
  csrf_token=meta['content']


#copy Header key content  form website
header = {"X-Csrf-Token" : csrf_token}

# we need to pass conditions (Payload) in data
# condition = { "scan_clause" : "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) ) )" }
choice = st.radio(
    "Select any filter",
    ["No Filter", "OPEN EQUALS HIGH", "OPEN EQUALS LOW", "CLOSE EQUALS HIGH", "CLOSE EQUALS LOW", "OPEN EQUALS HIGH AND CLOSE EQUALS LOW", "OPEN EQUALS LOW AND CLOSE EQUALS HIGH" ],
    captions = ["No Filter", "OPEN EQUALS HIGH", "OPEN EQUALS LOW", "CLOSE EQUALS HIGH", "CLOSE EQUALS LOW", "OPEN EQUALS HIGH AND CLOSE EQUALS LOW", "OPEN EQUALS LOW AND CLOSE EQUALS HIGH" ])


condition={}

if choice== "No Filter":
  # we need to pass conditions (Payload) in data
  condition = {"scan_clause" : "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) ) )" }
elif choice== "OPEN EQUALS HIGH"
  condition = {"scan_clause" :"( {cash} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest open = latest high ) )"}
elif choice== "OPEN EQUALS LOW"
  condition = {"scan_clause": "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest open = latest low ) ) "}
elif choice== "CLOSE EQUALS HIGH"
  condition = {"scan_clause": "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest close = latest high ) )" }
elif choice== "CLOSE EQUALS LOW" 
  condition = {"scan_clause": "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest close = latest low ) ) "}
elif choice== "OPEN EQUALS HIGH AND CLOSE EQUALS LOW"
  condition = {"scan_clause": "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest open = latest high and latest close = latest low ) )"}
else: #OPEN EQUALS LOW AND CLOSE EQUALS HIGH
  condition= {"scan_clause": "( {57960} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest open = latest low and latest close = latest high ) )"}


# data will be returned in a JSON format
data = s.post(url, headers= header, data= condition).json() 


if st.button('Refresh'):
  data = s.post(url, headers= header, data= condition).json()
  # st.dataframe(data['data'])
else:
  pass
    
df=pd.DataFrame(data['data'])
df=df.drop('sr', axis=1)
st.dataframe(df)
# st.dataframe(data['data'])


st.markdown(":computer: _Made by Kirtan Tank_")
