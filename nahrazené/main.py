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

def ziskej_vysledky_obci(URL):
    vysledky = []
    hlavicka = []
    for idx, adresa_obce in enumerate(cela_adresa_obce_list):
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

##########################################################################################
# ↓↓↓↓↓ ZÍSKÁNÍ URL VŠECH OBCÍ V JEDNOM OKRESE
##########################################################################################
"""
Funkce získá seznam URL adres všech obcí v jednom okrese do proměnné "cela_adresa_obce_list".
Tato funkce přijímá jako argument URL adresu okresu.
"""

def ziskej_adresy_obci_v_okrese(URL):
    odpoved_okres = get(URL)
    rozdelene_html_okres = BeautifulSoup(odpoved_okres.text, 'html.parser')
    url_obce = rozdelene_html_okres.find_all("a", href=lambda h: h and "ps311" in h)
    obec_odkazy = [odkaz for odkaz in url_obce if odkaz.text.strip() != "X"]
    cela_adresa_obce_list = [
        "https://www.volby.cz/pls/ps2017nss/" + odkaz["href"]
        for odkaz in obec_odkazy
    ]
    return cela_adresa_obce_list


"""
# Tisk všech adres obcí v daném okrese:
pprint(cela_adresa_obce_list)
print(type(cela_adresa_obce_list))
"""
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

##############################################################################
# ↓↓↓↓↓↓↓↓↓↓ ZÍSKÁNÍ NÁZVU SOUBORU:
##############################################################################

def ziskej_nazev_souboru():
    nazev_souboru = "vysledky_obce.csv"
    return nazev_souboru

"""
def ziskej_nazev_souboru():
    csv_kod_okresu = vyber_adresu_okresu # ← volání funkce pro výběr okresu
    nazev_souboru = f"vysledky_obce_{csv_kod_okresu}.csv"
    print(f"Výsledky budou uloženy do souboru: {nazev_souboru}")
    return nazev_souboru
"""

##############################################################################
# ↓↓↓↓↓↓↓↓↓↓ ULOŽENÍ VÝSLEDKŮ DO CSV SOUBORU:
##############################################################################

def uloz_vysledky_do_csv(hlavicka, vysledky, nazev_souboru):
    with open(nazev_souboru, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(hlavicka)
        for radek in vysledky:
            writer.writerow(radek)

##############################################################################
# ↓↓↓↓↓↓↓↓↓↓ VOLÁNÍ HLAVNÍ FUNKCE:
##############################################################################

if __name__ == "__main__":

# VOLÁNÍ DÍLČÍCH FUNKCÍ A UKLÁDANÍ DO PROMĚNNÝCH:

# 01 Proměnná, kde mám všechny URL okresů ve slovníku, kde klíč je kód okresu a hodnota je URL adresa:
    ziskane_URL_okresu = spoj_okresni_data_do_slovniku() # ← volání funkce pro získání URL všech okresů + uložení do proměnné (slovník)
    """UKÁZKA DAT V PROMĚNNÉ:
        'CZ0206': 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106',
        'CZ0207': 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107',
        ..... """

# 02 Proměnná, kde mám jednu URL adresu okresu ve stringu, kterou si vybral uživatel:
    vybrana_URL_jednoho_okresu = vyber_adresu_okresu(ziskane_URL_okresu) # ← volání funkce pro výběr okresu + uložení do proměnné ()
    """ UKÁZKA DAT V PROMĚNNÉ: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107"""


# 03 Proměnná, kde mám seznam URL adres všech obcí v jednom okrese, podle toho co si vybral uživatel za okres:
    cela_adresa_obce_list = ziskej_adresy_obci_v_okrese(vybrana_URL_jednoho_okresu) # ← volání funkce pro získání URL všech obcí v jednom okrese + uložení do proměnné (list)
    """ UKÁZKA DAT V PROMĚNNÉ: 
    ['https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=13&xobec=588300&xvyber=7201',
    'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=13&xobec=588326&xvyber=7201',
    'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=13&xobec=542318&xvyber=7201',
    'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=13&xobec=549690&xvyber=7201',
    'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=13&xobec=588377&xvyber=7201',
    ......."""

# 04 Proměnná, kde mám název CSV souboru, do kterého se budou ukládat výsledky:
    nazev_csv_souboru = ziskej_nazev_souboru() # ← NEMÁM OVĚŘENO, ŽE MI TO BUDE FUNGOVAT!!

# 05 Proměnná, kde mám data pro uložení do CSV souboru:
    vysledky, hlavicka = ziskej_vysledky_obci(cela_adresa_obce_list)

# 06 Volání funkce, která ukládá výsledky do CSV souboru:
    uloz_vysledky_do_csv(vysledky, hlavicka, nazev_csv_souboru)


# ZKUŠEBNÍ PRINTY FUNKCE:

# pprint(ziskane_URL_okresu)
# print(vybrana_URL_jednoho_okresu)
# pprint(cela_adresa_obce_list)
# print(nazev_csv_souboru)



"""

    uloz_vysledky_do_csv(csv_hlavicka, csv_vysledky, ziskej_nazev_souboru)
    # ↑ Volání první funkce "uloz_vysledky_do_csv", která volá funkci "ziskej_nazev_souboru"

"""
