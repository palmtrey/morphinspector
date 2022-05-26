"""
Morph Inspector
Copyright (C) 2022  Cameron M Palmer [https://github.com/palmtrey/morphinspector]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/].

=================================================================================

roc_curve.py provides functions for generating and plotting receiver operating 
characteristic (ROC) curves in order to judge the quality of morphs. It is desired 
that there is a linear relationship between the false positive rate (FPR, x-axis) 
and the true positive rate (TPR, y-axis) for morphs to perform well.

    Typical usage example:

    xy = gen_roc_curve('morph_csvs_dir', 'still_csvs_dir', 0.001)
    plot_roc_curve(xy)
"""


import os
import shutil
import matplotlib.pyplot as plt
from nearface import NearFace
import numpy as np
from tqdm import tqdm
import utils


def compare_stills(stills_dir: str, output_dir: str, still_id: str, use_threshold=False) -> None:
  """Uses NearFace to compare one still to all others.

  Takes a still and compares it to all the other stills, excluding itself.
  Writes a NearFace dump csv file for the still containing l2 distance data.

  Args:
    stills_dir: the path to a directory containing stills.
    output_dir: the path to a directory in which to write the NearFace
      dump csvs.
    still_id: the id of the still to compare. Example: '00'

  Raises:
    AttributeError: An error occurred when making a comparison.
      The problematic still will be skipped if this is raised.
  """
  temp_dir = 'temp'

  id_files = []

  for filename in os.listdir(stills_dir):
    if filename.startswith(still_id + '_'):
      id_files.append(filename)

  # Copy necessary images to a temp folder. Send this temp
  # folder to nearface.
  if not os.path.isdir(temp_dir):
    os.mkdir(temp_dir)
  for filename in id_files:
    shutil.copy(stills_dir + '/' + filename, temp_dir + '/' + filename)

  for still in tqdm(id_files):
    try:
      df = NearFace.find(
          img_path=stills_dir + '/' + still,
          db_path=temp_dir,
          distance_metric='euclidean_l2',
          enforce_detection=False,
          use_threshold=use_threshold
      )

      if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

      df.to_csv(output_dir + '/' + still + '.csv', sep='\t')

    except AttributeError:
      print('AttributeError encountered... skipping still ' + still)

  shutil.rmtree(temp_dir)


def compare_all_stills(stills_dir: str,
                       output_dir: str,
                       ids: list = [],
                       compare_all: bool = False,
                       use_threshold=False
                       ):
  """Makes many still comparisons by calling compare_stills multiple times."""

  if compare_all:
    stills = os.listdir(stills_dir)
    for still in stills:
      ids.append(still.split('_')[0])

  for id in tqdm(ids):
    compare_stills(stills_dir, output_dir, id, use_threshold=use_threshold)


def gen_roc_curve(morphs_csvs_dir: str, stills_csvs_dir: str, gamma_step: float) -> tuple[list]:
  """Generates x and y data for an ROC curve.

  Generates the data for an ROC curve given NearFace csvs for morphs
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

    where x and y are both lists of float values, x is false positive rate
    (FPR), y is true positive rate (TPR) for all gamma.
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

    id_a_avg = np.mean(list(id_a.values()))
    id_b_avg = np.mean(list(id_b.values()))

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
    # Regular below
    FP = result_dict[gamma]['FP']
    TN = result_dict[gamma]['TN']
    TP = result_dict[gamma]['TP']
    FN = result_dict[gamma]['FN']

    # Zander's inverted below
    # FN = result_dict[gamma]['FP']
    # TP = result_dict[gamma]['TN']
    # TN = result_dict[gamma]['TP']
    # FP = result_dict[gamma]['FN']

    # Actual inverted below
    # TP = result_dict[gamma]['FP']
    # FN = result_dict[gamma]['TN']
    # FP = result_dict[gamma]['TP']
    # TN = result_dict[gamma]['FN']

    #print('FN + TP: ' + str(FN+TP))
    #print('TN + FP: ' + str(TN+FP))

    result_dict[gamma]['TPR'] = TP / (TP + FN)
    result_dict[gamma]['FPR'] = FP / (FP + TN)

  x = []  # false positive rate
  y = []  # true positive rate

  for label in result_dict.keys():
    x.append(result_dict[label]['FPR'])
    y.append(result_dict[label]['TPR'])

  return (x, y)


def plot_roc_curve(xy: tuple[list[float], list[float]], plot_title: str) -> None:
  """Plots an ROC curve given its x and y coordinate data.

  Args:
    xy: a tuple containing two lists of floats. The first is the
      data for the x-axis, the false positive rate. The second
      is the data for the y-axis, the true positive rate.
    plot_title: the title to label the roc curve plot with

  """

  # x = FPR
  x = xy[0]

  # y = TPR
  y = xy[1]

  plt.scatter(x, y, s=3)
  plt.title(plot_title)
  plt.xlabel("False Positive Rate")
  plt.ylabel("True Positive Rate")
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.show()


def plot_multiple_roc_curve(
    xy0: tuple[list[float]],
    plot_title: str,
    xy1: tuple[list[float]] = None,
    xy2: tuple[list[float]] = None,
    xy3: tuple[list[float]] = None,
    xy0_label: str = '',
    xy1_label: str = '',
    xy2_label: str = '',
    xy3_label: str = ''):
  """Same as plot_roc_curve, except can plot up to four curves on one plot."""

  size = 3

  # x = FPR
  # y = TPR

  plt.scatter(xy0[0], xy0[1], s=size, label=xy0_label)

  if xy1 is not None:
    plt.scatter(xy1[0], xy1[1], s=size, label=xy1_label)

  if xy2 is not None:
    plt.scatter(xy2[0], xy2[1], s=size, label=xy2_label)

  if xy3 is not None:
    plt.scatter(xy3[0], xy3[1], s=size, label=xy3_label)

  plt.title(plot_title)
  plt.xlabel("False Positive Rate")
  plt.ylabel("True Positive Rate")
  plt.legend(loc='upper right')
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.show()