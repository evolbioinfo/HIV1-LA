import pandas as pd
from jphmm_tools import parse_breakpoints, breakpoints2bitmasks, HIV1_BREAKPOINTS, shift_bitmask, cut_breakpoints, \
    expand_crfs, remove_gaps, get_reference_seq, get_reference_coordinates
from jphmm_tools.subtyper import get_subtypes

REFERENCE_ID = 'B.FR.83.HXB2_LAI_IIIB_BRU.K03455'

if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_data', required=True, type=str)
    parser.add_argument('--in_msa', required=True, type=str)
    parser.add_argument('--in_rec', required=True, type=str)
    parser.add_argument('--ref_aln', required=True, type=str)
    parser.add_argument('--out_data', required=True, type=str)
    params = parser.parse_args()

    crf2st2bm = breakpoints2bitmasks(parse_breakpoints(HIV1_BREAKPOINTS), generalise_subtypes=True)
    cut_breakpoints(crf2st2bm,
                    cut_ref=remove_gaps(get_reference_seq(params.ref_aln,
                                                          reference_id=REFERENCE_ID)))
    position_shift, n, n_gappy = \
        get_reference_coordinates(params.ref_aln, reference_id=REFERENCE_ID)
    shift_bitmask(crf2st2bm,
                  {crf: position_shift[: min(n, len(next(iter(crf2st2bm[crf].values()))))] for crf in crf2st2bm.keys()},
                  n_gappy)
    expand_crfs(crf2st2bm, crf2st2bm)
    st_df = get_subtypes(params.in_msa, params.in_rec, crf2st2bitmask=crf2st2bm, slack=0, generalise_subtypes=True)

    df = pd.read_csv(params.in_data, sep='\t', header=0, index_col=0)
    df.index = df.index.map(str)

    df.join(st_df, how="outer").to_csv(params.out_data, sep='\t', index_label='id')
