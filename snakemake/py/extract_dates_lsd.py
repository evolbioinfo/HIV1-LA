import pandas as pd


INTERVAL = 'interval'

INPUT = 'input'


def date2years(d, default_min_date=1900, default_max_date=2023, type=INPUT):
    """
    Converts date to floats provided the dates are year-specific
    :param d: input date to be converted
    :param default_min_date: default min date
    :param default_max_date: default max date
    :param type: interval or input: if interval is specified the min and max dates returns would correspond
        to the 1st day of the date's month and the 1st day of the month following the date's one.
        Otherwise, the middle of the month will be returned.
    :return: date (None if min_date < max_date), min_date, max_date
    """
    if pd.notnull(d):
        min_date = int(d)
        max_date = min_date + 1

        if INTERVAL == type:
            return None, min_date, max_date
        else:
            date = (min_date + max_date) / 2
            return date, date, date
    else:
        return None, default_min_date, default_max_date


if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--data', required=True, type=str)
    parser.add_argument('--dates', required=True, type=str)
    parser.add_argument('--date_col', required=True, type=str)
    parser.add_argument('--type', required=False, choices=(INTERVAL, INPUT), type=str, default=INPUT)
    params = parser.parse_args()

    df = pd.read_csv(params.data, index_col=0, sep='\t')[[params.date_col]]
    m_date = date2years(df[~pd.isna(df[params.date_col])][params.date_col].min())[1]
    M_date = 2023
    df[['date', 'lower', 'upper']] = \
        df[params.date_col].apply(lambda _: date2years(_, m_date, M_date, params.type)).apply(pd.Series)
    df.loc[pd.isna(df['date']), 'date'] = 'b(' + df.loc[pd.isna(df['date']), 'lower'].astype(str) \
                                          + ',' + df.loc[pd.isna(df['date']), 'upper'].astype(str) + ')'
    if params.dates:
        with open(params.dates, 'w+') as f:
            f.write('%d\n' % df.shape[0])
        df['date'].to_csv(params.dates, sep='\t', header=False, mode='a')

