from pastml.tree import read_forest, annotate_dates, DATE_CI, DATE


if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser(description='Annotate a tree with location data.')

    parser.add_argument('--nexus', required=True, type=str,
                        help='Path to the input LSD2 time-scaled tree in nexus format.')
    parser.add_argument('--out_nwk', type=str, required=True,
                        help='Path where the date-annotated nwk tree should be saved.')
    params = parser.parse_args()

    tree = read_forest(params.nexus)[0]
    annotate_dates([tree])

    for i, n in enumerate(tree.traverse('preorder')):
        if n.is_root():
            n.name = 'root'
        elif not n.is_leaf():
            n.name = 'n{}'.format(i)

    tree.write(outfile=params.out_nwk, format_root_node=True, format=3,
               features=[DATE, DATE_CI])

