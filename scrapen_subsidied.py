import requests
import pandas as pd
import json
import ast
from requests_html import HTMLSession


def ophalen_subsidies(max):
    list = []
    for pagina in range(1, max + 1):
        page = requests.get('https://subsidieregister.zuid-holland.nl/api/subsidies?jaar=&programmakey=&doelstellingkey=&regelingkey=&pageno=' + str(pagina) + '&sortdir=desc&minaangevraagdbedrag=0&maxaangevraagdbedrag=5000000&minverleendbedrag=0&maxverleendbedrag=5000000&sortfield=jaar&aanvragernaam=')
        data = json.loads(page.text)
        data = str(data['results'])
        list.append(data)
        print(pagina)
        print(data)
    for i in range(0, len(list)):
        if i == 0:
            df = pd.DataFrame(ast.literal_eval(list[i]))
        else:
            df2 = pd.DataFrame(ast.literal_eval(list[i]))
            df = pd.concat([df, df2])

    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 10)
    print(df)


def ophalen_max_paginas(url):
    session = HTMLSession()
    page = session.get(url)
    page.html.render(sleep = 10)
    a = page.html.find('th.paging6')
    max_page = int(a[0].text)
    return max_page

def main():
    url = 'https://subsidieregister.zuid-holland.nl'
    max_paginas = ophalen_max_paginas(url)
    ophalen_subsidies(max_paginas)

if __name__ == '__main__':
    main()




