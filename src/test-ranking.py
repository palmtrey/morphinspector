import json
import ranking
import roc_curve
import utils


def main():
    # ranks = ranking.rank_morphs('../data/stats/details_l2.txt', 0.8)
    # print('Rank A morph count: ' + str(len(ranks[utils.Rank.A])))
    # print('Rank B morph count: ' + str(len(ranks[utils.Rank.B])))
    # print('Rank C morph count: ' + str(len(ranks[utils.Rank.C])))

    # ranking.copy_ranked_morphs_csvs('../data/nearface_out/morphs/csvs_renamed_all_l2',
    #                                 '../data/nearface_out/morphs/subset',
    #                                 ranks)

    # xy = roc_curve.gen_roc_curve('../data/nearface_out/morphs/subset/rank_c',
    #                              '../data/nearface_out/stills/nearface_dump_stills_l2',
    #                              0.001)

    with open('roc_curveA.json', 'r') as f:
        xy = json.load(f)

    roc_curve.plot_roc_curve(xy, 'Rank A Morphs ROC Curve')


if __name__ == '__main__':
    main()
