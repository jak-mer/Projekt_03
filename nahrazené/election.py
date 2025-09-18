"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Jakub Merta
email: merta.arch@gmail.com
"""

############################################ KNIHOVNY:

from requests import get
from bs4 import BeautifulSoup
import csv 
import re
import sys

##########################################################################################
# ↓↓↓↓↓ FUNKCE, KTERÁ ZÍSKÁ URL VŠECH OBCÍ V JEDNOM OKRESE:
##########################################################################################

def ziskej_adresy_obci_v_okrese(URL):
    odpoved_okres = get(URL)
    rozdelene_html_okres = BeautifulSoup(odpoved_okres.text, 'html.parser')
    url_obce = rozdelene_html_okres.find_all("a", href=lambda h: h and "ps311" in h)
    obec_odkazy = [odkaz for odkaz in url_obce if odkaz.text.strip() != "X"]
    url_vsech_obci = [
        "https://www.volby.cz/pls/ps2017nss/" + odkaz["href"]
        for odkaz in obec_odkazy
    ]
    return url_vsech_obci

##########################################################################################
# ↓↓↓↓↓ FUNKCE, KTERÁ ZÍSKÁ DATA O VÝSLEDCÍCH VOLEB ZE VŠECH OBCÍ V JEDNOM OKRESE:
##########################################################################################

def ziskej_vysledky_obci(URL):
    vysledky = []
    hlavicka = []
    for idx, adresa_obce in enumerate(URL):
        odpoved_obec = get(adresa_obce)
        rozdelene_html = BeautifulSoup(odpoved_obec.text, 'html.parser')

        # Název obce
        nazev_obce = rozdelene_html.find("h3", string=lambda t: t and t.strip().startswith("Obec:")).text.replace("Obec:", "").strip()
        # Kód obce
        odkaz = rozdelene_html.find("a", href=lambda h: h and "ps311" in h)
        kod_obce = ""
        if odkaz:
            match = re.search(r"xobec=(\d{6})", odkaz["href"])
            if match:
                kod_obce = match.group(1)
        # Počet voličů, obálek, platných hlasů
        volici = rozdelene_html.find("td", {"headers": "sa2"}).text.strip().replace('\xa0', '')
        obalky = rozdelene_html.find("td", {"headers": "sa5"}).text.strip().replace('\xa0', '')
        platne = rozdelene_html.find("td", {"headers": "sa6"}).text.strip().replace('\xa0', '')
        # Hlasy pro každou stranu
        hlasy_stran = {}
        for radek in rozdelene_html.find_all("tr"):
            nazev = radek.find("td", {"class": "overflow_name"})
            hlasy = radek.find("td", {"headers": lambda x: x and x.startswith("t") and x.endswith("sa2")})
            if nazev and hlasy:
                hlasy_stran[nazev.text.strip()] = hlasy.text.strip().replace('\xa0', '')

        # Sestavení hlavičky pouze z první obce
        if idx == 0:
            hlavicka = [
                "Kód obce",
                "Název obce",
                "Počet voličů",
                "Počet obálek",
                "Počet platných hlasů"
            ] + list(hlasy_stran.keys())

        # Uložení výsledků do seznamu
        vysledky.append([kod_obce, nazev_obce, volici, obalky, platne] + list(hlasy_stran.values()))
    return vysledky, hlavicka

##############################################################################
# ↓↓↓↓↓↓↓↓↓↓ FUNKCE, KTERÁ ULOŽÍ VÝSLEDKY DO CSV SOUBORU:
##############################################################################

def uloz_vysledky_do_csv(hlavicka, vysledky, nazev_souboru):
    with open(nazev_souboru, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(hlavicka)
        for radek in vysledky:
            writer.writerow(radek)

##############################################################################
# ↓↓↓↓↓↓↓↓↓↓ HLAVNÍ FUNKCE:
##############################################################################

def hlavni_funkce(adresa_okresu, ziskej_nazev_souboru):
        print("STAHUJI DATA Z VYBRANÉHO URL")
        cela_adresa_obce_list = ziskej_adresy_obci_v_okrese(adresa_okresu)
        vysledky, hlavicka = ziskej_vysledky_obci(cela_adresa_obce_list)
        print("UKLADAM DATA DO CSV SOUBORU")
        uloz_vysledky_do_csv(hlavicka, vysledky, ziskej_nazev_souboru)
        print("UKONCUJI PROGRAM")


##############################################################################
# ↓↓↓↓↓↓↓↓↓↓ VOLÁNÍ PROGRAMU:
##############################################################################

if __name__ == "__main__":
    adresa_okresu = sys.argv[1]
    ziskej_nazev_souboru = sys.argv[2]
    hlavni_funkce(adresa_okresu, ziskej_nazev_souboru)


# 1.argument: URL Kraje: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107
# 2.argument: Název souboru: vysledky_obce.csv

# STAHUJI DATA Z VYBRANEHO URL:
# UKLADAM DATA DO CSV SOUBORU:
# UKONČUJI PROGRAM: 


# Příkaz pro spuštění programu:
# python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3103" "vysledky_obce.csv"