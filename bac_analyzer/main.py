import os
import sqlite3
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from bac_analyzer.utils.file_paths import SQL_ELEVI_DATABASE, ROOT_DIR


plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')


def load_data(year):
    conn = sqlite3.connect(SQL_ELEVI_DATABASE)
    query = "SELECT * from Elevi where year = ?"

    df = pd.read_sql_query(query, conn, params=(year,))

    return df


def plot_student_medie_by_licee_judet(df, judet):
    plt.figure(figsize=(20,10))
    sns.stripplot(data=df[df['judet'] == judet], x='medie', y='liceu', hue='liceu', dodge=False, jitter=False, size=5, palette='tab20')
    plt.title(f'Medii BAC pe Licee {judet}')
    plt.xlabel('Medie')
    plt.ylabel('Liceu')
    plt.xlim(5,10)
    plt.tight_layout()
    plt.show()


def plot_judet_medie(df):
    means = df.groupby('judet')['medie'].mean().sort_values(ascending=False).reset_index()

    sns.barplot(means, x='medie', y='judet')

    plt.xlim(7,8.5)
    plt.show()


def plot_rezultate(df):
    rezultate = df.groupby('rezultat').size().sort_values(ascending=False).reset_index(name='count')
    print(rezultate)

    sns.barplot(rezultate, x='rezultat', y='count')

    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Analyze BAC data.')
    parser.add_argument('--input', type=str, default=SQL_ELEVI_DATABASE, help='Path to the input data file')
    parser.add_argument('--year', type=int, default=2025, help='Year of the BAC exam data to analyze')
    parser.add_argument('--judet', type=str, default='BUCURESTI', help='Judet of the exam data')
    parser.add_argument('--temp_option', type=int, default=1, help='Which type of plot to display (1, 2 or 3) **TEMPORARY**')
    args = parser.parse_args()

    df = load_data(args.year)

    if args.temp_option == 1:
        plot_student_medie_by_licee_judet(df, args.judet)
    elif args.temp_option == 2:
        plot_judet_medie(df)
    elif args.temp_option == 3:
        plot_rezultate(df)


if __name__ == '__main__':
    main()
