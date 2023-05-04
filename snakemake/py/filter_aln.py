import gzip
import logging
import lzma
import os

import pandas as pd
from Bio import SeqIO


def get_write_handle(fa, temp_suffix='', mode='wb'):
    if fa.endswith('.gz'):
        return gzip.open(fa + temp_suffix, mode)
    if fa.endswith('.xz'):
        return lzma.open(fa + temp_suffix, mode)
    return open(fa + temp_suffix, mode)


def get_read_handle(filepath, write=False):
    """Automatically get (un)compressed file handle"""
    ext = filepath.split(".")[-1]

    mode = "wt" if write else "rt"

    if ext == "gz":
        return gzip.open(filepath, mode)
    elif ext == "xz":
        return lzma.open(filepath, mode)

    return open(filepath, mode[0])


def filter_recs(fa, md):
    df = pd.read_csv(md, sep='\t', index_col=0)[['subtype_jpHMM']]
    df.index = df.index.map(str)

    subtype2count = {st: len(df[df['subtype_jpHMM'] == st]) for st in df['subtype_jpHMM'].unique()}

    with get_read_handle(fa) as handle:
        for rec in SeqIO.parse(handle, "fasta"):
            subtype = df.loc[rec.id, 'subtype_jpHMM']
            if ',' not in subtype and subtype2count[subtype] >= 10:
                yield rec


if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_aln', required=True, type=str)
    parser.add_argument('--out_aln', required=True, type=str)
    parser.add_argument('--metadata', required=True, type=str)
    params = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S",
                        filename=None)

    with get_write_handle(params.out_aln, '.temp') as f:
        count = 0
        for rec in filter_recs(params.in_aln, params.metadata):
            f.write('>{}\n{}\n'.format(rec.id, rec.seq).encode())
            count += 1
    os.rename(params.out_aln + '.temp', params.out_aln)
    logging.info("Kept {} pure-subtype records with at least 10 sequences per subtype".format(count))
