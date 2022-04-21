import utils
import windows
import os
import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtGui as QtGui
from tqdm import tqdm


class GUISettings():
  def __init__(self, morphs_dir:str, stills_dir:str, still_ext:str, use_saved_details:bool=False, details_cosine_path:str=None, details_l2_path:str=None, csvs_cosine_path:str=None, csvs_l2_path:str=None, precision:int=3):
    self.morphs_dir = morphs_dir
    self.stills_dir = stills_dir
    self.still_ext = still_ext
    self.use_saved_details = use_saved_details
    self.details_cosine_path = details_cosine_path
    self.details_l2_path = details_l2_path
    self.csvs_cosine_path = csvs_cosine_path
    self.csvs_l2_path = csvs_l2_path
    self.precision = precision

    if self.use_saved_details == True and self.details_cosine_path == None and self.details_l2_path == None:
      raise ValueError('User selected to use saved details but did not provide a path to details')


class MorphInspectorGUI():
  def __init__(self, settings:GUISettings):
    self.settings = settings

    self.Morphs = self.encapsulate_morphs(self.settings)

    self.app = QtWidgets.QApplication([])

    # Printing screen information
    self.screen = self.app.primaryScreen()
    print('Screen: %s' % self.screen.name())
    self.size = self.screen.size()
    print('Size: %d x %d' % (self.size.width(), self.size.height()))
    self.rect = self.screen.availableGeometry()
    print('Available: %d x %d' % (self.rect.width(), self.rect.height()))

    # Create the main window for the app
    self.mswindow = windows.MSWindow(self.size, self.settings.precision, self.Morphs)
  

    # Show the window
    self.mswindow.show()

  def encapsulate_morphs(self, settings:GUISettings) -> list:
    '''
    Takes in the directory where morphs are stored and encapsulates these
    morphs in the Morph type. Returns a list of all Morph objects.
    '''

    Morphs = []

    print('Preparing morphs for display...')
    for morph in tqdm(os.listdir(settings.morphs_dir)):
      try:
        Morphs.append(utils.Morph(
          settings.morphs_dir + '/' + morph, 
          settings.stills_dir, 
          settings.still_ext, 
          csv_cosine_path=settings.csvs_cosine_path, 
          csv_l2_path=settings.csvs_l2_path,
          details_cosine_path=settings.details_cosine_path,
          details_l2_path=settings.details_l2_path
          ))
      except KeyError:
        print('KeyError, morph probably not found in existing file. Skipping...')

    return Morphs


  def start(self):
    if self.settings.use_saved_details == False:
      print('use_saved_details=False. Generating details...')

      if self.settings.csvs_cosine_path == None and self.settings.csvs_l2_path == None:
        raise TypeError('use_saved_details=False, but user did not provide csvs paths.')
      else:
        if self.settings.csvs_cosine_path != None:
          print('Generating cosine details...')
          utils.writescores(self.settings.csvs_cosine_path, 'temp/details_cosine.txt', 'VGG-Face_cosine')
          self.settings.details_cosine_path = 'temp/details_cosine.txt'
        if self.settings.csvs_l2_path != None:
          print('Generating l2 details...')
          utils.writescores(self.settings.csvs_l2_path, 'temp/details_l2.txt', 'VGG-Face_euclidean_l2')
          self.settings.details_l2_path = 'temp/details_l2.txt'

    self.app.exec()

  



  