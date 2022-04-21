import csv
import json
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import pandas
from scipy.stats import wasserstein_distance
from tqdm import tqdm

class Morph():
  '''
  A class for representing a morph and all the data attached to it.
  '''

  def __init__(self, morph_path:str, stills_dir:str, still_ext:str, csv_cosine_path:str='', csv_l2_path:str='', details_cosine_path:str='', details_l2_path:str=''):
    self.morph_path = morph_path
    self.morph_ext = self.morph_path.split('.')[-1]
    self.stills_dir = stills_dir


    self.still1 = get_stills_from_morph(morph_path)[0]
    self.still2 = get_stills_from_morph(morph_path)[1]
    self.still1_id = self.still1.split('_')[0]
    self.still2_id = self.still2.split('_')[0]
    self.still_ext = still_ext
    self.still1_path = stills_dir + '/' + self.still1 + self.still_ext
    self.still2_path = stills_dir + '/' + self.still2 + self.still_ext


    # Append all stills of each id into a list
    self.all_still1 = []
    self.all_still2 = []

    for still in os.listdir(stills_dir):
      if still.split('/')[-1].split('_')[0] == self.still1_id:
        self.all_still1.append(still)
      
      if still.split('/')[-1].split('_')[0] == self.still2_id:
        self.all_still2.append(still)

    self.csv_cosine_path = csv_cosine_path
    self.csv_l2_path = csv_l2_path

    if csv_cosine_path != None:
      self.details_cosine = calc_morphdetails(self.csv_cosine_path, 'VGG-Face_cosine', self.morph_ext)
    elif details_cosine_path != '':
      with open(details_cosine_path) as file:
        self.details_cosine = json.load(file)
        self.details_cosine = self.details_cosine[self.get_morph() + '.csv']
    else:
      self.details_cosine = None

    if csv_l2_path != None:
      self.details_l2 = calc_morphdetails(self.csv_l2_path, 'VGG-Face_euclidean_l2', self.morph_ext)
    elif details_l2_path != '':
      with open(details_l2_path) as file:
        self.details_l2 = json.load(file)
      self.details_l2 = self.details_l2[self.get_morph() + '.csv']
    else:
      self.details_l2 = None

  def get_details(self, type:str) -> dict:
    result = {}
    result['morphscore'] = self.get_morphscore(type)
    result['distanceA'] = self.get_distanceA(type)
    result['distanceB'] = self.get_distanceB(type)
    result['1-wasserstein'] = self.get_emd(type)
    return result

  def get_morphscore(self, type:str) -> float:
    if type == 'cosine':
      if self.details_cosine == None:
        raise TypeError('morph does not contain a cosine morphscore')
      else:
        return self.details_cosine['morphscore']

    elif type == 'l2':
      if self.details_l2 == None:
        raise TypeError('morph does not contain an l2 morphscore')
      else:
        return self.details_l2['morphscore']
    else:
      raise IndexError(type + ' is not a valid distance metric.')
  
  def get_distanceA(self, type:str) -> float:
    if type == 'cosine':
      if self.details_cosine == None:
        raise TypeError('morph does not contain a cosine distance A')
      else:
        return self.details_cosine['distanceA']
    elif type == 'l2':
      if self.details_l2 == None:
        raise TypeError('morph does not contain an l2 distance A')
      else:
        return self.details_l2['distanceA']
    else:
      raise IndexError(type + ' is not a valid distance metric.')

  def get_distanceB(self, type:str) -> float:
    if type == 'cosine':
      if self.details_cosine == None:
        raise TypeError('morph does not contain a cosine distance B')
      else:
        return self.details_cosine['distanceB']
    elif type == 'l2':
      if self.details_l2 == None:
        raise TypeError('morph does not contain an l2 distance B')
      else:
        return self.details_l2['distanceB']
    else:
      raise IndexError(type + ' is not a valid distance metric.')

  def get_emd(self, type:str) -> float:
    if type == 'cosine':
      if self.details_cosine == None:
        raise TypeError("morph does not contain a cosine earth mover's / 1-wasserstein distance")
      else:
        return self.details_cosine['1-wasserstein']
    elif type == 'l2':
      if self.details_l2 == None:
        raise TypeError("morph does not contain an l2 earth mover's / 1-wasserstein distance")
      else:
        return self.details_l2['1-wasserstein']
    else:
      raise IndexError(type + ' is not a valid distance metric.')

  def get_morph_path(self) -> str:
    return self.morph_path

  def get_stills_dir(self) -> str:
    return self.stills_dir

  def get_still1_path(self) -> str:
    return self.still1_path
  
  def get_still2_path(self) -> str:
    return self.still2_path

  def get_morph(self) -> str:
    return self.get_morph_path().split('/')[-1]
  
  def get_still1(self) -> str:
    return self.get_still1_path().split('/')[-1]
  
  def get_still2(self) -> str:
    return self.get_still2_path().split('/')[-1]

  def get_still1_id(self) -> str:
    return self.still1_id

  def get_still2_id(self) -> str:
    return self.still2_id

  def get_all_still1(self) -> list:
    return self.all_still1

  def get_all_still2(self) -> list:
    return self.all_still2





    
