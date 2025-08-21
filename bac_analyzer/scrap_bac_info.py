import os
import re
import time
import json
import logging
import requests
from threading import Thread
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from bac_analyzer.utils.elev import Elev
from bac_analyzer.utils.logger import init_logger
from bac_analyzer.utils.file_paths import JUDETE_LOCATION, SQL_ELEVI_DATABASE
from bac_analyzer.utils.scrap_bac_info_utils import get_return_data, init_elevi_database, insert_elevi_to_db, check_if_db_has_year_page_judet, parse_row_content



year = 2023 # TODO 2024 and 2023



# Set and format all needed files globally inside script
judete = json.load(open(JUDETE_LOCATION, 'r'))


init_logger()


def main(year):
    init_elevi_database(SQL_ELEVI_DATABASE) # Creates elevi database if it doesnt exist
    final_data = {}

    # Loop through all judete and get each one's data from the year x
    for judet, initiale_judet in judete.items():
        logging.info('Processing data for judetul %s', judet)
        get_year_data_judet(year, initiale_judet)
    

    return


def get_year_data_judet(year, initiale_judet, max_workers: int = 16, batch_size: int = 100, max_page_debug: int = 9999):
    elevi_to_insert_in_db = []
    
    # Loop through all of the year pages and get_table_data from each with multiple threads
    page = 1
    reached_end = False
    while not reached_end:
        logging.debug("Processing batch for pages %d to %d", page, page+batch_size-1)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(lambda args: get_table_data(*args),
                                   [(year, initiale_judet, page) for page in range(page, page + batch_size)])

            for result in results:
                if result['status'] == 404:
                    logging.debug('Reached end of pages at page %d', page-1)
                    reached_end = True
                    break

                if page > max_page_debug:
                    logging.debug('Reached max page allowed for debug purposes %d', page)
                    reached_end = True
                    break
                
                if result['data'] != None:
                    for elev in result['data']:
                        elevi_to_insert_in_db.append(elev)

                #logging.debug('Page %d processed with status %s: %s', page, result['status'], result['message'])
                page += 1

    # Add missing elevi to database
    insert_elevi_to_db(elevi_to_insert_in_db)


def get_table_data(year, initiale_judet, page):
    # Check db if already exists
    if check_if_db_has_year_page_judet(year, page, [judet for judet, initiale in judete.items() if initiale == initiale_judet][0]):
        return get_return_data(304, 'Cache found', None)

    # Get page contents
    get = requests.get(f'https://static.bacalaureat.edu.ro/{year}/rapoarte/{initiale_judet}/rezultate/dupa_medie/page_{page}.html')
    if get.status_code != 200:
        return get_return_data(get.status_code, get.text, None)

    soup = BeautifulSoup(get.content, 'html.parser')
    table = soup.find('table', id='mainTable')

    if table is None:
        return get_return_data(get.status_code, 'Table not found', None)
    
    # Parse table data (Extract each elev from table entry)
    elevi = []
    rows = table.find_all('tr')
    for i in range(2, len(rows), 2):
        # Each table entry is made out of 2 joined rows
        group = rows[i:i+2]
        row_content = []
        
        # Extracts elev code, score, and result from 'LuatDePeBacalaureatEduRo["CJ1 <br>"]="CJ1 <br>";LuatDePe_BacalaureatEduRo["CJ1 <br>"]="10";Luat_DePe_BacalaureatEduRo["CJ1 <br>"]="REUSIT";'
        script_item = group[0].find_all('script')[0].get_text(strip=True)
        matches = re.findall(r'="([^"<]+) <br>', script_item) + re.findall(r'="([^"<]+)";', script_item)

        # Add all important data to row_content
        row_content.extend(matches)
        for row in group:
            row_content.extend([item.get_text(strip=True) for item in row.find_all('td')])

        # Add elev from row to elevi array
        judet = [judet for judet, initiale in judete.items() if initiale == initiale_judet][0]
        elev_obj = parse_row_content(row_content, judet, page, year)

        elevi.append(elev_obj.to_dict())
        
    return get_return_data(get.status_code, 'Data fetched successfully', elevi)


if __name__ == '__main__':
    start = time.time()
    main(year)
    logging.info(f'Time taken: {time.time() - start:.2f} seconds')