import os
import logging
import csv
import requests

CSV_VAC = {
    'url': 'https://raw.githubusercontent.com/ard-data/2020-rki-impf-archive/master/data/9_csv_v2/region_BY.csv',
    'file': 'vac.csv'
}
CSV_INF_OLD = {
    'url': 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv',
    'file': 'arcgisinf.csv'
}

CSV_INF = {
    'url': 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv',
    'file': 'inf.csv'
}


def fix_comma_in_csv(filename):
    fin = open(filename, "rt")
    data = fin.read()

    data = data.replace('"," ', '_')
    data = data.replace('","', '.')
    data = data.replace('\"', '')
    fin.close()
    fin = open(filename, "wt")
    fin.write(data)
    fin.close()


def download_data(csv_data):
    response = requests.get(csv_data['url'])

    with open(csv_data['file'], 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
        print(f'Downloaded {csv_data["file"]}')


download_data(CSV_VAC)
download_data(CSV_INF_OLD)
download_data(CSV_INF)
fix_comma_in_csv('arcgisinf.csv')
