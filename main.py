import requests
from tkinter import *
import sqlite3
import mysql.connector

switch = 1


# installer certaine library via : pip install <library>

# switch de table
def switchTable():
    global switch
    switch *= -1
    refresh()


# créer le lien en fonction de la ville passé en paramètre
def api_weather(ville):
    api_url1 = "http://api.openweathermap.org/data/2.5/weather?q="
    api_url2 = ",fr&lang=fr&units=metric&APPID=20732b663eb6d3ee95e868da30aa8b43"
    url = api_url1 + ville + api_url2
    return url


# Donne toute les info de la ville grace a l'api openweather
def weather_info(ville):
    url = api_weather(ville)
    api_status = requests.get(url)
    if api_status.status_code == 200:
        data = api_status.json()
        max = data["main"]["temp_max"]
        min = data["main"]["temp_min"]
        lon = data["coord"]["lon"]
        lat = data["coord"]["lat"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        celsius = data["main"]["temp"]
        fahrenheit = celsius * 9 / 5 + 32
        winds = data["wind"]["speed"]
        weather_liste = [str(pressure), str(humidity), str(celsius),
                         str(fahrenheit), str(winds), str(max), str(min), str(lon), str(lat)]
        return weather_liste


# recupere les info en fonction du nom
def recup_data(name):
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="cabouhna")
    cur = conn.cursor()
    cur.execute("SELECT * FROM etudiants")
    resultats = cur.fetchall()
    list_of_data = ["NULL", "NULL", "NULL", "NULL", 0, 0]
    for resultat in resultats:
        if resultat[1] == name:
            list_of_data = [resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[0]]
    cur.close()
    conn.close()
    return list_of_data


# recupere les info en fonction du nom (table etudiants)
def recup_data2(name):
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="cabouhna")
    cur = conn.cursor()
    cur.execute("SELECT * FROM adresses")
    resultats = cur.fetchall()
    list_of_data = ["NULL", "NULL"]
    for resultat in resultats:
        if resultat[0] == name:
            list_of_data = [resultat[0], resultat[1]]
    cur.close()
    conn.close()
    return list_of_data


# lorsqu'un nom correspond il envoie les données de la pression dans la base de donnée
def EnvoiDePression(liste_info):
    # a changer pour le server
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="cabouhna")
    cur = conn.cursor()
    ligne_weather = weather_info(liste_info[2])
    id = liste_info[5]
    pressure = int(ligne_weather[0])
    lol = "UPDATE etudiants SET pression = " + str(pressure) + " WHERE id = " + str(id)
    cur.execute(lol)
    conn.commit()
    cur.close()
    conn.close()


# si on vas dans fichier puis refresh on fait disparaite tous le texte
def refresh():
    name.config(text="")
    lastName.config(text="")
    ville1.config(text="")
    ville2.config(text="")
    pressure.config(text="")
    humidity.config(text="")
    celsius.config(text="")
    fahrenheit.config(text="")
    wind.config(text="")
    max.config(text="")
    min.config(text="")
    lon.config(text="")
    lat.config(text="")
    status.config(text="Status : No information")


# si on ne trouve pas le nom écrit on fait disparaite tout le texte
def error():
    name.config(text="")
    lastName.config(text="")
    ville1.config(text="")
    ville2.config(text="")
    pressure.config(text="")
    humidity.config(text="")
    celsius.config(text="")
    fahrenheit.config(text="")
    wind.config(text="")
    max.config(text="")
    min.config(text="")
    lon.config(text="")
    lat.config(text="")
    status.config(text="Status : Information not found")


