import os
import sqlite3
import argparse
import pandas as pd


from bac_analyzer.utils.cli import define_args
from bac_analyzer.utils.file_paths import SQL_ELEVI_DATABASE
from bac_analyzer.utils.graphs import strip_plot, box_plot, bar_plot, histogram_plot, density_plot



def load_dataframe(year = None):
    conn = sqlite3.connect(SQL_ELEVI_DATABASE)
    if year:
        query = "SELECT * from Elevi where year = ?"

        df = pd.read_sql_query(query, conn, params=(year,))

        return df

    query = "SELECT * from Elevi"

    df = pd.read_sql(query, conn)

    conn.close()

    return df



def main():
    parser = define_args()
    args = parser.parse_args()

    df = load_dataframe()
    #
    #other_dfs = [load_data(x) for x in [2023,2024,2025] if x != args.year] # Make an array containing all the other years except args.year
    #all_dfs = other_dfs + [df] # Create a list with a dataframe from each year

    if args.command == 'strip':
        strip_plot(df, args.year, args.county)
    elif args.command == 'box':
        box_plot(df, args.year, args.county)
    elif args.command == 'bar':
        bar_plot(df, args.year, args.county, args.highschool)
    elif args.command == 'histogram':
        histogram_plot(df, args.year, args.county, args.highschool, args.score)
    elif args.command == 'density':
        density_plot(df, args.year, args.county, args.score)


if __name__ == '__main__':
    main()
