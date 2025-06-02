import requests
from bs4 import BeautifulSoup
import csv
import sys

# 1. Funkce pro ověření vstupních argumentů
def validate_arguments(args):
    if len(args) != 3:
        print("Zadejte prosím dva argumenty: URL a název výstupního souboru.")
        sys.exit(1)

# 2. Funkce pro načtení HTML obsahu stránky
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Chyba při načítání URL: {e}")
        sys.exit(1)

# 3. Funkce pro zpracování jednoho řádku s výsledky jedné obce
def parse_municipality_row(row):
    cols = row.find_all('td')
    if len(cols) > 1:
        municipality_code = cols[0].text.strip()
        municipality_name = cols[1].text.strip()
        voters_listed = cols[2].text.strip()
        ballots_issued = cols[3].text.strip()
        valid_votes = cols[4].text.strip()
        parties = [party.text.strip() for party in cols[5:]]
        return [municipality_code, municipality_name, voters_listed, ballots_issued, valid_votes] + parties
    return None

# 4. Funkce pro zpracování celé tabulky s výsledky
def parse_election_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')
    
    election_results = []
    for row in rows[1:]:  # přeskočení hlavičky
        parsed = parse_municipality_row(row)
        if parsed:
            election_results.append(parsed)
    
    return election_results

# 5. Funkce pro zápis výsledků do CSV
def write_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy', 'Kandidující strany...'])
        writer.writerows(data)

# 6. Hlavní funkce, která spouští celý proces
def main():
    validate_arguments(sys.argv)

    url = sys.argv[1]
    output_filename = sys.argv[2]

    print(f"Stahuji data z: {url}")
    html = fetch_html(url)
    
    print("Zpracovávám výsledky voleb...")
    results = parse_election_data(html)

    print(f"Ukládám výsledky do souboru: {output_filename}")
    write_to_csv(output_filename, results)

    print("Hotovo! 🎉 Výsledky byly úspěšně uloženy.")

if __name__ == '__main__':
    main()
