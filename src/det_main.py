import det_curve
import json


def main():

  clarkson_morphs = [
      'clarkson_morphs_l2',
      'ranking_subsets/clarkson_subset_l2/rank_a',
      'ranking_subsets/clarkson_subset_l2/rank_b'
      'ranking_subsets/clarkson_subset_l2/rank_c']

  clarkson_s_morphs = [
      'clarkson_morphs_scanned_l2',
      'ranking_subsets/clarkson_scanned_subset_l2/rank_a',
      'ranking_subsets/clarkson_scanned_subset_l2/rank_b'
      'ranking_subsets/clarkson_scanned_subset_l2/rank_c']

  frll_morphs = [
      'frll_morphs_l2',
      'ranking_subsets/frll_subset_l2/rank_a',
      'ranking_subsets/frll_subset_l2/rank_b'
      'ranking_subsets/frll_subset_l2/rank_c']

  frll_s_morphs = [
      'frll_morphs_scanned_l2',
      'ranking_subsets/frll_scanned_subset_l2/rank_a',
      'ranking_subsets/frll_subset_l2/rank_b'
      'ranking_subsets/frll_subset_l2/rank_c']

  xy = []

  for morph in clarkson_morphs:
    xy.append(det_curve.gen_det_curve(
        '../data/stats/nearface_out/morphs/' + morph,
        '../data/stats/nearface_out/stills/clarkson_stills_l2_threshold',
        0.001))

    with open('../data/stats/det_curves/' + morph + '_det_curve.json', 'w') as f:
      json.dump(xy[-1], f)

    print(morph + ':')

    det_curve.det_curve_stats(xy)

  det_curve.plot_multiple_det_curve(xy[0], 'Clarkson L2 DET Curves')


if __name__ == '__main__':
  main()
