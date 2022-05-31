import det_curve
import json
import mmpmr
import numpy as np


def main():

  gamma_step = 0.001
  gamma_list = np.arange(0, 2 + gamma_step, gamma_step)

  clarkson_morphs = [
      'clarkson_morphs_l2',
      'ranking_subsets/clarkson_subset_l2/rank_a',
      'ranking_subsets/clarkson_subset_l2/rank_b',
      'ranking_subsets/clarkson_subset_l2/rank_c']

  clarkson_s_morphs = [
      'clarkson_morphs_scanned_l2',
      'ranking_subsets/clarkson_scanned_subset_l2/rank_a',
      'ranking_subsets/clarkson_scanned_subset_l2/rank_b',
      'ranking_subsets/clarkson_scanned_subset_l2/rank_c']

  frll_morphs = [
      'frll_morphs_l2',
      'ranking_subsets/frll_subset_l2/rank_a',
      'ranking_subsets/frll_subset_l2/rank_b',
      'ranking_subsets/frll_subset_l2/rank_c']

  frll_s_morphs = [
      'frll_morphs_scanned_l2',
      'ranking_subsets/frll_scanned_subset_l2/rank_a',
      'ranking_subsets/frll_scanned_subset_l2/rank_b',
      'ranking_subsets/frll_scanned_subset_l2/rank_c']

  xy = []

  for morph in frll_s_morphs:
    xy.append(det_curve.gen_det_curve(
        '../data/stats/nearface_out/morphs/' + morph,
        '../data/stats/nearface_out/stills/frll_stills_l2_threshold',
        gamma_step))

    with open('../data/stats/det_curves/' + morph.replace('/', '_') + '_det_curve.json', 'w') as f:
      json.dump(xy[-1], f)

    print(morph + ':')

    det_curve.det_curve_stats(xy[-1])

    tau = gamma_list[min(range(len(xy[-1][0])), key=lambda i: abs(xy[-1][0][i] - 0.001))]

    print('Tau @ APCER=10^-3: ' + str(tau))

  det_curve.plot_multiple_det_curve(
      xy[0],
      'FRLL L2 Print & Scan DET Curves',
      xy[1],
      xy[2],
      xy[3],
      xy0_label='All Ranks',
      xy1_label='Rank A',
      xy2_label='Rank B',
      xy3_label='Rank C')


if __name__ == '__main__':
  main()
