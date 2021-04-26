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

bl_kurzel = ['BB', 'BE', 'BW', 'BY', 'DE', 'HB', 'HE', 'HH', 'MV', 'NI', 'NW', 'RP', 'SH', 'SL', 'SN', 'ST', 'TH']


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
    df['weekday_name'] = df.apply(lambda x: week_day_string(x['weekday']), axis=1)
    df['calendar_week'] = df[date_column].dt.isocalendar().week
    df['year_and_week'] = df.apply(lambda x: year_and_week(x['date']), axis=1)
    return df.drop(columns=['weekday'])
