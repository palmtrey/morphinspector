import enum
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas
from scipy.stats import wasserstein_distance
from tqdm import tqdm
from enum import Enum
import yaml
import pickle
import statistics


class GUISettings():
  '''
  Create an object of type GUISettings to define settings
  for the main application.
  '''
  def __init__(
      self, 
      morphs_dir:str = '', 
      stills_dir:str = '', 
      still_ext:str = '.jpg', 
      details_cosine_path:str='', 
      details_l2_path:str='', 

      csvs_cosine_path:str='', 
      csvs_l2_path:str='', 

      precision:int=3
      ):
    
    
    self.morphs_dir = morphs_dir
    self.stills_dir = stills_dir
    self.still_ext = still_ext
    self.details_cosine_path = details_cosine_path
    self.details_l2_path = details_l2_path
    self.csvs_cosine_path = csvs_cosine_path
    self.csvs_l2_path = csvs_l2_path
    self.precision = precision

  def __str__(self) -> str:
    result = ''
    result += 'morphs_dir: ' + self.morphs_dir + '\n'
    result += 'stills_dir: ' + self.stills_dir + '\n'
    result += 'still_ext: ' + self.still_ext + '\n'
    result += 'details_cosine_path: ' + self.details_cosine_path + '\n'
    result += 'details_l2_path: ' + self.details_l2_path + '\n'
    result += 'csvs_cosine_path: ' + self.csvs_cosine_path + '\n'
    result += 'csvs_l2_path: ' + self.csvs_l2_path + '\n'
    result += 'precision: ' + str(self.precision)

    return result

  def save_config(self) -> None:
    outputdict = {}
    outputdict['morphs_dir'] = self.morphs_dir
    outputdict['stills_dir'] = self.stills_dir
    outputdict['still_ext'] = self.still_ext
    outputdict['details_cosine_path'] = self.details_cosine_path
    outputdict['details_l2_path'] = self.details_l2_path
    outputdict['csvs_cosine_path'] = self.csvs_cosine_path
    outputdict['csvs_l2_path'] = self.csvs_l2_path
    outputdict['precision'] = self.precision

    with open('../resources/config.yml', 'w') as f:
      yaml.dump(outputdict, f)

  def load_config(self) -> None:
    if os.path.exists('../resources/config.yml'):
      with open('../resources/config.yml', 'r') as f:
        inputdict = yaml.load(f, yaml.Loader)

        self.morphs_dir = inputdict['morphs_dir']
        self.stills_dir = inputdict['stills_dir']
        self.still_ext = inputdict['still_ext']
        self.details_cosine_path = inputdict['details_cosine_path']
        self.details_l2_path = inputdict['details_l2_path']
        self.csvs_cosine_path = inputdict['csvs_cosine_path']
        self.csvs_l2_path = inputdict['csvs_l2_path']
        self.precision = inputdict['precision']
    else:
      report('Config file does not exist. Will retrieve settings from', ReportType.INFO)


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

    if csv_cosine_path != '':
      self.details_cosine = calc_morphdetails(self.csv_cosine_path, 'VGG-Face_cosine', self.morph_ext)
    elif details_cosine_path != '':
      with open(details_cosine_path) as file:
        self.details_cosine = json.load(file)[self.get_morph() + '.csv']
    else:
      self.details_cosine = ''

    if csv_l2_path != '':
      self.details_l2 = calc_morphdetails(self.csv_l2_path, 'VGG-Face_euclidean_l2', self.morph_ext)
    elif details_l2_path != '':
      with open(details_l2_path) as file:
        self.details_l2 = json.load(file)[self.get_morph() + '.csv']
    else:
      self.details_l2 = ''

  def get_details(self, type:str) -> dict:
    result = {}
    result['avgdist'] = self.get_avgdist(type)
    result['distanceA'] = self.get_distanceA(type)
    result['distanceB'] = self.get_distanceB(type)
    result['1-wasserstein'] = self.get_emd(type)
    return result

  def get_avgdist(self, type:str) -> float:
    if type == 'cosine':
      if self.details_cosine == None:
        raise TypeError('morph does not contain a cosine morphscore')
      else:
        return self.details_cosine['avgdist']

    elif type == 'l2':
      if self.details_l2 == None:
        raise TypeError('morph does not contain an l2 morphscore')
      else:
        return self.details_l2['avgdist']
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


class ReportType(Enum):
  INFO = 1
  WARNING = 2
  ERROR = 3


