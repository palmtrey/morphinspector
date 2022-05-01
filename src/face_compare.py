##
# @file face_compare.py
#
# @brief Uses the NearFace library to run facial recognition on a set of images

from turtle import distance
from nearface import NearFace
import os
from tqdm import tqdm


def compare(morphs_dir:str, stills_dir:str, output_csvs_dir:str):
  '''
  Compares each morph image found in morphs_dir to all still images found in stills_dir
  
  '''
  for filename in tqdm(os.listdir(morphs_dir)):
    try:

      df = NearFace.find(
        img_path = morphs_dir + '/' + filename, 
        db_path = stills_dir,
        distance_metric='euclidean_l2',
        enforce_detection= False, 
        use_threshold=False
      )

      if not os.path.isdir(output_csvs_dir):
        os.mkdir(output_csvs_dir)
        
      df.to_csv(output_csvs_dir + '/' + filename + '.csv', sep='\t')
      
    except AttributeError:
      print('AttributeError encountered... skipping morph ' + filename)


if __name__ == '__main__':
  compare(
      morphs_dir='../data/images/frll_morphs',
      stills_dir='../data/images/frll_stills',
      output_csvs_dir='../data/nearface_out/morphs/frll_morphs_l2'
  )
