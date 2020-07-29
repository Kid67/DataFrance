import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import csv
import os
import time

# Liste des colonnes du dictionnaire

colonnes = ['ville', 'lien', "Code Insee", "Région", "Département",
            "Etablissement public de coopération intercommunale (EPCI)",
            "Code postal (CP)", "Nom des habitants", "Population (2017)",
            "Population : rang national (2017)", "Densité de population (2017)", "Taux de chômage (2017)",
            "Pavillon bleu", "Ville d'art et d'histoire", "Ville fleurie", "Ville internet", "Superficie (surface)",
            "Altitude min.", "Altitude max.", "Latitude", "Longitude"]

#fonction pour faire la differnce entre les liens scrapes et non scrapes

def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))

if os.path.isfile("dataset\\infos.csv"):
    tableauInfos = pd.read_csv("dataset\\infos.csv", error_bad_lines=False, dtype="unicode")
    colonnes1 = tableauInfos["lien"]
    tableauLiens = pd.read_csv("dataset\\liensVilles.csv")
    colonnes2 = tableauLiens["lien"]
    listeLiens = diff(colonnes1, colonnes2)
else:
    #création du csv info. On crée d'abord tableauinfo sous forme de dataframme avec les colomns de colonnes

    tableauInfos = DataFrame(columns=colonnes)

# on convertit le tableau en csv

    tableauInfos.to_csv("dataset\\infos.csv", index=False)  
# je recupere la liste des lien à scraper
    tableauLiens = pd.read_csv("dataset\\liensVilles.csv")
    listeLiens = tableauLiens["lien"] 

listeLiens = [lien for lien in listeLiens if lien[:11] == "/management"]

#initialisation du dictionnaire avec la liste de "colonnes"

dico = {i: "" for i in colonnes}



def parse(lien):
    #initialisation du dictionnaire avec la liste de "colonnes"

    dico = {i: "" for i in colonnes}
    req = requests.get("http://www.journaldunet.com" + lien)
    time.sleep(2)
    if req.status_code == 200:
        with open("dataset\\infos.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=colonnes, lineterminator="\n")
            contenu = req.content
            soup = bs(contenu, "html.parser")

            dico["lien"] = lien
            dico["ville"] = tableauLiens[tableauLiens["lien"] == lien]["ville"].iloc[0]

            tables = soup.findAll("table", class_="odTable odTableAuto")

            for i in range(len(tables)):
                toutLesTr = tables[i].findAll("tr")
                for tr in toutLesTr[1:]:
                    cle = tr.findAll('td')[0].text
                    valeur = tr.findAll('td')[1].text

                    if "Nom des habitants" in cle:
                        dico["Nom des habitants"] = valeur
                    elif "Taux de chômage" in cle:
                        dico["Taux de chômage (2017)"] = valeur
                    else:
                        dico[cle] = valeur
            writer.writerow(dico)
            print(lien)

if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, listeLiens)