class Rank(enum.Enum):
  A = 1  # Rank A indicates that the morph can be identified as both of its composite identities

  B = 2  # Rank B indiciates that the morph can only be identified as one of its composite identities.

  C = 3  # Rank C indiciates that the morph cannot be identified as either one of its composite identities.


def encapsulate_morphs(settings:GUISettings) -> list:
    '''
    Takes in the directory where morphs are stored and encapsulates these
    morphs in the Morph type. Returns a list of all Morph objects.

    If encapsulate_morphs finds a pickled version of morphs under
    ../resources/cache matching the same path, it will load those
    instead of re-encapsulating existing morphs to improve startup time.
    If it does not find this pickled version, it will instead encapsulate
    the morphs and store a pickled encapsulation under ../resources/cache
    in the format 'morphs_dir.morphcache'.
    '''

    # If the settings object does not contain morphs or stills directories,
    # return None
    if settings.morphs_dir == '' or settings.stills_dir == '':
      return None

    morph_cache_file = settings.morphs_dir.replace('/', '_') + '.morphcache'

    # If a pickled cache exists, load the cache and use it.
    if os.path.exists('../resources/cache/' + morph_cache_file):
      with open('../resources/cache/' + morph_cache_file, 'rb') as f:
        return pickle.load(f)


    


    # If a pickled cache does not exist, encapsulate the morphs
    # (approx. 18 ms per morph)
    Morphs = []

    print('Preparing morphs for display...')
    for morph in tqdm(os.listdir(settings.morphs_dir)):
      try:
        Morphs.append(Morph(
          settings.morphs_dir + '/' + morph, 
          settings.stills_dir, 
          settings.still_ext, 
          csv_cosine_path=settings.csvs_cosine_path, 
          csv_l2_path=settings.csvs_l2_path,
          details_cosine_path=settings.details_cosine_path,
          details_l2_path=settings.details_l2_path
          ))
      except KeyError:
        pass
        #print('KeyError, morph probably not found in existing file. Skipping...')

    # Store the encapsulated morphs as a cache
    with open('../resources/cache/' + morph_cache_file, 'wb') as f:
      pickle.dump(Morphs, f)

    return Morphs


def get_stills_from_morph(morph:str) -> list:
  return [morph.split('/')[-1].split('-')[0].split('.')[0], morph.split('/')[-1].split('-')[1].split('.')[0]]


def calc_avgdist(morph_csv:str, distance_label:str, morph_ext:str = '.png') -> float:
  '''
  Calculates an average distance for a given morph's csv file.

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

  Returns:
    - The average distance from the given morph to both its stills.
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

  avgdist = statistics.mean([statistics.mean(identity_1_distances), statistics.mean(identity_2_distances)])

  return avgdist


def calc_morphdetails(morph_csv: str, distance_label: str, morph_ext: str = '.png') -> dict:
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
  result['avgdist'] = calc_avgdist(morph_csv, distance_label, morph_ext)
  result['distanceA'] = np.mean(identity_1_distances)
  result['distanceB'] = np.mean(identity_2_distances)
  result['1-wasserstein'] = wasserstein_distance(identity_1_distances, identity_2_distances)

  return result


def writescores(morph_csvs_dir:str, output_file:str, distance_label:str) -> None:
  '''
  Writes morph details for all morphs csvs stored in morph_csvs_dir to an output file, output_file (a txt file)

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

  details = {}
  for csv in tqdm(os.listdir(morph_csvs_dir)):
    try:
      details[csv] = calc_morphdetails(morph_csvs_dir + '/' + csv, distance_label)
    except statistics.StatisticsError:
      print('StatisticsError. Skipping morph.')

  with open(output_file, 'w') as file:
    file.write(json.dumps(details))


def plot_wasserstein(morph_details_file:str) -> None:
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


def write_details_to_csv(morph_details_file:str, csv_out_file:str) -> None:
  csv_out = 'File Name, average distance, distance A, distance B, 1-wasserstein\n'

  details = {}
  with open(morph_details_file) as f:
    details = json.load(f)
  
  for key in details.keys():
    csv_out += key + ',' + str(details[key]['avgdist']) + ',' + str(details[key]['distanceA']) + ',' + str(details[key]['distanceB']) + ',' + str(details[key]['1-wasserstein']) + '\n'

  with open(csv_out_file, 'w') as f:
    f.write(csv_out)


def report(message, type:ReportType) -> None:
  prefix = ''
  message = str(message).split('\n')
  if type == ReportType.INFO:
    prefix = '[INFO] '
  elif type == ReportType.WARNING:
    prefix = '[WARNING] '
  else: # type == ReportType.ERROR
    prefix = '[ERROR] '

  for line in message:
    print(prefix + line)




