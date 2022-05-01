import json
import ranking
import roc_curve
import utils


def main():
    # ranks = ranking.rank_morphs('../data/stats/details_frll_scanned_l2.txt', 0.86)  # 0.86 is default l2 threshold
    # print('Rank A morph count: ' + str(len(ranks[utils.Rank.A])))
    # print('Rank B morph count: ' + str(len(ranks[utils.Rank.B])))
    # print('Rank C morph count: ' + str(len(ranks[utils.Rank.C])))

    # ranking.copy_ranked_morphs_csvs('../data/nearface_out/morphs/frll_morphs_scanned_l2',
    #                                 '../data/ranking_subsets/frll_scanned_subset_l2',
    #                                 ranks)

    # roc_names = ['roc_curveA.json', 'roc_curveB.json', 'roc_curveC.json', 'roc_curveAll.json']
    # roc_locs = ['../data/ranking_subsets/frll_scanned_subset_l2/rank_a',
    #             '../data/ranking_subsets/frll_scanned_subset_l2/rank_b',
    #             '../data/ranking_subsets/frll_scanned_subset_l2/rank_c',
    #             '../data/nearface_out/morphs/frll_morphs_scanned_l2']

    # for i in range(0, 4):
    #     xy = roc_curve.gen_roc_curve(roc_locs[i],
    #                                  '../data/nearface_out/stills/frll_stills_l2',
    #                                  0.001)

    #     with open('../data/roc_curves/frll_scanned_l2/' + roc_names[i], 'w') as f:
    #         json.dump(xy, f)

    # roc_labels = ['Rank A', 'Rank B', 'Rank C', 'All Ranks']
    # roc_path = '../data/roc_curves/frll_scanned_l2/'

    # for i in range(0, 4):
    #     with open(roc_path + roc_names[i], 'r') as f:
    #         xy = json.load(f)

    #     roc_curve.plot_roc_curve(xy, roc_labels[i])
    pass

if __name__ == '__main__':
    main()
