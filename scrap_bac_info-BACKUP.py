import os
import re
import json
import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import time

from bac_analyzer.utils.file_paths import CACHE_LOCATION, RESULTS_LOCATION, JUDETE_LOCATION, TABLE_DATA_INDEX_LOCATION, SQL_ELEVI_DATABASE
from bac_analyzer.utils.elev import Elev
from bac_analyzer.utils.scrap_bac_info_utils import try_update_cache, get_return_data, init_elev_database, insert_elev_to_db

year = 2025


data_index = json.load(open(TABLE_DATA_INDEX_LOCATION, 'r'))
judete = json.load(open(JUDETE_LOCATION, 'r'))


cache_file = CACHE_LOCATION.format(year=year)
results_file = RESULTS_LOCATION.format(year=year)



def main(year):
    cursor = init_elev_database(SQL_ELEVI_DATABASE)

    final_data = {}
    final_data = get_year_data_judet(year, 'CJ')
    for judet, initiale_judet in judete.items():
        print(initiale_judet)
    return

    cursor.connection.close()


def get_year_data_judet(year, initiale_judet, max_workers: int = 16, batch_size: int = 100):
    year_data_judet = {}
    data_cache = {}
    
    page = 1
    reached_end = False
    while not reached_end:
        print(f'Processing batch for pages {page} to {page+batch_size-1}')
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(lambda args: get_table_data(*args),
                                   [(year, initiale_judet, p) for p in range(page, page + batch_size)])

            for result in results:
                #print(result['data'])
                if page == 5:
                    reached_end = True
                    break
                if result['status'] == 404:
                    print(f'Reached end of pages at page {page-1}')
                    reached_end = True
                    break

                print(f'Page {page} processed with status {result["status"]}: {result["message"]}')


                year_data_judet[page] = result['data']
                data_cache[page] = result['data']
                page += 1

            try_update_cache(data_cache)

    # PERFORMANCE DEBUG PURPOSES
    #page_table_data = get_table_data(page)
    #while page_table_data['status'] != 404:
    #    print(f'Processing page {page} with status {page_table_data["status"]}: {page_table_data["message"]}')
    #    final_data.update(page_table_data['data'])
    #    data_cache[page] = page_table_data['data']
#
    #    if page % 50 == 0:
    #        try_update_cache(data_cache)
#
    #    page += 1
    #    page_table_data = get_table_data(page)
#
    #try_update_cache(data_cache)

    return year_data_judet


def get_table_data(year, initiale_judet, page):
    # Check if cache file exists and is valid otherwise create it
    if os.path.isfile(cache_file):
        with open(cache_file, 'r') as file:
            try:
                cache_json = json.load(file)
            except json.JSONDecodeError:
                cache_json = {}
    else:
        cache_json = {}

    page_str = str(page)
    if page_str in cache_json:
        return get_return_data(304, 'Cache found', cache_json[page_str])


    get = requests.get(f'https://static.bacalaureat.edu.ro/{year}/rapoarte/{initiale_judet}/rezultate/dupa_medie/page_{page}.html')
    if get.status_code != 200:
        return get_return_data(get.status_code, get.text, None)

    soup = BeautifulSoup(get.content, 'html.parser')
    table = soup.find('table', id='mainTable')

    if table is None:
        return get_return_data(get.status_code, 'Table not found', None)
    
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
        data[nr_crt] = Elev(**{key: row_content[int(i)] for key, i in data_index.items()}).to_dict()

    return get_return_data(get.status_code, 'Data fetched successfully', data)


if __name__ == '__main__':
    start = time.time()
    main(year)
    print(f'Time taken: {time.time() - start:.2f} seconds')