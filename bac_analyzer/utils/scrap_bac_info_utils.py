import os
import json
import sqlite3

from bac_analyzer.utils.file_paths import SQL_ELEVI_DATABASE, TABLE_DATA_INDEX_LOCATION
from bac_analyzer.utils.elev import Elev


data_index = json.load(open(TABLE_DATA_INDEX_LOCATION, 'r'))


def get_return_data(status, message, data):
    return {
        'status': status,
        'message': message,
        'data': data
    }


def parse_row_content(row_content, judet, page, year): # return Elev
    elev = Elev()

    ignore_keys = ['judet', 'page', 'year']
    str_keys = ['limba_materna', 'limba_moderna_studiata_nota', 'competente_digitale', 'rezultat']
    float_keys = ['medie', 'limba_romana_nota', 'limba_romana_contestatie', 'limba_romana_nota_finala', 'limba_materna_nota', 'limba_materna_contestatie', 'limba_materna_nota_finala', 'limba_moderna_studiata_nota',
                  'disciplina_obligatorie_nota', 'disciplina_obligatorie_contestatie', 'disciplina_obligatorie_nota_finala', 'disciplina_alegere_nota', 'disciplina_alegere_contestatie', 'disciplina_alegere_nota_finala']
    for key in elev.__dict__.keys():
        if key in ignore_keys:
            continue

        value = row_content[int(data_index[key])]
        if value.strip() == '':
            value = None
        #print(f'{row_content} -> {value}')

        if key in str_keys:
            setattr(elev, key, str(value) if value is not None else None)
        elif key in float_keys:
            setattr(elev, key, float(value) if value is not None else None)
        elif key == 'promotie_anterioara':
            elev.promotie_anterioara = True if value == 'DA' else False
        else:
            setattr(elev, key, value)

    elev.judet = judet
    elev.page = page
    elev.year = year
    
    return elev


def init_elevi_database(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Elevi (
                   cod TEXT PRIMARY KEY,
                   medie REAL,
                   rezultat TEXT,
                   liceu TEXT,
                   promotie_anterioara BOOLEAN,
                   forma_invatamant TEXT,
                   specializare TEXT,
                   limba_romana_competente TEXT,
                   limba_romana_nota REAL,
                   limba_romana_contestatie REAL,
                   limba_romana_nota_finala REAL,
                   limba_moderna_studiata_competente TEXT,
                   limba_moderna_studiata_nota REAL,
                   disciplina_obligatorie TEXT,
                   disciplina_obligatorie_nota REAL,
                   disciplina_obligatorie_contestatie REAL,
                   disciplina_obligatorie_nota_finala REAL,
                   disciplina_alegere TEXT,
                   disciplina_alegere_nota REAL,
                   disciplina_alegere_contestatie REAL,
                   disciplina_alegere_nota_finala REAL,
                   competente_digitale TEXT,
                   judet TEXT,
                   page INTEGER,
                   year INTEGER
                   )
                   """)
    conn.commit()
    conn.close()


def insert_elevi_to_db(elevi):
    conn = sqlite3.connect(SQL_ELEVI_DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("BEGIN TRANSACTION")
    for elev in elevi:
        cursor.execute("""
               INSERT OR REPLACE INTO Elevi (
                   cod, medie, rezultat, liceu, promotie_anterioara,
                   forma_invatamant, specializare, limba_romana_competente,
                   limba_romana_nota, limba_romana_contestatie, limba_romana_nota_finala,
                   limba_moderna_studiata_competente, limba_moderna_studiata_nota,
                   disciplina_obligatorie, disciplina_obligatorie_nota, disciplina_obligatorie_contestatie,
                   disciplina_obligatorie_nota_finala, disciplina_alegere, disciplina_alegere_nota,
                   disciplina_alegere_contestatie, disciplina_alegere_nota_finala,
                   competente_digitale, judet, page, year
               ) VALUES (
                   :cod, :medie, :rezultat, :liceu, :promotie_anterioara,
                   :forma_invatamant, :specializare, :limba_romana_competente,
                   :limba_romana_nota, :limba_romana_contestatie, :limba_romana_nota_finala,
                   :limba_moderna_studiata_competente, :limba_moderna_studiata_nota,
                   :disciplina_obligatorie, :disciplina_obligatorie_nota, :disciplina_obligatorie_contestatie,
                   :disciplina_obligatorie_nota_finala, :disciplina_alegere, :disciplina_alegere_nota,
                   :disciplina_alegere_contestatie, :disciplina_alegere_nota_finala,
                   :competente_digitale, :judet, :page, :year
               )
           """, {**elev})
        
    conn.commit()
    conn.close()


def check_if_db_has_year_page_judet(year, page, judet):
    conn = sqlite3.connect(SQL_ELEVI_DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT EXISTS(
                      SELECT 1 FROM Elevi WHERE year = ? AND page = ? AND judet = ?)""", (year, page, judet))
    
    count = cursor.fetchone()[0]
    conn.close()

    return True if count == 1 else False