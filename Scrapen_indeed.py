import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import math


def ophalen_aantal_paginas(soup):
    """"Functie voor het ophalen van het aantal pagina's"""
    list = []

    # Webscrapen van de paginanummers op de laatste pagina.
    for div in soup.find_all(name='div', attrs={'class': 'pagination'}):
        for span in div.find_all(name='span', attrs={'class': 'pn'}):
            list.append(span.text.strip())
    list = [x for x in list if x.isdigit()]
    return int(list[-1])


def maken_url(trefwoord, plaats, radius):
    """"Functie voor het maken van een list met URL's die het langs moet gaan, de lengte wordt bepaald met de functie ophalen_aantal_paginas"""

    # URL voor het ophalen van aantal pagina's, standaard is pag. 100 zodat de laatste pagina weergeven kan worden.
    URL = 'https://www.indeed.nl/vacatures?as_and=' + trefwoord + '&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=' + radius + '&l=' + plaats + '&fromage=any&limit=10&sort=date&psf=advsrch&start=' + str(
        100000)

    # De pagina wordt opgehaald en met soup omgezet in text.
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Aanroepen functie voor de lengte van de zoekopdracht, returned een int.
    lengte = ophalen_aantal_paginas(soup)

    # Aanmaken lijst waar de URL's in geplaats gaan worden.
    list_url = []

    # Loopen door de lengte en steeds het paginanummer aan het eind aanpassen.
    for i in range(0, (lengte * 10), 10):
        URL = 'https://www.indeed.nl/vacatures?as_and=' + trefwoord + '&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=' + radius + '&l=' + plaats + '&fromage=any&limit=10&sort=date&psf=advsrch&start=' + str(
            i)
        list_url.append(URL)
    return list_url


def data_ophalen(list):
    """"Functie voor het ophalen van de vacatures"""
    jobs = []  # Aanmaken list waar de vacatures in gaan
    # Loopen door de list van URL's
    for i in range(len(list)):

        # De pagina wordt opgehaald en met soup omgezet in text.
        page = requests.get(list[i])
        soup = BeautifulSoup(page.text, 'html.parser')

        # Loopen door de text van soup naar elke div met de eigenschap class = row.
        for div in soup.find_all(name='div', attrs={'class': 'row'}):
            dict_vacature = {}  # Aanmaken dictionairy per vacature
            gesponsord = ''  # Aanmaken lege string om te kijken of het gesponsord is .

            # Loopen door elke html link binnen de div met de eigenschap data-tn-element = jobTitle.
            for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
                dict_vacature['Functie'] = str(a['title'])  # Ophalen functietitel en in dictionairy zetten.
                dict_vacature['URL'] = 'https://www.indeed.nl' + str(a['href'])

            # Loopen door elke div binnen de div met de eigenschap class = company.
            for b in div.find_all(name='span', attrs={'class': 'company'}):
                dict_vacature['Bedrijf'] = str(b.text.strip())  # Ophalen bedrijf en in dictionairy zetten.

            # Loopen door elke div binnen de div met de eigenschap class = result-link-bar.
            for c in div.find_all(name='div', attrs={'class': 'result-link-bar'}):
                # Loopen door elke span binnen de div met de eigenschap class = sponsoredGray.
                for d in c.find_all(name='span', attrs={'class': 'sponsoredGray'}):
                    gesponsord = d.text.strip().split(' ', 1)[0]  # String aanpassen

            # Als de string leeg is, is de vacature geen sponsor en wordt het toegevoegd aan de list, anders is het een gesponsorde vacature
            if gesponsord == '':
                jobs.append(dict_vacature)

    # Omzetten list met dictionairies in een dataframe
    df = pd.DataFrame(jobs)
    return df


def main():
    # Invoer variabelen
    trefwoord = 'ict'  # invoer trefwoord.
    plaats = 'Leiden'  # invoer plaatsnaam.
    radius = '0'  # invoer radius, 0 is alleen de plaatsnaam.

    # Ophalen list met URL's
    list_url = maken_url(trefwoord, plaats, radius)

    # Ophalen data in de vorm van een dataframe
    df_vacatures = data_ophalen(list_url)

    # Printen van de uitkomst.
    df_vacatures = df_vacatures.sort_values('Bedrijf')

    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.max.colwidth', 100)
    print(df_vacatures)


if __name__ == '__main__':
    main()

