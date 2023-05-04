from collections import defaultdict

import pandas as pd
from ete3 import Tree
from pastml.tree import remove_certain_leaves

if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--data', required=True, type=str)
    parser.add_argument('--partition', required=True, type=str)
    parser.add_argument('--in_nwk', required=True, type=str)
    parser.add_argument('--out_nwk', required=True, type=str)
    parser.add_argument('--subtype_col', required=False, default='generalized_subtype', type=str)
    params = parser.parse_args()

    df = pd.read_csv(params.data, index_col=0, sep='\t')[[params.subtype_col]]
    df.index = df.index.map(str)
    tree = Tree(params.in_nwk)

    st2count = defaultdict(lambda: 1)
    st2root = {}
    for n in tree.traverse('postorder'):
        if n.is_leaf():
            n.add_feature('subtype', df.loc[n.name, params.subtype_col])
            continue
        subtypes = set(getattr(_, 'subtype', None) for _ in n.children)
        st = 'node'
        if len(subtypes) == 1 and subtypes != {None}:
            st = subtypes.pop()
            n.add_feature('subtype', st)
        n.name = '{}_{}'.format(st, st2count[st])
        st2count[st] += 1
        st2root[st].append(n.name)

    rare_subtypes = {st for (st, c) in st2count.items() if c < 10}
    to_remove = set()
    for st in rare_subtypes:
        to_remove |= set(df[df[params.subtype_col] == st].index)
    print('Removing {} tips corresponding to rare subtypes {}'.format(len(to_remove), ','.join(rare_subtypes)))
    tree = remove_certain_leaves(tree, lambda _: _.name in to_remove)
    tree.write(outfile=params.out_nwk, format=3)

    with open(params.partition, 'w+') as f:
        for st, root in st2root.items():
            if st not in rare_subtypes:
                f.write(st + ' 1 {' + root + '}\n')