# affiche toutes les informations grace a la base de donner et les données de l'api lorsqu'un nom correspond
def afficher_mot(event):
    mot = Entree.get()
    if switch == -1:
        afficher_mot2(mot)
    else:
        liste = recup_data(mot)
        if liste[0] != "NULL":
            name.config(text="Name : " + liste[0])
            lastName.config(text="LastName : " + liste[1])
            ville1.config(text="City n°1 : " + liste[2])
            if liste[3] != "//":
                ville2.config(text="City n°2 : " + liste[3])
            else:
                ville2.config(text="City n°2 : Undefined")
            ville = liste[2]
            weatherListe = weather_info(ville)
            pressure.config(text="Pressure : " + weatherListe[0] + " hPa")
            humidity.config(text="Humidity : " + weatherListe[1])
            celsius.config(text="Celsius : " + weatherListe[2] + " °C")
            fahrenheit.config(text="Fahrenheit : " + weatherListe[3] + " °F")
            wind.config(text="Wind : " + weatherListe[4])
            max.config(text="Max : " + weatherListe[5])
            min.config(text="Min : " + weatherListe[6])
            lon.config(text="Lon : " + weatherListe[7])
            lat.config(text="Lat : " + weatherListe[8])
            status.config(text="Status : Information detected")
            EnvoiDePression(liste)
        else:
            error()


def afficher_mot2(mot):
    liste = recup_data2(mot)
    if liste[0] != "NULL":
        name.config(text="Name : " + liste[0])
        lastName.config(text="Adresse : " + liste[1])
        status.config(text="Status : Information detected")
    else:
        error()


# Tkinter start
fenetre = Tk()
fenetre.title("Data Weather")
fenetre.geometry("480x680")
fenetre.wm_minsize(480, 680)
fenetre.iconbitmap("sun.ico")
fenetre.config(background='#817AD8')

# Menu
menu = Menu(fenetre)
file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label="Refresh", command=refresh)
file_menu.add_command(label="Table switch", command=switchTable)
file_menu.add_command(label="Quitter", command=fenetre.quit)
menu.add_cascade(label="Fichier", menu=file_menu)
fenetre.config(menu=menu)

frame = Frame(fenetre, bg='#9A95DC', bd=1, relief=SUNKEN)

# title
title = Label(frame, background='#9A95DC', text="Enter a name", font=('TISA', 22))
title.pack(expand=YES)

Entree = Entry(frame, font=('TISA', 20))
Entree.pack(side=TOP)
Entree.bind("<Return>", afficher_mot)

frame2 = Frame(fenetre, bg='#817AD8', bd=0, relief=SUNKEN)
frame2.pack(side=BOTTOM)

# info : Nom

name = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
name.pack(side=TOP, expand=YES)

lastName = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
lastName.pack(side=TOP, expand=YES)

ville1 = Label(frame2, background='#817AD8', text="", font=('Helvetica', 25))
ville1.pack(side=TOP, expand=YES)

pressure = Label(frame2, background='#817AD8', text="", font=('Helvetica', 30))
pressure.pack(side=TOP, expand=YES)

ville2 = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
ville2.pack(side=TOP, expand=YES)

humidity = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
humidity.pack(side=TOP, expand=YES)

celsius = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
celsius.pack(side=TOP, expand=YES)

fahrenheit = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
fahrenheit.pack(side=TOP, expand=YES)

lon = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
lon.pack(side=TOP, expand=YES)

lat = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
lat.pack(side=TOP, expand=YES)

max = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
max.pack(side=TOP, expand=YES)

min = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
min.pack(side=TOP, expand=YES)

wind = Label(frame2, background='#817AD8', text="", font=('Helvetica', 17))
wind.pack(side=TOP, expand=YES)

frame3 = Frame(fenetre, bg='#9A95DC', bd=0.5, relief=SUNKEN)

status = Label(frame3, background='#9A95DC', text="Status : No information", font=('Helvetica', 20))
status.pack(side=BOTTOM, expand=YES)

frame.pack(expand=YES)
frame2.pack(expand=YES)
frame3.pack(expand=NO)

# Lancer la boucle principale pour afficher la fenêtre
fenetre.mainloop()

