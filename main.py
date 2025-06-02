import requests
from bs4 import BeautifulSoup
import csv
import sys
from urllib.parse import urljoin


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def get_obec_links(base_url, soup):
    links = []
    for row in soup.select('table tr')[2:]:
        cells = row.find_all('td')
        if len(cells) >= 1:
            link = cells[0].find('a')
            name = cells[1].text.strip()
            if link:
                href = link['href']
                full_url = urljoin(base_url, href)
                code = link.text.strip()
                links.append((code, name, full_url))
    return links


def get_obec_data(code, name, url):
    soup = get_soup(url)

    # Informace o voličích a hlasech
    tables = soup.find_all('table')
    t1 = tables[0].find_all('td')
    voters_in_list = t1[3].text.replace('\xa0', '')
    envelopes_given = t1[4].text.replace('\xa0', '')
    valid_votes = t1[7].text.replace('\xa0', '')

    # Hlasy pro strany
    parties_data = {}
    for table in tables[1:]:
        rows = table.find_all('tr')[2:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                party = cols[1].text.strip()
                votes = cols[2].text.strip().replace('\xa0', '')
                parties_data[party] = votes

    return {
        'kod_obce': code,
        'obec': name,
        'voliči_v_seznamu': voters_in_list,
        'vydané_obálky': envelopes_given,
        'platné_hlasy': valid_votes,
        'strany': parties_data
    }


def main():
    if len(sys.argv) != 3:
        print("Chyba: Zadejte 2 argumenty – URL územního celku a název výstupního CSV souboru.")
        sys.exit(1)

    main_url = sys.argv[1]
    output_file = sys.argv[2]

    if "volby.cz/pls/ps2017nss/ps32" not in main_url:
        print("Chyba: Zadaná URL není platná volební stránka.")
        sys.exit(1)

    print(f"Načítám seznam obcí z: {main_url}")
    soup = get_soup(main_url)
    obce_links = get_obec_links(main_url, soup)

    all_results = []
    all_parties = set()

    for code, name, url in obce_links:
        print(f"Zpracovávám obec: {name} ({code})")
        data = get_obec_data(code, name, url)
        all_parties.update(data['strany'].keys())
        all_results.append(data)

    sorted_parties = sorted(all_parties)

    # Zápis do CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy'] + sorted_parties
        writer.writerow(header)

        for row in all_results:
            strany_votes = [row['strany'].get(party, '0') for party in sorted_parties]
            writer.writerow([
                row['kod_obce'],
                row['obec'],
                row['voliči_v_seznamu'],
                row['vydané_obálky'],
                row['platné_hlasy']
            ] + strany_votes)

    print(f"Hotovo! Výsledky uloženy do souboru {output_file}")


if __name__ == "__main__":
    main()
