import os
import csv
import requests

import shared

CSV_VAC_INCOMPLETE = {
    'url_v2_old': 'https://raw.githubusercontent.com/ard-data/2020-rki-impf-archive/master/data/9_csv_v2/region_',
    'url': 'https://raw.githubusercontent.com/ard-data/2020-rki-impf-archive/master/data/9_csv_v3/region_',
    'file': 'data/vac.csv'
}

CSV_INF_CURRENT = {
    'url': 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv',
    'file': 'data/arcgisinf.csv'
}

CSV_INF_LK_HIST = {
    'url': 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv',
    'url2': 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rl-crowdsource-by-ags.csv',
    'file': 'data/inf_lk.csv'
}

CSV_INF_BL_HIST = {
    'url2': 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-state.csv',
    'url': 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rl-crowdsource-by-state.csv',
    'file': 'data/inf_bl.csv'
}

JSON_AGS = {
    'url': 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/ags.json',
    'file': 'data/ags.json'
}

# link wrong!
CSV_MUC_INZ = {
    'url': 'https://e.infogram.com/d2725960-06c5-4f17-8626-871d208db126?parent_url=https%3A%2F%2Fwww.muenchen.de%2Frathaus%2FStadtinfos%2FCoronavirus-Fallzahlen.html&src=embed#',
    'file': 'data/muc-inz.csv'
    # formatted very badly! >:(
}


def fix_comma_in_muc_infogram_csv(filename):
    fin = open(filename, "rt")
    data = fin.read()

    data = data.replace('","', ';')
    data = data.replace('\"', '')
    fin.close()
    fin = open(filename, "wt")
    fin.write(data)
    fin.close()


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


def download_csv(csv_data):
    response = requests.get(csv_data['url'])

    with open(csv_data['file'], 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
        print(f'Downloaded csv: {csv_data["file"]}')


def download_file(file_data):
    response = requests.get(file_data['url'])
    with open(file_data['file'], 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {file_data["file"]}')


def perform_download():
    import time
    import random

    bl_kurzel = shared.bl_kurzel
    random.shuffle(bl_kurzel)
    for bundesland_kurzel in bl_kurzel:
        dict = {
            'url': f'{CSV_VAC_INCOMPLETE["url"]}{bundesland_kurzel}.csv',
            'file': f'data/vac_{bundesland_kurzel}.csv',
        }

        time.sleep(random.uniform(0, 1))
        download_file(dict)
    time.sleep(random.uniform(0, 1))
    download_file(CSV_INF_LK_HIST)
    time.sleep(random.uniform(0, 1))
    download_file(CSV_INF_BL_HIST)
    time.sleep(random.uniform(0, 1))
    if os.path.isfile(JSON_AGS['file']):
        print(f'Skipping   {JSON_AGS["file"]} It already exists.')
    else:
        download_file(JSON_AGS)

    # download_file(CSV_MUC_INZ)
    # fix_comma_in_muc_infogram_csv(CSV_MUC_INZ['file'])

    download_file(CSV_INF_CURRENT)
    fix_comma_in_csv(CSV_INF_CURRENT['file'])


if __name__ == '__main__':
    from datetime import datetime
    print(f"{datetime.now()}")
    perform_download()
