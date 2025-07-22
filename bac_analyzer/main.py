import os
import json
import argparse
import matplotlib.pyplot as plt


def load_data():
    pass


def main():
    parser = argparse.ArgumentParser(description='Analyze BAC data.')
    parser.add_argument('--input', type=str, default='', help='Path to the input data file')
    parser.add_argument('--year', type=int, default=2025, help='Year of the BAC exam data to analyze')
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
