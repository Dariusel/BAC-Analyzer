import os
import re
import json
import requests
from bs4 import BeautifulSoup

year = 2025



data_index = {
    'cod': 0,
    'medie': 1,
    'rezultat': 2,
    'liceu': 5,
    'promotie_anterioara': 6,
    'forma_invatamant': 7,
    'specializare': 8,
    'limba_romana_competente': 9,
    'limba_romana_nota': 10,
    'limba_romana_contestatie': 11,
    'limba_romana_nota_finala': 12,
    'limba_moderna_studiata_competente': 14,
    'limba_moderna_studiata_nota': 15,
    'disciplina_obligatorie': 16,
    'disciplina_obligatorie_nota': 25,
    'disciplina_obligatorie_contestatie': 26,
    'disciplina_obligatorie_nota_finala': 27,
    'disciplina_alegere': 17,
    'disciplina_alegere_nota': 28,
    'disciplina_alegere_contestatie': 29,
    'disciplina_alegere_nota_finala': 30,
    'competente_digitale': 18,
}

CACHE_LOCATION = f'resources/cache/bac/bac-{year}.json'
RESULTS_LOCATION = f'resources/results/bac-{year}.json'


def main(year):
    final_data = {}
    data_cache = {}
    
    page = 1
    page_table_data = get_table_data(page)
    while page_table_data:
        final_data.update(page_table_data)
        data_cache[page] = page_table_data

        if page % 50 == 0:
            try_update_cache(data_cache)

        page += 1
        page_table_data = get_table_data(page)

    try_update_cache(data_cache)

    # Save final data to results file
    os.makedirs(os.path.dirname(RESULTS_LOCATION), exist_ok=True)  # Ensure results directory exists
    with open(RESULTS_LOCATION, 'w') as file:
        json.dump(final_data, file, indent=4, ensure_ascii=False)

    return final_data


def get_table_data(page):
    # Check if cache file exists and is valid otherwise create it
    if os.path.isfile(CACHE_LOCATION):
        with open(CACHE_LOCATION, 'r') as file:
            try:
                cache_json = json.load(file)
            except json.JSONDecodeError:
                cache_json = {}
    else:
        cache_json = {}

    page_str = str(page)
    if page_str in cache_json:
        print(f'Using cache for page {page}')
        return cache_json[page_str] # Return cached data if available


    get = requests.get(f'https://static.bacalaureat.edu.ro/{year}/rapoarte/CJ/rezultate/dupa_medie/page_{page}.html')
    if get.status_code != 200:
        return None

    print(f'Fetching data for page {page}...')
    soup = BeautifulSoup(get.content, 'html.parser')
    table = soup.find('table', id='mainTable')

    if table is None:
        return 'Table not found'
    
    data = {}
    rows = table.find_all('tr')
    for i in range(2, len(rows), 2):
        group = rows[i:i+2]
        row_content = []
        
        script_item = group[0].find_all('script')[0].get_text(strip=True)
        matches = re.findall(r'="([^"<]+) <br>', script_item) + re.findall(r'="([^"<]+)";', script_item) # Extracts candidate code, score, and result from 'LuatDePeBacalaureatEduRo["CJ1496166 <br>"]="CJ1496166 <br>";LuatDePe_BacalaureatEduRo["CJ1496166 <br>"]="10";Luat_DePe_BacalaureatEduRo["CJ1496166 <br>"]="REUSIT";'

        row_content.extend(matches)
        for row in group:
            row_content.extend([item.get_text(strip=True) for item in row.find_all('td')])

        nr_crt = row_content[3]
        data[nr_crt] = {key: row_content[i] for key, i in data_index.items()}

    return data
 


def try_update_cache(data):
    os.makedirs(os.path.dirname(CACHE_LOCATION), exist_ok=True) # Ensure cache directory exists

    # Create cache file if it doesn't exist
    if not os.path.isfile(CACHE_LOCATION):
        with open(CACHE_LOCATION, 'w') as file:
            json.dump({}, file)

    # Read existing cache
    with open(CACHE_LOCATION, 'r') as file:
        try:
            cache_json = json.load(file)
        except json.JSONDecodeError:
            cache_json = {}

    # Update cache with new data
    with open(CACHE_LOCATION, 'w') as file:
        for page in data:
            cache_json[str(page)] = data[page]

        json.dump(cache_json, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main(year)