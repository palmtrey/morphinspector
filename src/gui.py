import utils
import windows
import os
import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtGui as QtGui
from tqdm import tqdm


class MorphInspectorGUI():
  '''
  The main GUI class for the Morph Inspector application
  '''
  def __init__(self, settings:utils.GUISettings):
    self.settings = settings

    

    self.app = QtWidgets.QApplication([])

    # Printing screen information
    self.screen = self.app.primaryScreen()
    print('Screen: %s' % self.screen.name())
    self.size = self.screen.size()
    print('Size: %d x %d' % (self.size.width(), self.size.height()))
    self.rect = self.screen.availableGeometry()
    print('Available: %d x %d' % (self.rect.width(), self.rect.height()))

    self.Morphs = self.encapsulate_morphs(self.settings)

    # Create the main window for the app
    self.mainwindow = windows.MainWindow(self.size, self.settings.precision, self.Morphs, self.settings)

    # Show the window
    self.mainwindow.show()

  def encapsulate_morphs(self, settings:utils.GUISettings) -> list:
    '''
    Takes in the directory where morphs are stored and encapsulates these
    morphs in the Morph type. Returns a list of all Morph objects.
    '''

    if settings.morphs_dir == '' or settings.stills_dir == '':
      return None


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

  



  