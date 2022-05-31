import matplotlib.pyplot as plt
import pandas
import os
from tqdm import tqdm


def calc_mmpmr(morphs_csvs_dir: str, tau: list[float], distance_label: str):
  """Calculates MMPMR (Mated Morph Presentation Match Rate) for a fixed tau.

  Refer to: https://www.christoph-busch.de/files/Scherhag-Methodology-BIOSIG-2017.pdf

  Uses the first image of each of the two morph composition
  subjects to calculate MMPMR.

  Stills must be named using the format:
    id_imagenum
  Morphs must be named using the format:
    still1-still2

  Args:
    morphs_csvs_dir: a path to a folder containing csv files
      that contain comparison scores from a morph to all
      stills.
    tau: a list of taus to calculate MMPMR for (can be used
      to create graphs of tau vs. MMPMR).
    distance_label: the csv file label for distances 
      (ex. 'VGG-Face_cosine', 'VGG-Face_euclidean_l2', etc.)
  """

  # print(os.listdir(morphs_csvs_dir))

  mmpmr_sum: dict[float:float] = {}

  M: int = len(os.listdir(morphs_csvs_dir))

  for morph_csv in tqdm(os.listdir(morphs_csvs_dir)):
    morph_csv = morphs_csvs_dir + '/' + morph_csv
    df = pandas.read_csv(morph_csv, sep='\t')
    df.drop(columns=['Unnamed: 0'], inplace=True)
    for i in range(len(df)):
      df.at[i, 'identity'] = df['identity'][i].split('/')[-1]

    identity_1 = morph_csv.split('/')[-1].split('-')[0].split('_')[0]
    identity_2 = morph_csv.split('/')[-1].split('-')[1].split('.')[0].split('_')[0]

    identity_1_distances = []
    identity_2_distances = []

    for i in range(len(df)):
      if df['identity'][i].split('_')[0] == identity_1:
        identity_1_distances.append(df[distance_label][i])
      elif df['identity'][i].split('_')[0] == identity_2:
        identity_2_distances.append(df[distance_label][i])
      else:
        pass
    
    try:
      first_id_distances = [identity_1_distances[0], identity_2_distances[0]]
    except IndexError:
      print("No comparison image found for morph " + str(morph_csv) + '. Skipping.')
      continue

    for t in tau:
      if max(first_id_distances) > t:
        if t in mmpmr_sum.keys():
          mmpmr_sum[t] += max(first_id_distances)
        else:
          mmpmr_sum[t] = max(first_id_distances)

  result = []

  for t in mmpmr_sum.keys():
    result.append(1 / M * mmpmr_sum[t])

  return result
    

if __name__ == '__main__':
  # Example usage
  tau = [0.0]
  res = calc_mmpmr('../data/stats/nearface_out/morphs/ranking_subsets/frll_scanned_subset_l2/rank_c', tau, 'VGG-Face_euclidean_l2')
  
  # print(tau)
  print(res)
