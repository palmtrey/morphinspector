import utils
import windows
import PyQt6.QtWidgets as QtWidgets


class MorphInspectorGUI():
  '''
  The main GUI class for the Morph Inspector application
  '''
  def __init__(self, settings: utils.GUISettings):
    self.app = QtWidgets.QApplication([])
    self.report_screen_info()

    self.settings = settings
    self.settings.load_config()

    self.Morphs = utils.encapsulate_morphs(self.settings)

    # Create the main window for the app
    self.mainwindow = windows.MainWindow(self.size, self.settings.precision, self.Morphs, self.settings)

    # Show the window
    self.mainwindow.show()

  def start(self):
    if self.settings.details_cosine_path == '' or self.settings.details_l2_path == '':
      print('use_saved_details=False. Generating details...')

      if self.settings.csvs_cosine_path is None and self.settings.csvs_l2_path is None:
        raise TypeError('use_saved_details=False, but user did not provide csvs paths.')
      else:
        if self.settings.csvs_cosine_path is not None:
          print('Generating cosine details...')
          utils.writescores(self.settings.csvs_cosine_path, 'temp/details_cosine.txt', 'VGG-Face_cosine')
          self.settings.details_cosine_path = 'temp/details_cosine.txt'
        if self.settings.csvs_l2_path is not None:
          print('Generating l2 details...')
          utils.writescores(self.settings.csvs_l2_path, 'temp/details_l2.txt', 'VGG-Face_euclidean_l2')
          self.settings.details_l2_path = 'temp/details_l2.txt'

    self.app.exec()

  def report_screen_info(self):
    # Prints screen information
    self.screen = self.app.primaryScreen()
    self.size = self.screen.size()
    self.rect = self.screen.availableGeometry()

    utils.report('Screen: ' + str(self.screen.name()), utils.ReportType.INFO)
    utils.report('Size: ' + str(self.size.width()) + ' x ' + str(self.size.height()), utils.ReportType.INFO)
    utils.report('Available: ' + str(self.rect.width()) + ' x ' + str(self.rect.height()), utils.ReportType.INFO)