def get_stills_from_morph(morph:str) -> list:
  return [morph.split('/')[-1].split('-')[0].split('.')[0], morph.split('/')[-1].split('-')[1].split('.')[0]]


def calc_morphscore(morph_csv:str, distance_label:str, morph_ext:str = '.png') -> float:
  '''
  Calculates a morphscore for a given morph's csv using the MorphScore Equation.

  Preconditions:
    - morph_csv is a valid path to a morph's csv file containing still comparisons,
      using the naming convention below:
        still_1-still_2.morph_ext.csv
    - the morph's csv file is formatted using tab separators
  
  Postconditions:
    - None
  
  Parameters:
    - morph_csv: a valid path to a morph's csv comparison file
    - morph_ext: the morph's file extension
    - distance_label: the csv file label for distances (ex. 'VGG-Face_cosine', 'VGG-Face_euclidean_l2', etc.)
  '''

  if morph_csv == '':
    return float(-1)

  # Prepare incoming csv file
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

  n = len(identity_1_distances)
  p = len(identity_2_distances)

  morphscore = 2 / (1/n * sum(identity_1_distances) + 1/p * sum(identity_2_distances))

  return morphscore

def calc_morphdetails(morph_csv:str, distance_label:str, morph_ext:str = '.png') -> dict:
  '''
  Calculates various metrics for rating a given morph and returns them in a dictionary

  Preconditions:
    - morph_csv is a valid path to a morph's csv file containing still comparisons,
      using the naming convention below:
        still_1-still_2.morph_ext.csv
    - the morph's csv file is formatted using tab separators
  
  Postconditions:
    - None
  
  Parameters:
    - morph_csv: a valid path to a morph's csv comparison file
    - morph_ext: the morph's file extension
    - distance_label: the csv file label for distances (ex. 'VGG-Face_cosine', 'VGG-Face_euclidean_l2', etc.)
  '''


  # Prepare incoming csv file
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

  result = {}
  result['morphscore'] = calc_morphscore(morph_csv, distance_label, morph_ext)
  result['distanceA'] = np.mean(identity_1_distances)
  result['distanceB'] = np.mean(identity_2_distances)
  result['1-wasserstein'] = wasserstein_distance(identity_1_distances, identity_2_distances)

  return result


def writescores(morph_csvs_dir:str, output_file:str, distance_label:str) -> None:
  '''
  Writes MorphScores for all morphs csvs stored in morph_csvs_dir to an output file, output_file (a txt file)

  Preconditions: 
    - morphs_csvs_dir is a valid directory containing validly formatted csvs
  
  Postconditions:
    - output_file is a .txt file containing a dictionary of morphs (keys) and scores (values)

  Parameters:
    - morphs_csvs_dir: a valid path to a directory containing morph csvs
    - output_file: a file to create to output a dictionary of morphscores
    - distance_label: this will change based on what kind of distance 
      metric was used when creating the morph csv files. Some common settings
      are listed below:
        cosine: 'VGG-Face_cosine'
        L2 euclidian: 'VGG-Face_euclidean_l2'
  '''

  scores = {}
  for csv in tqdm(os.listdir(morph_csvs_dir)):
    scores[csv] = calc_morphdetails(morph_csvs_dir + '/' + csv, distance_label)

  with open(output_file, 'w') as file:
    file.write(json.dumps(scores))


def plotscores(scores_file:str) -> None:
  '''
  Plots a histogram of MorphScores, given a MorphScore .txt file

  Preconditions:
    - scores_file is the path to a valid .txt morphscores file created with writescores()
  
  Postconditions:
    - None

  Parameters:
    - scores_file: the morphscores file to use
  '''

  scores = {}
  with open(scores_file) as file:
    scores = json.load(file)
  

  plt.hist(scores.values(), bins=100)
  plt.show()

