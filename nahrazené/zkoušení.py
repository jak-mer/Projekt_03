"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Jakub Merta
email: merta.arch@gmail.com
"""
# KNIHOVNY:
from requests import get
from bs4 import BeautifulSoup
import csv 
import re
from pprint import pprint  

##########################################################################################
# ↓↓↓↓↓ ZÍSKÁNÍ DAT O VÝSLEDCÍCH VOLEB ZE VŠECH OBCÍ V JEDNOM OKRESE:
##########################################################################################

def ziskej_vysledky_obci(list_of_urls_obci):
    vysledky = []
    hlavicka = []
    
    for idx, adresa_obce in enumerate(list_of_urls_obci):
        try:
            print(f"Stahuji data pro obec: {adresa_obce}")
            odpoved_obec = get(adresa_obce)
            odpoved_obec.raise_for_status()
        except Exception as e:
            print(f"Chyba při stahování {adresa_obce}: {e}")
            continue

        rozdelene_html = BeautifulSoup(odpoved_obec.text, 'html.parser')

        nazev_obce_tag = rozdelene_html.find("h3", string=lambda t: t and t.strip().startswith("Obec:"))
        nazev_obce = nazev_obce_tag.text.replace("Obec:", "").strip() if nazev_obce_tag else "N/A"
        
        kod_obce_tag = rozdelene_html.find("td", {"headers": "sa1"})
        kod_obce = kod_obce_tag.text.strip().replace('\xa0', '') if kod_obce_tag else "N/A"

        volici_tag = rozdelene_html.find("td", {"headers": "sa2"})
        obalky_tag = rozdelene_html.find("td", {"headers": "sa5"})
        platne_tag = rozdelene_html.find("td", {"headers": "sa6"})

        volici = volici_tag.text.strip().replace('\xa0', '') if volici_tag else "N/A"
        obalky = obalky_tag.text.strip().replace('\xa0', '') if obalky_tag else "N/A"
        platne = platne_tag.text.strip().replace('\xa0', '') if platne_tag else "N/A"
        
        hlasy_stran = {}
        tabulka_hlasu = rozdelene_html.find("table", {"class": "table"}) 
        if tabulka_hlasu:
            for radek in tabulka_hlasu.find_all("tr"):
                nazev = radek.find("td", {"class": "overflow_name"})
                hlasy_tds = radek.find_all("td", {"class": "cislo"}) 
                
                if nazev and hlasy_tds:
                    hlasy_pro_stranu = ""
                    for td_hlasy in hlasy_tds:
                        if td_hlasy.get('headers') and td_hlasy.get('headers').startswith('t') and td_hlasy.get('headers').endswith('sa2'):
                            hlasy_pro_stranu = td_hlasy.text.strip().replace('\xa0', '')
                            break 
                    
                    if hlasy_pro_stranu:
                         hlasy_stran[nazev.text.strip()] = hlasy_pro_stranu
        
        if idx == 0:
            hlavicka = [
                "Kód obce",
                "Název obce",
                "Počet voličů",
                "Počet vydaných obálek",
                "Počet platných hlasů"
            ] + list(hlasy_stran.keys())
            print("Hlavička sestavena.")

        aktualni_radek_dat = [kod_obce, nazev_obce, volici, obalky, platne]
        for nazev_strany in hlavicka[5:]:
            aktualni_radek_dat.append(hlasy_stran.get(nazev_strany, "0"))
            
        vysledky.append(aktualni_radek_dat)
        print(f"Data obce '{nazev_obce}' přidána.")

    print("\nZískávání výsledků obcí dokončeno.")
    return vysledky, hlavicka


vysledky, hlavicka = (ziskej_vysledky_obci("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107"))

pprint(hlavicka)
pprint(vysledky)