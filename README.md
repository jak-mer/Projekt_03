## **Scraper volebních dat**

Tento projekt je Python skript navržený pro stahování výsledků voleb z webových stránek Českého statistického úřadu (volby.cz). Získává podrobné informace o volební účasti a hlasech pro politické strany z určených obcí v rámci daného okresu a ukládá tato data do souboru CSV.



### Instalace

Pro spuštění tohoto projektu je nutné nainstalovat Python knihovny, viz soubor requirements.txt.

Pro instalaci si vytvořte nové virtuální prostředí.



### Spuštění projektu

Tento skript main.py vyžaduje při spuštění v rámci příkazového řádku dva argumenty:



1/ URL adresa stránky s volebními výsledky okresu na volby.cz.

2/ Požadovaný název výstupního souboru CSV.



##### Zde je příklad, jak skript spustit:



###### Obecně:

python main.py <url\_okresu> <název\_výstupního\_souboru.csv>



### Ukázka projektu



###### Výsledky stahování pro okres Brno-město:



\# 1.argument: URL Kraje: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ\&xkraj=11\&xnumnuts=6202

\# 2.argument: Název souboru: vysledky\_brno\_mesto.csv



###### Spuštění programu:



\# STAHUJI DATA Z URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ\&xkraj=11\&xnumnuts=6202

\# UKLADAM DATA DO CSV SOUBORU: vysledky\_brno\_mesto.csv

\# UKONČUJI PROGRAM



###### Částečný výstup:

Kód obce,Název obce,Počet voličů,Počet obálek,Počet platných hlasů,Občanská demokratická strana, ....

535427,Bakov nad Jizerou,3922,2549,2539,285,3,3,204,1,179,153,27,32,36,2,1,252,2,2,113,864,1,8,42,2,18,4,6,295,4

535443,Bělá pod Bezdězem,3805,2215,2204,215,2,0,214,1,107,153,28,33,33,4,4,218,3,4,61,802,3,3,38,0,9,8,7,253,1

535451,Benátky nad Jizerou,5596,3267,3254,533,12,2,225,3,176,198,58,24,58,4,3,323,0,1,151,1041,1,6,77,1,26,10,6,306,9

...



