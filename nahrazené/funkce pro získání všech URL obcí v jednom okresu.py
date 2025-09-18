
# KNIHOVNY:
from requests import get
from bs4 import BeautifulSoup
import csv 
import re
from pprint import pprint  


##########################################################################################
# ZÍSKÁNÍ URL VŠECH OBCÍ V JEDNOM OKRESE
##########################################################################################

# Argument funkce:
adresa_okresu = 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'

def ziskej_adresy_obci_v_okrese(adresa_okresu):
    odpoved_okres = get(adresa_okresu)
    rozdelene_html_okres = BeautifulSoup(odpoved_okres.text, 'html.parser')
    url_obce = rozdelene_html_okres.find_all("a", href=lambda h: h and "ps311" in h)
    obec_odkazy = [odkaz for odkaz in url_obce if odkaz.text.strip() != "X"]
    cela_adresa_obce_list = [
        "https://www.volby.cz/pls/ps2017nss/" + odkaz["href"]
        for odkaz in obec_odkazy
    ]
    return cela_adresa_obce_list

##### VOLÁNÍ FUNKCE #####:
# Volání funkce s argumentem: odkaz na územní celek
cela_adresa_obce_list = ziskej_adresy_obci_v_okrese(adresa_okresu)

# Tisk všech adres obcí v daném okrese:
pprint(cela_adresa_obce_list)
print(type(cela_adresa_obce_list))

##########################################################################################
# ZÍSKÁNÍ URL VŠECH OBCÍ V JEDNOM OKRESE
##########################################################################################








