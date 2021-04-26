import plotly.express as px
from itertools import cycle
import pandas as pd

bl_dict = {
    'BB': 'Brandenburg',
    'BE': 'Berlin',
    'BW': 'Baden-Württemberg',
    'BY': 'Bayern',
    'DE': 'Deutschland',
    'HB': 'Bremen',
    'HE': 'Hessen',
    'HH': 'Hamburg',
    'MV': 'Mecklenburg-Vorpommern',
    'NI': 'Niedersachsen',
    'NW': 'Nordrhein-Westfalen',
    'RP': 'Rheinland-Pfalz',
    'SH': 'Schleswig-Holstein',
    'SL': 'Saarland',
    'SN': 'Sachsen',
    'ST': 'Sachsen-Anhalt',
    'TH': 'Thüringen'
}

inf_lander_dict = {
    'BB': 'DE-BB',
    'BE': 'DE-BE',
    'BW': 'DE-BW',
    'BY': 'DE-BY',
    'HB': 'DE-HB',
    'HE': 'DE-HE',
    'HH': 'DE-HH',
    'MV': 'DE-MV',
    'NI': 'DE-NI',
    'NW': 'DE-NW',
    'RP': 'DE-RP',
    'SH': 'DE-SH',
    'SL': 'DE-SL',
    'SN': 'DE-SN',
    'ST': 'DE-ST',
    'TH': 'DE-TH',
    'DE': 'sum_cases'
}
# Quelle:
# https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/Tabellen/bevoelkerung-nichtdeutsch-laender.html
lander_pop_dict = {
    'DE': 83_190_556,
    'NW': 17_947_221,
    'BY': 13_124_737,
    'BW': 11_100_394,
    'NI': 7_993_608,
    'HE': 6_288_080,
    'RP': 4_093_903,
    'SN': 4_071_971,
    'BE': 3_669_491,
    'SH': 2_903_773,
    'BB': 2_521_893,
    'ST': 2_194_782,
    'TH': 2_133_378,
    'HH': 1_847_253,
    'MV': 1_608_138,
    'SL': 986_887,
    'HB': 681_202,
}


bl_kurzel = ['BB', 'BE', 'BW', 'BY', 'DE', 'HB', 'HE', 'HH',
             'MV', 'NI', 'NW', 'RP', 'SH', 'SL', 'SN', 'ST', 'TH']


def get_land_pop(kurzel):
    return lander_pop_dict[kurzel]


def get_palette():
    return cycle(px.colors.qualitative.Safe)


# palette = cycle(['black', 'grey', 'red', 'blue'])
# palette = cycle(px.colors.sequential.PuBu)

def write_html(fig, filename):
    fig.write_html(f"plots/{filename}.html", include_plotlyjs="cdn")


ags_df = pd.read_json('data/ags.json').transpose()


def get_ags(lk_name):
    row = ags_df[ags_df['name'] == lk_name]
    return f'{row.index.values[0]}'


def week_day_string(weekday):
    if weekday == 0:
        return 'Mon'
    elif weekday == 1:
        return 'Tue'
    elif weekday == 2:
        return 'Wed'
    elif weekday == 3:
        return 'Thu'
    elif weekday == 4:
        return 'Fri'
    elif weekday == 5:
        return 'Sat'
    elif weekday == 6:
        return 'Sun'
    else:
        return 'other'


def is_weekend(weekday):
    if weekday == 5:
        return True
    elif weekday == 6:
        return True
    else:
        return False


def year_and_week(date):
    year = date.year - 1 if date.month < 2 and date.week > 10 else date.year
    return f"{year}_{format(date.week, '02d')}"


# df has to have a dt date column
def add_weekday_stuff(df, date_column):
    df['weekday'] = df[date_column].dt.dayofweek
    df['is_weekend'] = df.apply(lambda x: is_weekend(x['weekday']), axis=1)
    df['weekday_name'] = df.apply(
        lambda x: week_day_string(x['weekday']), axis=1)
    df['calendar_week'] = df[date_column].dt.isocalendar().week
    df['year_and_week'] = df.apply(lambda x: year_and_week(x['date']), axis=1)
    return df.drop(columns=['weekday'])
