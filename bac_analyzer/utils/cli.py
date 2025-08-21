import argparse

from bac_analyzer.utils.file_paths import SQL_ELEVI_DATABASE

def define_args():
    parser = argparse.ArgumentParser(description='Analyze BAC data.')
    subparser = parser.add_subparsers(dest='command')


    parser.add_argument('--input', type=str, default=SQL_ELEVI_DATABASE, help='Path to the input data file')


    # Strip Plot
    strip_plot_parser = subparser.add_parser('strip')
    strip_plot_parser.add_argument('--year', type=int, default=2025, help='Year of the BAC exam data to analyze')
    strip_plot_parser.add_argument('--county', '--judet', type=str, default='BUCURESTI', help='Target county (judet) to filter results for the strip plot')

    # Box&Whiskers Plot
    box_plot_parser = subparser.add_parser('box')
    box_plot_parser.add_argument('--year', type=int, default=2025, help='Year of the BAC exam data to analyze')
    box_plot_parser.add_argument('--county', '--judet', type=str, default=None, help='If specified, shows distribution of scores for all highschools in that county instead of all counties')

    # Bar Plot
    bar_plot_parser = subparser.add_parser('bar')
    bar_plot_parser.add_argument('--year', type=int, default=2025, help='Year of the BAC exam data to analyze')
    bar_plot_parser.add_argument('--county', '--judet', type=str, default=None, help='Target county (judet) to restrict results')
    bar_plot_parser.add_argument('--highschool', '--liceu', type=str, default=None, help='Target highschool (liceu) within the selected county')

    # Histogram Plot
    histogram_plot_parser = subparser.add_parser('histogram')
    histogram_plot_parser.add_argument('--year', type=int, default=2025, help='Year of the BAC exam data to analyze')
    histogram_plot_parser.add_argument('--county', '--judet', type=str, default=None, help='Filter by specific county (judet)')
    histogram_plot_parser.add_argument('--highschool', '--liceu', type=str, default=None, help='Filter by specific highschool (liceu)')
    histogram_plot_parser.add_argument('--score', '--nota', type=float, default=None, help='Highlight a specific score (nota) on the histogram')

    # Density Plot
    density_plot_parser = subparser.add_parser('density')
    density_plot_parser.add_argument('--year', type=int, default=None, help='Select a year to compare distributions across counties. Required if --county is used')
    density_plot_parser.add_argument('--county', '--judet', type=str, default=None, help='If specified --year, compares all highschools in the selected county')
    density_plot_parser.add_argument('--score', '--nota', type=float, default=None, help='Highlight a specific score (nota) with a vertical line on the density plot')

    return parser