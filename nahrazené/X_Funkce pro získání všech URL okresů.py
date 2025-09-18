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
# ↓↓↓↓↓ ZÍSKÁNÍ URL VŠECH OKRESŮ V ČR DO SLOVNÍKU:
##########################################################################################
"""
VÝSTUP:
'CZ0206': 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106',
'CZ0207': 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107',
 """

def ziskej_kompletni_url_okresu():
    URL = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    odpoved = get(URL)
    rozdelene_html = BeautifulSoup(odpoved.text, 'html.parser')
    nalezene_tagy = rozdelene_html.find_all("a", href=lambda h: h and h.startswith("ps32"), string="X")
    list_href_values = [tag['href'] for tag in nalezene_tagy]
    base_url_prefix = "https://www.volby.cz/pls/ps2017nss/"
    kompletni_url_adresy = [base_url_prefix + fragment for fragment in list_href_values]
    return kompletni_url_adresy

# Vypsání výsledku
# pprint(ziskej_kompletni_url_okresu())


def vytvor_seznam_kodu_vsech_okresu():
    URL = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    odpoved = get(URL)
    rozdelene_html = BeautifulSoup(odpoved.text, 'html.parser')
    nalezene_tagy_s_kodem = rozdelene_html.find_all("a", href=re.compile(r"^ps311"), string=lambda text: text and len(text.strip()) == 6)
    district_codes = [tag.get_text(strip=True) for tag in nalezene_tagy_s_kodem]
    return district_codes

# Vypsání výsledku
# pprint(vytvor_seznam_kodu_vsech_okresu())


def spoj_okresni_data_do_slovniku():
    list_kodu = vytvor_seznam_kodu_vsech_okresu()
    list_url = ziskej_kompletni_url_okresu()
    spojeny_slovnik = dict(zip(list_kodu, list_url))
    return spojeny_slovnik

pprint(spoj_okresni_data_do_slovniku())
pprint(type(spoj_okresni_data_do_slovniku()))


##############################################################################
# ↓↓↓↓↓ VÝBĚR OKRESU UŽIVATELEM:
##############################################################################

def vyber_adresu_okresu(data_slovnik):
    while True:
        user_input = input("\nZadejte kód, pro který chcete získat URL (nebo 'konec' pro ukončení): ").strip().upper()

        if user_input == 'KONEC':
            return None
        
        if user_input in data_slovnik:
            return data_slovnik[user_input]
        else:
            print(f"Chyba: Kód '{user_input}' nebyl nalezen. Zkuste to prosím znovu.")

print(vyber_adresu_okresu(spoj_okresni_data_do_slovniku()))