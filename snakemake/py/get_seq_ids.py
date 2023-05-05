import pandas as pd

if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--input_data', required=True, type=str)
    parser.add_argument('--outgroup', required=False, type=str)
    parser.add_argument('--subtype', nargs='+', type=str)
    params = parser.parse_args()

    df = pd.read_csv(params.input_data, sep='\t', index_col=0, header=0)
    df.index = df.index.map(str)

    ids = list()
    for subtype in params.subtype:
        ids.extend(list(df[df['generalized_subtype'] == subtype].index))
    with open(params.outgroup, 'w+') as f:
        f.write('\n'.join(ids))
