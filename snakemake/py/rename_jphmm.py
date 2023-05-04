import pandas as pd

if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_file', required=True, type=str)
    parser.add_argument('--out_file', required=True, type=str)
    parser.add_argument('--map', required=True, type=str)
    params = parser.parse_args()

    accession2id = pd.read_csv(params.map, sep='\t')[['id', 'accession']]
    accession2id = dict(zip(list(accession2id['accession']), list(accession2id['id'])))

    with open(params.out_file, 'w+') as f:
        with open(params.in_file, 'r') as in_f:
            for line in in_f.readlines():
                if line.startswith('>'):
                    name = line.split(' ')[0].strip('>').strip('\n')
                    accession = name[name.rfind('_') + 1:]
                    line = line.replace(name, accession2id[accession])
                f.write(line)