def show_morphs(morphs_dir:str, stills_dir:str, scores_file:str, ms_threshold:float=0.0, still_ext:str='.jpg'):
  '''
  Iterates through morphs, showing a morph and its composite stills, along with its morph score beneath

  Preconditions:
    - morphs_dir and stills_dir are valid directories containing morphs and stills
    - stills use the extension still_ext, which defaults to '.jpg'
    - scores_file is the path to a valid .txt morphscores file created with writescores()

  Postconditions:
    - None
  
  Parameters:
    - morphs_dir: the directory containing morphs
    - stills_dir: the directory containing stills
    - scores_file: the path to a .txt morphscores file
    - ms_threshold: the low-end threshold to display. For example, a value of ms_threshold = 1.0
      will only display morphs with a morphscore higher than 1.0.
    - still_ext: the file extension used by the still images
  '''

  scores = {}
  with open(scores_file) as file:
    scores = json.load(file)


  for morph in os.listdir(morphs_dir):
    
    try:
      score = round(scores[morph + '.csv'], 3)
    except KeyError:
      print("KeyError encountered. Skipping morph...")
    if score < ms_threshold:
      continue

    f = plt.figure(morph)
    ax = np.zeros(3, dtype=object)

    spec = gridspec.GridSpec(ncols=2, nrows=2)

    ax[0] = f.add_subplot(spec[0, 0:])
    ax[1] = f.add_subplot(spec[1, 0])
    ax[2] = f.add_subplot(spec[1, 1])
    still_1 = morph.split('-')[0]
    still_2 = morph.split('-')[1].split('.')[0]
    morph_img = mpimg.imread(morphs_dir + '/' + morph)
    still_1_img = mpimg.imread(stills_dir + '/' + still_1 + still_ext)
    still_2_img = mpimg.imread(stills_dir + '/' + still_2 + still_ext)

    for a in ax:
      a.set_yticklabels([])
      a.set_xticks([])
      a.set_xticklabels([])
      a.set_yticks([])

    ax[0].imshow(morph_img)
    ax[1].imshow(still_1_img)
    ax[2].imshow(still_2_img)

    placeholder = 5.00
    ax[0].title.set_text(morph + ', MorphScore: ' + str(score) + '\n' + 'Average distance to identities (1 / MorphScore): ' + str(round(1/scores[morph + '.csv'], 3)))
    ax[1].set_xlabel(still_1 + still_ext)
    ax[2].set_xlabel(still_2 + still_ext)


    plt.show()
  

def plot_wasserstein(morph_details_file:str):
  details = {}
  with open(morph_details_file) as file:
    details = json.load(file)

  xA = []
  yA = []

  xB = []
  yB = []

  xM = []
  yM = []

  for key in details.keys():
    xA.append(details[key]['distanceA'])
    xB.append(details[key]['distanceB'])
    yA.append(details[key]['1-wasserstein'])
    yB.append(details[key]['1-wasserstein'])

    xM.append((details[key]['distanceA'] + details[key]['distanceB'])/2)
    yM.append(details[key]['1-wasserstein'])

  
  plt.figure(0)
  plt.scatter(xA, yA, s=5)
  plt.xlabel('1-wasserstein distance')
  plt.ylabel('distance A')

  plt.figure(1)
  plt.scatter(xB, yB, s=5)
  plt.xlabel('1-wasserstein distance')
  plt.ylabel('distance B')

  plt.figure(2)
  plt.scatter(xM, yM, s=5)
  plt.xlabel('1-wasserstein distance')
  plt.ylabel('Average of distance A and B')

  plt.figure(3)
  plt.hist(yM, bins=100)
  plt.show()


def write_details_to_csv(morph_details_file:str, csv_out_file:str):
  csv_out = 'File Name, MorphScore, distance A, distance B, 1-wasserstein\n'

  details = {}
  with open(morph_details_file) as f:
    details = json.load(f)
  
  for key in details.keys():
    csv_out += key + ',' + str(details[key]['morphscore']) + ',' + str(details[key]['distanceA']) + ',' + str(details[key]['distanceB']) + ',' + str(details[key]['1-wasserstein']) + '\n'

  with open(csv_out_file, 'w') as f:
    f.write(csv_out)

    





