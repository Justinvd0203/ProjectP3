import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import json
import ast
from selenium import webdriver
#
# pageno = 137
# page = requests.get('https://subsidieregister.zuid-holland.nl/api/subsidies?jaar=&programmakey=&doelstellingkey=&regelingkey=&pageno=' + str(pageno) + '&sortdir=desc&minaangevraagdbedrag=0&maxaangevraagdbedrag=5000000&minverleendbedrag=0&maxverleendbedrag=5000000&sortfield=jaar&aanvragernaam=')
#
# data = json.loads(page.text)
# data = data['results']
# print(data)
#
# data = str(data)
# df = pd.DataFrame(ast.literal_eval(data))
#
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_columns', 10)
# print(df)


page = requests.get('https://subsidieregister.zuid-holland.nl')
soup = BeautifulSoup(page.text, 'html.parser')
print(soup)




