import os

import bac_analyzer




def get_root_dir():
    file_dir = os.path.dirname(bac_analyzer.__file__)
    root_dir = ''
    if 'site-packages' in file_dir.lower(): # Normal Install
        root_dir = os.path.abspath(os.path.join(file_dir, '..', '..', '..', '..'))
    else: # Editable Install
        root_dir = os.path.abspath(os.path.join(file_dir, '..'))

    return root_dir



ROOT_DIR = get_root_dir()

JUDETE_LOCATION = os.path.join(ROOT_DIR,
                               'resources',
                               'judete.json')

TABLE_DATA_INDEX_LOCATION = os.path.join(ROOT_DIR,
                                         'resources',
                                         'table_data_indexes.json')

SQL_ELEVI_DATABASE = os.path.join(ROOT_DIR,
                                  'elevi.db')