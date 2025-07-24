import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

JUDETE_LOCATION = os.path.join(ROOT_DIR,
                               'resources',
                               'judete.json')

TABLE_DATA_INDEX_LOCATION = os.path.join(ROOT_DIR,
                                         'resources',
                                         'table_data_indexes.json')

SQL_ELEVI_DATABASE = os.path.join(ROOT_DIR,
                                  'elevi.db')