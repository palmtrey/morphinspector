import utils
import widgets
import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtGui as QtGui

class MSWindow(QtWidgets.QMainWindow):
  def __init__(self, size:QtCore.QSize, precision:int, Morphs:list):
    super().__init__()

    # Logic setup
    self.precision = precision
    self.Morphs = Morphs
    self.morph_index = 0

    # Window GUI setup
    self.size = size
    self.setWindowTitle("Morph Viewer")
    self.setMinimumSize(self.size.width()//3, self.size.height()//3)

    self.morph_image = widgets.MImageContainer('../images/morphs_renamed/00_0-01_0.png', 'Morph')

    self.still1_image = widgets.MImageContainer('../images/stills_renamed/00_0.jpg', 'Still 1')
    self.still1_image.all_stills_pressed.connect(self.all_stills1_pressed)

    self.still2_image = widgets.MImageContainer('../images/stills_renamed/01_0.jpg', 'Still 2')
    self.still2_image.all_stills_pressed.connect(self.all_stills2_pressed)

    self.data_label = widgets.DataLabel()

    self.next_button = QtWidgets.QPushButton()
    self.next_button.setText('Next ->')
    self.next_button.clicked.connect(self.next_button_clicked)

    self.previous_button = QtWidgets.QPushButton()
    self.previous_button.setText('<- Previous')
    self.previous_button.clicked.connect(self.previous_button_clicked)

    self.morph_label = QtWidgets.QLabel()
    self.morph_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)



    self.layout = QtWidgets.QGridLayout()
    self.layout.addWidget(self.morph_image, 0, 0, 2, 1)
    self.layout.addWidget(self.still1_image, 0, 1, 2, 1)
    self.layout.addWidget(self.still2_image, 0, 2, 2, 1)
    self.layout.addWidget(self.data_label, 2, 0, 1,3)
    self.layout.addWidget(self.next_button, 3, 2)
    self.layout.addWidget(self.previous_button, 3, 0)
    self.layout.addWidget(self.morph_label, 3, 1)

    self.widget = widgets.WindowWidget()
    self.widget.setLayout(self.layout)
    self.setCentralWidget(self.widget)

    # Set the first morph
    self.set_morph(self.Morphs[self.morph_index])

    
  def set_morph(self, morph:utils.Morph) -> None:
    self.morph = morph
    self.morph_image.set_image(self.morph.get_morph_path())
    self.still1_image.set_image(self.morph.get_still1_path())
    self.still2_image.set_image(self.morph.get_still2_path())
    self.morph_label.setText(str(self.morph_index + 1) + ' / ' + str(len(self.Morphs)))
    self.set_data()

  def set_data(self) -> None:
    cosine_data = self.morph.get_details('cosine')
    l2_data = self.morph.get_details('l2')
    data_string = ''

    # Formatting cosine data
    data_string += 'Cosine Distance Metric:\n'
    data_string += '  MorphScore: ' + str(round(cosine_data['morphscore'], self.precision)) + '\n'
    data_string += '  1/MorphScore: ' + str(round(1 / cosine_data['morphscore'], self.precision)) + '\n'
    data_string += '  Avg distance to ' + self.morph.get_still1() + ': ' + str(round(cosine_data['distanceA'], self.precision)) + '\n'
    data_string += '  Avg distance to ' + self.morph.get_still2() + ': ' + str(round(cosine_data['distanceB'], self.precision)) + '\n'
    data_string += '  1-Wasserstein (EMD) distance between above: ' + str(round(cosine_data['1-wasserstein'], self.precision)) + '\n'

    data_string += '\n'

    data_string += 'L2 Euclidean Distance Metric:\n'
    data_string += '  MorphScore: ' + str(round(l2_data['morphscore'], self.precision)) + '\n'
    data_string += '  1/MorphScore: ' + str(round(1 / l2_data['morphscore'], self.precision)) + '\n'
    data_string += '  Avg distance to ' + self.morph.get_still1() + ': ' + str(round(l2_data['distanceA'], self.precision)) + '\n'
    data_string += '  Avg distance to ' + self.morph.get_still2() + ': ' + str(round(l2_data['distanceB'], self.precision)) + '\n'
    data_string += '  1-Wasserstein (earth mover) distance between above: ' + str(round(l2_data['1-wasserstein'], self.precision)) + '\n'


    self.data_label.setText(data_string)

  def get_morph(self) -> str:
    return self.morph


  def next_button_clicked(self) -> None:
    if self.morph_index < len(self.Morphs) - 1:
      self.morph_index += 1
    else:
      self.morph_index = 0
    self.set_morph(self.Morphs[self.morph_index])
    

  def previous_button_clicked(self) -> None:
    if self.morph_index != 0:
      self.morph_index -= 1
    else:
      self.morph_index = len(self.Morphs) - 1
    self.set_morph(self.Morphs[self.morph_index])

  def all_stills1_pressed(self) -> None:
    print('All stills 1 pressed!')
    self.still_window = AllStillsWindow(self.size, self.morph, 1)
    self.still_window.show()

  def all_stills2_pressed(self) -> None:
    print('All stills 2 pressed!')
    self.still_window = AllStillsWindow(self.size, self.morph, 2)
    self.still_window.show()

class AllStillsWindow(QtWidgets.QMainWindow):
  def __init__(self, size:QtCore.QSize, morph:utils.Morph, still_num:int):
    super().__init__()
    self.size = size
    self.morph = morph
    self.stills_dir = morph.get_stills_dir()
    if still_num == 1:
      self.still = morph.get_still1()
      self.still_path = morph.get_still1_path()
      self.id = morph.get_still1_id()
      self.stills = morph.get_all_still1()
    elif still_num == 2:
      self.still = morph.get_still2()
      self.still_path = morph.get_still2_path()
      self.id = morph.get_still2_id
      self.stills = morph.get_all_still2()
    else:
      raise ValueError('still_num in AllStillsWindow initializer must be either 1 or 2.')

    print('All stills: ' + str(self.stills))
    print('Stills dir: ' + morph.get_stills_dir())

    self.size = size
    self.setWindowTitle('All stills for ' + str(self.still))
    self.setMinimumSize(self.size.width()//4, self.size.height()//4)

    

    # self.layout = QtWidgets.QGridLayout()

    # row = 0
    # column = 0
    # images = []
    # iterator = 0
    # for still in self.stills:
    #   print(self.stills_dir + '/' + still)
    #   # images.append(widgets.MImageContainer(self.stills_dir + '/' + still, ''))
    #   images.append(widgets.MImage(self.stills_dir + '/' + still))
    #   self.layout.addWidget(images[iterator], row, column)
    #   if column == 0:
    #     column = 1
    #   elif column == 1:
    #     column = 0
    #     row += 1
    #   iterator += 1
      
    self.layout = QtWidgets.QVBoxLayout()
    for still in self.stills:
      self.layout.addWidget(widgets.MImageContainer(self.stills_dir + '/' + still, ''))

    self.widget = QtWidgets.QWidget()
    self.widget.setLayout(self.layout)

    self.scroll = QtWidgets.QScrollArea()
    self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scroll.setWidgetResizable(True)
    self.scroll.setWidget(self.widget)

    self.setCentralWidget(self.scroll)
