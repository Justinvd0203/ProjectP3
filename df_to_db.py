import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from pandas.io import sql
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# Functie voor het overzetten van een dataframe in een mysql database
def csv_naar_sql(df, naam, gebruiker, wachtwoord, database, host):
    # creeren naam uit path location
    naam = naam.split('.')
    naam = str(naam[0])
    naam = naam.split('/')
    naam = str(naam[-1])

    #verbinden met de database en dit vervolgens met df.to_sql het df in de database zetten
    connector = 'mysql+mysqlconnector://' + gebruiker + ':' + wachtwoord + '@' + host + '/' + database
    engine = create_engine(str(connector))
    con = engine.connect()
    df.to_sql(con=con, name=naam)

    #nogmaals verbinden met een raw connection om te kijken of het overzetten gelukt is
    connection = engine.raw_connection()
    cursor = connection.cursor()

    #select statement om te kijken of de database bestaat, bij een error bestaat hij niet en returned False.
    try:
        cursor.execute('SELECT 1 FROM ' + naam + ' LIMIT 1;')
        result = cursor.fetchone()
        if result[0] == 1:
            return True
    except mysql.connector.errors.ProgrammingError as e:
        return False


def tkinter():
    # functie die aangeroepen wordt door de button
    def overzetten():
        # gebruiker laten kiezen welke file hij/zij wilt overzetten en dit vervolgens als een pandas dataframe openen
        root.filename = filedialog.askopenfilename(initialdir='/', title='Kies een csv bestand',
                                                   filetypes=(('csv files', '*.csv'), ('alle files', '*.*')))
        df = pd.read_csv(str(root.filename))

        #Opslaan input van de gebruiker
        gebruiker = str(entrygebruiker.get())
        wachtwoord = str(entrywachtwoord.get())
        database = str(entrydatabase.get())
        host = str(entryhost.get())

        # uitvoeren methode csv_naar_sql wat een boolean returnes. Als deze boolean True is dan is het gelukt,
        # anders niet gelukt. Dit wordt ook weergeven in een messagebox
        gelukt = csv_naar_sql(df, root.filename, gebruiker, wachtwoord, database, host)
        if gelukt == True:
            tk.messagebox.showinfo('Succes', 'De data is met succes overgezt in de database')
        elif gelukt == False:
            tk.messagebox.showinfo('Niet gelukt', 'De data is niet succesvol overgezet in de database')

    #aanmaken hoofdscherm tkinter
    root = tk.Tk()
    root.config(background='white')
    root.title('Smart071 Groep4 csv to SQLDB')

    canvashoofd = tk.Canvas(root, width=800, height=600, background='white', borderwidth=0, highlightthickness=0)
    canvashoofd.pack()

    #aanmaken titel op hoofdcanvas
    titel = tk.Label(text='SMART071', background='white', font=('Courier bold', 44), fg='sky blue')
    canvashoofd.create_window(400, 100, window=titel)

    #aanmaken invoer gebruiker
    labelgebruiker = tk.Label(text='Gebruiker:', background='white', font=('Courier', 20))
    canvashoofd.create_window(200, 200, window=labelgebruiker)
    entrygebruiker = tk.Entry(root, font=('Courier', 15))
    canvashoofd.create_window(450, 200, window=entrygebruiker)

    #aanmaken invoer wachtwoord
    labelwachtwoord = tk.Label(text='Wachtwoord:', background='white', font=('Courier', 20))
    canvashoofd.create_window(200, 275, window=labelwachtwoord)
    entrywachtwoord = tk.Entry(root, font=('Courier', 15), show='*')
    canvashoofd.create_window(450, 275, window=entrywachtwoord)

    #aanmaken invoer database
    labeldatabase = tk.Label(text='Database:', background='white', font=('Courier', 20))
    canvashoofd.create_window(200, 350, window=labeldatabase)
    entrydatabase = tk.Entry(root, font=('Courier', 15))
    canvashoofd.create_window(450, 350, window=entrydatabase)

    #aanmaken invoer host
    labelhost = tk.Label(text='Host:', background='white', font=('Courier', 20))
    canvashoofd.create_window(200, 425, window=labelhost)
    entryhost = tk.Entry(root, font=('Courier', 15))
    canvashoofd.create_window(450, 425, window=entryhost)

    #invoegen afbeelding hsleiden
    imgHSL = PhotoImage(file='Afbeeldingen/hsleiden.png')
    imgHSL = imgHSL.subsample(2)
    labelimgHSL = tk.Label(root, image=imgHSL, borderwidth=0)
    canvashoofd.create_window(700, 525, window=labelimgHSL)

    #aanmake button die de functie overzetten aanroept
    button = tk.Button(root, text='Overzetten', command=overzetten, bg='sky blue', bd=2.5, font=('Courier', 15))
    canvashoofd.create_window(400, 500, window=button)

    root.mainloop()


if __name__ == '__main__':
    tkinter()
