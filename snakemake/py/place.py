import json

from ete3 import Tree

if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser(description='Annotate a tree with location data.')

    parser.add_argument('--in_nwk', required=True, type=str,
                        help='Path to the input unrooted tree in newick format.')
    parser.add_argument('--out_nwk', type=str, required=True,
                        help='Path where the rooted nwk tree should be saved.')
    parser.add_argument('--placement', type=str, required=True,
                        help='EPA-NG output with outgroup placement information.')
    params = parser.parse_args()

    tree = Tree(params.in_nwk)
    with open(params.placement, 'r') as f:
        res = json.load(f)
    field2value = dict(zip(res['fields'], res['placements'][0]['p'][0]))

    for i, n in enumerate(tree.traverse('postorder')):
        if i == field2value['edge_num']:
            dist = n.dist
            tree.set_outgroup(n)
            og, ig = tree.children
            if ig == n:
                og, ig = ig, og
            og.dist = field2value['distal_length']
            ig.dist = dist - field2value['distal_length']
            break

    tree.write(outfile=params.out_nwk)

