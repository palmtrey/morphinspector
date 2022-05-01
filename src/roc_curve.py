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
import pandas
from tqdm import tqdm


def import_morph_nearface_csv(csv_file: str) -> tuple[dict]:
  """Imports a csv containing morph distances.

  Imports a morph csv created by NearFace and returns a tuple of
  two dicts, the first containing the distances to identity 1,
  the second containing the distances to identity 2.

  Args:
    csv_file: A path to a morph's csv file generated
      by NearFace.

  Returns:
    A tuple containing two dicts in the format

    tuple(identity_1_dict, identity_2_dict)

    where each dict is in the format

    {still_1: distance_to_morph, still_2: ...}

  """

  distance_label = 'VGG-Face_euclidean_l2'

  df = pandas.read_csv(csv_file, sep='\t')
  df.drop(columns=['Unnamed: 0'], inplace=True)
  for i in range(len(df)):
    df.at[i, 'identity'] = df['identity'][i].split('/')[-1]

  identity_1 = csv_file.split('/')[-1].split('-')[0].split('_')[0]
  identity_2 = csv_file.split('/')[-1].split('-')[1].split('.')[0].split('_')[0]

  identity_1_distances = {}
  identity_2_distances = {}

  for i in range(len(df)):
    if df['identity'][i].split('_')[0] == identity_1:
      identity_1_distances[df['identity'][i]] = df[distance_label][i]
    elif df['identity'][i].split('_')[0] == identity_2:
      identity_2_distances[df['identity'][i]] = df[distance_label][i]

  return (identity_1_distances, identity_2_distances)


def import_still_nearface_csv(csv_file: str) -> dict:
  """Imports a csv containing still distances.

  Imports a still csv created by NearFace and returns a dict
  containing distances from the given still to all other stills.

  Args:
    csv_file: A path to a still's csv file generated
      by NearFace.

  Returns:
    A dict in the format

    {still_1: dist_to_given_still, still_2: ...}

  """
  distance_label = 'VGG-Face_euclidean_l2'

  df = pandas.read_csv(csv_file, sep='\t')
  df.drop(columns=['Unnamed: 0'], inplace=True)
  for i in range(len(df)):
    df.at[i, 'identity'] = df['identity'][i].split('/')[-1]

  result_dict = {}
  for i in range(len(df)):
    result_dict[df['identity'][i]] = df[distance_label][i]

  return result_dict


def classify(dist: float, gamma: float) -> bool:
  """Classifies a distance as recognized or not.

  Args:
    dist: The distance to classify.
    gamma: The threshold to compare against.

  Returns:
    True if dist < gamma, false otherwise.

  """
  if dist < gamma:
    return True   # Face recognized (positive)
  else:
    return False  # Face not recognized (negative)


def compare_stills(stills_dir: str, output_dir: str, still_id: str) -> None:
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
          use_threshold=False
      )

      if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

      df.to_csv(output_dir + '/' + still + '.csv', sep='\t')

    except AttributeError:
      print('AttributeError encountered... skipping still ' + still)

  shutil.rmtree(temp_dir)


def compare_all_stills(stills_dir: str, output_dir: str, ids: list = [], compare_all: bool = False):
  """Makes many still comparisons by calling compare_stills multiple times."""

  if compare_all:
    stills = os.listdir(stills_dir)
    for still in stills:
      ids.append(still.split('_')[0])

  for id in tqdm(ids):
    compare_stills(stills_dir, output_dir, id)


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
    a_b = import_morph_nearface_csv(morphs_csvs_dir + '/' + file)
    id_a = a_b[0]
    id_b = a_b[1]

    for gamma in gamma_list:
      for distance in id_a.values():
        if classify(distance, gamma):
          result_dict[gamma]['FP'] += 1
        else:
          result_dict[gamma]['TN'] += 1

      for distance in id_b.values():
        if classify(distance, gamma):
          result_dict[gamma]['FP'] += 1
        else:
          result_dict[gamma]['TN'] += 1

  # Then compare stills to stills
  print('Retrieving data from stills...')
  for file in tqdm(os.listdir(stills_csvs_dir)):
    id = import_still_nearface_csv(stills_csvs_dir + '/' + file)

    for gamma in gamma_list:
      for distance in id.values():
        if distance != 0:
          if classify(distance, gamma):
            result_dict[gamma]['TP'] += 1
          else:
            result_dict[gamma]['FN'] += 1

  # Calculate true positive rate and false positive rate for each gamma
  for gamma in result_dict.keys():
    FP = result_dict[gamma]['FP']
    TN = result_dict[gamma]['TN']
    TP = result_dict[gamma]['TP']
    FN = result_dict[gamma]['FN']

    result_dict[gamma]['TPR'] = TP / (TP + FN)
    result_dict[gamma]['FPR'] = FP / (FP + TN)

  x = []  # false positive rate
  y = []  # true positive rate

  for label in result_dict.keys():
    x.append(result_dict[label]['FPR'])
    y.append(result_dict[label]['TPR'])

  return (x, y)


def plot_roc_curve(xy: tuple[list[float], list[float]], plot_title: str) -> None:
  """Plots a ROC curve given its x and y coordinate data.

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
  plt.plot(x, y)
  plt.title(plot_title)
  plt.xlabel("False Positive Rate")
  plt.ylabel("True Positive Rate")
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.show()
