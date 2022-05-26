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

ranking.py provides a set of functions used to create a morph "tier list",
ranking morphs based on their ability to fool a facial recognition system.

  Typical usage example:

  TODO
"""

import csv
from itertools import zip_longest
import json
import os
import pandas
import shutil
from utils import Rank


def rank_morphs(morph_details: str, threshold: float
                ) -> dict[Rank.A: list[str], Rank.B: list[str], Rank.C: list[str]]:
  """Ranks morphs into the categories provided by class Rank.

  Args:
    morph_details: the path to a directory containing a morph details file.
    threshold: the recognition distance threshold to use when ranking morphs.

  Returns:
    A dict of lists in the format

    {
     Rank.A: list_of_rank_A_morphs,
     Rank.B: list_of_rank_B_morphs,
     Rank.C: list_of_rank_C_morphs
    }

  """
  rankA = []
  rankB = []
  rankC = []
  details = {}
  with open(morph_details, 'r') as f:
    details = json.load(f)

  for morph in details.keys():
    morph_name = morph.split('.')[0]
    distanceA = details[morph]['distanceA']
    distanceB = details[morph]['distanceB']

    if distanceA < threshold and distanceB < threshold:
        rankA.append(morph_name)
    elif distanceA < threshold and distanceB >= threshold:
      rankB.append(morph_name)
    elif distanceA >= threshold and distanceB < threshold:
      rankB.append(morph_name)
    else:
      rankC.append(morph_name)

  return {Rank.A: rankA,
          Rank.B: rankB,
          Rank.C: rankC
          }


def copy_ranked_morphs_csvs(morph_csv_dir: str, dest_dir: str, ranks: dict[Rank, list]) -> None:
  """
  Copies a set of ranked morphs' csvs given by rank_morphs to their own folders.

  Args:
    morph_csv_dir: the path to a directory containing morph images.
    dest_dir: the path to a directory within which to create rank
      directories within which to store ranked morphs.
    ranks: output dictionary from rank_morphs()
  """

  folder_names = ['rank_a', 'rank_b', 'rank_c']

  if not os.path.isdir(dest_dir):
    os.mkdir(dest_dir)

  for name in folder_names:
    if not os.path.isdir(dest_dir + '/' + name):
      os.mkdir(dest_dir + '/' + name)

  morph_0 = os.listdir(morph_csv_dir)[0]

  file_ext = morph_0[morph_0.find('.') + 1:]

  for morph_A in ranks[Rank.A]:
    shutil.copy(morph_csv_dir + '/' + morph_A + '.' + file_ext, dest_dir + '/' + folder_names[0])

  for morph_B in ranks[Rank.B]:
    shutil.copy(morph_csv_dir + '/' + morph_B + '.' + file_ext, dest_dir + '/' + folder_names[1])

  for morph_C in ranks[Rank.C]:
    shutil.copy(morph_csv_dir + '/' + morph_C + '.' + file_ext, dest_dir + '/' + folder_names[2])


def export_ranked_morphs(morph_details: str, threshold: float, outfile: str) -> None:
  '''
  Uses rank_morphs() to rank a set of morphs and then exports the
  rankings to a csv file in a human-readable format.
  '''

  ranks = rank_morphs(morph_details, threshold)

  ranks_export = {}

  ranks_export['Rank A'] = ranks[Rank.A]
  ranks_export['Rank B'] = ranks[Rank.B]
  ranks_export['Rank C'] = ranks[Rank.C]

  with open(outfile, 'w') as f:
    json.dump(ranks_export, f)

