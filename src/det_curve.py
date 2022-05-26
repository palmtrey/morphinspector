import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm
import utils


def gen_det_curve(morphs_csvs_dir: str, stills_csvs_dir: str, gamma_step: float) -> tuple[list]:
  """Generates x and y data for a DET curve.

  Generates the data for a DET curve given NearFace csvs for morphs
  (compared to all stills), a directory of stills, and an increment
  to step gamma (the recognition threshold) by.


  Args:
  morphs_csvs_dir: path to a directory containing csvs for morphs
    output by nearface.
  stills_dir: path to a directory containing all still images.
  gamma_step: a value by which to increment gamma by. Lower
    gamma_step will lead to more data and a higher resolution ROC
    curve.

  Returns:
  x and y coordinate data for the roc curve in the form

  tuple(x, y)

  where x and y are both lists of float values, x is APCER, y is
  BPCER for all gamma.
  """

  # Create a list of all morph names
  morphs = []

  for file in os.listdir(morphs_csvs_dir):
    morphs.append(file.split('.')[0])

  FP = 0
  TN = 0

  gamma_list = np.arange(0, 2 + gamma_step, gamma_step)

  result_dict = {}

  for gamma in gamma_list:
    result_dict[gamma] = {'FP': 0, 'TN': 0, 'TP': 0, 'FN': 0, 'TPR': 0.0, 'FPR': 0.0}

  # Start with morph compared to identities (these all should be negative/zero)
  print('Retrieving data from morphs...')
  for file in tqdm(os.listdir(morphs_csvs_dir)):
    a_b = utils.import_morph_nearface_csv(morphs_csvs_dir + '/' + file)
    id_a = a_b[0]
    id_b = a_b[1]

    id_a_avg = np.nanmean(list(id_a.values()))
    id_b_avg = np.nanmean(list(id_b.values()))

    for gamma in gamma_list:
      if not utils.classify(id_a_avg, gamma): # This should yield a 0 from the FRS
        result_dict[gamma]['TP'] += 1
      else:
        result_dict[gamma]['FN'] += 1

  # for distance in id_b.values():
    if not utils.classify(id_b_avg, gamma):
      result_dict[gamma]['TP'] += 1
    else:
      result_dict[gamma]['FN'] += 1

  # Then compare stills to stills
  print('Retrieving data from stills...')
  for file in tqdm(os.listdir(stills_csvs_dir)):
    id = utils.import_still_nearface_csv(stills_csvs_dir + '/' + file)

    for gamma in gamma_list:
      for distance in id.values():
        if distance != 0:
          if utils.classify(distance, gamma): # This should yield a 1 from the FRS
            result_dict[gamma]['TN'] += 1
          else:
            result_dict[gamma]['FP'] += 1

  # Calculate true positive rate and false positive rate for each gamma
  for gamma in result_dict.keys():
    # Regular
    FP = result_dict[gamma]['FP']
    TN = result_dict[gamma]['TN']
    TP = result_dict[gamma]['TP']
    FN = result_dict[gamma]['FN']

    # Zander's inverted
    # FN = result_dict[gamma]['FP']
    # TP = result_dict[gamma]['TN']
    # TN = result_dict[gamma]['TP']
    # FP = result_dict[gamma]['FN']

    # Actual inverted
    # TP = result_dict[gamma]['FP']
    # FN = result_dict[gamma]['TN']
    # FP = result_dict[gamma]['TP']
    # TN = result_dict[gamma]['FN']

    result_dict[gamma]['APCER'] = FN / (TP + FN)
    result_dict[gamma]['BPCER'] = FP / (FP + TN)

  x = []  # false positive rate
  y = []  # true positive rate

  for label in result_dict.keys():
    x.append(result_dict[label]['APCER'])
    y.append(result_dict[label]['BPCER'])

  return (x, y)


def plot_det_curve(xy: tuple[list[float], list[float]], plot_title: str) -> None:
  """Plots a DET curve given its x and y coordinate data.

  Args:
  xy: a tuple containing two lists of floats. The first is the
    data for the x-axis, the APCER. The second
    is the data for the y-axis, the BPCER.
  plot_title: the title to label the DET curve plot with.

  """

  # x = APCER
  x = xy[0]

  # y = BPCER
  y = xy[1]

  plt.scatter(x, y, s=3)
  plt.title(plot_title)
  plt.xlabel("APCER")
  plt.ylabel("BPCER")
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.show()


def det_curve_stats(xy: tuple[list[float], list[float]]) -> None:
  """Prints out four statistics for a given DET curve.
  
  Stats printed:
    APCER @ BPCER = 1.0
    APCER @ BPCER = 0.1
    APCER @ BPCER = 0.05
    APCER @ BPCER = 0.01
  """
  
  apcer = xy[0]
  bpcer = xy[1]

  print('APCER @ BPCER = 1.0: ' + str(apcer[min(range(len(bpcer)), key=lambda i: abs(bpcer[i]-1.0))]))
  print('APCER @ BPCER = 0.1: ' + str(apcer[min(range(len(bpcer)), key=lambda i: abs(bpcer[i]-0.1))]))
  print('APCER @ BPCER = 0.05: ' + str(apcer[min(range(len(bpcer)), key=lambda i: abs(bpcer[i]-0.05))]))
  print('APCER @ BPCER = 0.01: ' + str(apcer[min(range(len(bpcer)), key=lambda i: abs(bpcer[i]-0.01))]))


def plot_multiple_det_curve(
    xy0: tuple[list[float]],
    plot_title: str,
    xy1: tuple[list[float]] = None,
    xy2: tuple[list[float]] = None,
    xy3: tuple[list[float]] = None,
    xy0_label: str = '',
    xy1_label: str = '',
    xy2_label: str = '',
    xy3_label: str = ''):

  """Same as plot_det_curve, except can plot up to four curves on one plot."""

  size = 3

  plt.scatter(xy0[0], xy0[1], s=size, label=xy0_label)

  if xy1 is not None:
    plt.scatter(xy1[0], xy1[1], s=size, label=xy1_label)

  if xy2 is not None:
    plt.scatter(xy2[0], xy2[1], s=size, label=xy2_label)

  if xy3 is not None:
    plt.scatter(xy3[0], xy3[1], s=size, label=xy3_label)

  plt.title(plot_title)
  plt.xlabel("APCER")
  plt.ylabel("BPCER")
  plt.legend(loc='upper right')
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.show()
