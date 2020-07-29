import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import  csv

colonnes = ["ville", "lien"]

tableau = DataFrame(columns=colonnes)
tableau.to_csv("dataset\\liensVilles.csv", index=False)

dico = {}
dico["ville"] = ""
dico["lien"] = ""

url = "http://www.journaldunet.com/management/ville/index/villes?page="

with open("dataset\\liensVilles.csv", "a", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=colonnes, lineterminator="\n")
    for numeroPage in range(1, 700):
        print(numeroPage)
        req = requests.get(url + str(numeroPage))
        contenu = req.content
        soup = bs(contenu, "html.parser")

        touslesliens = soup.findAll("a")

        for lien in touslesliens:
            if ("/ville-" in lien["href"]) and ('/management/' in lien['href']):
                dico["lien"] = lien["href"]
                dico["ville"] = lien.text

                writer.writerow(dico)