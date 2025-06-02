# Election Scraper 2017

Tento skript slouží k automatickému stahování a ukládání volebních výsledků z webové stránky [volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro konkrétní územní celek. Výsledky jsou uloženy do CSV souboru, který obsahuje kód obce, název obce, voliče v seznamu, vydané obálky, platné hlasy a hlasy pro jednotlivé politické strany.

## Požadavky

Pro běh skriptu je potřeba nainstalovat následující knihovny:

- requests
- beautifulsoup4
- lxml

Pro instalaci knihoven stačí pustit v terminálu:
pip install -r requirements.txt


Jak spustit:
Stáhněte si projekt a přejděte do adresáře, kde je uložený.

Spusťte skript pomocí následujícího příkazu:
python main.py "URL územního celku" "název_výstupního_souboru.csv"

Příklad:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
(Tento příkaz stáhne výsledky voleb pro územní celek Prostějov a uloží je do souboru vysledky_prostejov.csv.)

Formát výstupu:
Výstupní CSV soubor bude obsahovat následující sloupce:

1. Kód obce
2. Název obce
3. Voliči v seznamu
4. Vydané obálky
5. Platné hlasy
6. a další budou jednotlivé Politické strany a jejich hlasy

Soubor se uloží do adresáře .venv, který vznikl pro virtuální prostředí projektu.

