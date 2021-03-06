import utils
from PIL import Image
import PyQt6.QtCore as QtCore
import PyQt6.QtGui as QtGui
import PyQt6.QtWidgets as QtWidgets
from pathlib import Path


class DataLabel(QtWidgets.QLabel):
  def __init__(self):
    super().__init__()
    self.text = "Data: \n Some data here."
    self.setText(self.text)
    self.setStyleSheet("font:Roboto; border:1px solid rgb(0, 0, 0); ")
    self.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
  
  def getText(self):
    return self.text


class MImage(QtWidgets.QWidget):
  def __init__(self, image: str, parent=None):
    super().__init__()
    self.p = QtGui.QPixmap(image)
    self.native_height = 1  # default values for aspect ratio 1:1 (square image)
    self.native_width = 1
    self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

  def setPixmap(self, p):
    self.p = QtGui.QPixmap(p)
    pil_img = Image.open(p)
    self.native_height = pil_img.size[0]
    self.native_width = pil_img.size[1]
    self.update()

  def paintEvent(self, event):
    if not self.p.isNull():
      painter = QtGui.QPainter(self)
      painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
      painter.drawPixmap(self.rect(), self.p)

  def resizeEvent(self, event):
    new_size = QtCore.QSize(self.native_height, self.native_width)
    new_size.scale(event.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    self.resize(new_size)


class MImageContainer(QtWidgets.QWidget):
  # Signals
  all_stills_pressed = QtCore.pyqtSignal()

  def __init__(self, image: str, type: str):
    super().__init__()
    self.mimage = MImage(image)
    self.bottom_label_text = image.split('/')[-1]
    self.top_label_text = type
    self.bottom_label = QtWidgets.QLabel(self.bottom_label_text)
    self.bottom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
    self.top_label = QtWidgets.QLabel(type)

    self.layout = QtWidgets.QGridLayout()
    self.layout.addWidget(self.top_label, 0, 0, 1, 1)
    self.layout.addWidget(self.mimage, 1, 0, 10, 2)
    self.layout.addWidget(self.bottom_label, 11, 0, 1, 1)

    if (self.top_label_text.lower().find('still') != -1):
      self.all_button = QtWidgets.QPushButton()
      self.all_button.setText('Show all')
      self.layout.addWidget(self.all_button, 12, 0, 1, 1)
      self.all_button.clicked.connect(self.all_button_pressed)

    self.setLayout(self.layout)
    
  def set_image(self, image:str) -> None:
    self.mimage.setPixmap(image)
    self.bottom_label_text = image.split('/')[-1]
    self.bottom_label.setText(self.bottom_label_text)

  def all_button_pressed(self) -> None:
    self.all_stills_pressed.emit()


class MImage2(QtWidgets.QLabel):
  def __init__(self, image: str, parent=None):
    super().__init__()
    self.p = QtGui.QPixmap(image)
    pil_img = Image.open(image)
    self.native_height = pil_img.size[0]
    self.native_width = pil_img.size[1]
    self.setPixmap(self.p)
    self.fixed_height = 250

  def resizeEvent(self, event):
    self.p = self.p.scaled(event.size().width(), self.fixed_height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    self.setPixmap(self.p)

class MImageContainer2(QtWidgets.QWidget):

  def __init__(self, image: str):
    super().__init__()
    self.mimage = MImage2(image)
    self.bottom_label_text = image.split('/')[-1]
    self.bottom_label = QtWidgets.QLabel(self.bottom_label_text)
    self.bottom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    self.layout = QtWidgets.QGridLayout()
    self.layout.addWidget(self.mimage, 0, 0, 10, 2)
    self.layout.addWidget(self.bottom_label, 11, 0, 1, 1)

    self.setLayout(self.layout)


class WindowWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
  
  def resizeEvent(self, event):
    new_size = QtCore.QSize(2, 1)
    new_size.scale(event.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    self.resize(new_size)


class DetailLine(QtWidgets.QWidget):
  def __init__(self, labeltext:str):
    super().__init__()

    self.label = QtWidgets.QLabel(self)
    self.label.setText(labeltext)
    self.line = QtWidgets.QLineEdit(self)
    
    self.layout = QtWidgets.QHBoxLayout()
    self.layout.addWidget(self.label)
    self.layout.addWidget(self.line)

    self.setLayout(self.layout)


class DetailsDialog(QtWidgets.QDialog):
  def __init__(self, size:QtCore.QSize, settings:utils.GUISettings):
    super().__init__()

    self.settings = settings
    self.setMinimumSize(size.width()//4, size.height()//4)
    self.setWindowTitle('Morph Inspector Settings')

    self.morphs_dir_label = QtWidgets.QLabel(self)
    self.morphs_dir_label.setText('Morphs directory: ')
    self.morphs_dir_line = QtWidgets.QLineEdit(self)
    self.morphs_dir_line.setText(self.settings.morphs_dir)
    self.morphs_dir_bt = QtWidgets.QPushButton(self)
    self.morphs_dir_bt.setText('Search')
    self.morphs_dir_bt.clicked.connect(lambda: self.get_dir('morphs_dir'))

    self.stills_dir_label = QtWidgets.QLabel(self)
    self.stills_dir_label.setText('Stills directory: ')
    self.stills_dir_line = QtWidgets.QLineEdit(self)
    self.stills_dir_line.setText(self.settings.stills_dir)
    self.stills_dir_bt = QtWidgets.QPushButton(self)
    self.stills_dir_bt.setText('Search')
    self.stills_dir_bt.clicked.connect(lambda: self.get_dir('stills_dir'))

    self.details_cosine_label = QtWidgets.QLabel(self)
    self.details_cosine_label.setText('VGG-Face Cosine details file: ')
    self.details_cosine_line = QtWidgets.QLineEdit(self)
    self.details_cosine_line.setText(self.settings.details_cosine_path)
    self.details_cosine_bt = QtWidgets.QPushButton(self)
    self.details_cosine_bt.setText('Search')
    self.details_cosine_bt.clicked.connect(lambda: self.get_file('details_cosine'))

    self.details_l2_label = QtWidgets.QLabel(self)
    self.details_l2_label.setText('VGG-Face L2 details file: ')
    self.details_l2_line = QtWidgets.QLineEdit(self)
    self.details_l2_line.setText(self.settings.details_l2_path)
    self.details_l2_bt = QtWidgets.QPushButton(self)
    self.details_l2_bt.setText('Search')
    self.details_l2_bt.clicked.connect(lambda: self.get_file('details_l2'))

    self.csvs_cosine_label = QtWidgets.QLabel(self)
    self.csvs_cosine_label.setText('VGG-Face Cosine CSVs directory: ')
    self.csvs_cosine_line = QtWidgets.QLineEdit(self)
    self.csvs_cosine_line.setText(self.settings.csvs_cosine_path)
    self.csvs_cosine_bt = QtWidgets.QPushButton(self)
    self.csvs_cosine_bt.setText('Search')
    self.csvs_cosine_bt.clicked.connect(lambda: self.get_dir('csvs_cosine'))

    self.csvs_l2_label = QtWidgets.QLabel(self)
    self.csvs_l2_label.setText('VGG-Face L2 CSVs directory: ')
    self.csvs_l2_line = QtWidgets.QLineEdit(self)
    self.csvs_l2_line.setText(self.settings.csvs_l2_path)
    self.csvs_l2_bt = QtWidgets.QPushButton(self)
    self.csvs_l2_bt.setText('Search')
    self.csvs_l2_bt.clicked.connect(lambda: self.get_dir('csvs_l2'))

    self.precision_label = QtWidgets.QLabel(self)
    self.precision_label.setText('Precision (integer): ')
    self.precision_line = QtWidgets.QLineEdit(self)
    self.precision_line.setText(str(self.settings.precision))

    self.confirm_button = QtWidgets.QPushButton()
    self.confirm_button.setText('Confirm')
    self.confirm_button.clicked.connect(self.confirm_clicked)

    self.layout = QtWidgets.QGridLayout()
    self.layout.addWidget(self.morphs_dir_label, 0, 0)
    self.layout.addWidget(self.morphs_dir_line, 0, 1, 1, 2)
    self.layout.addWidget(self.morphs_dir_bt, 0, 3)

    self.layout.addWidget(self.stills_dir_label, 1, 0)
    self.layout.addWidget(self.stills_dir_line, 1, 1, 1, 2)
    self.layout.addWidget(self.stills_dir_bt, 1, 3)

    self.layout.addWidget(self.details_cosine_label, 2, 0)
    self.layout.addWidget(self.details_cosine_line, 2, 1, 1, 2)
    self.layout.addWidget(self.details_cosine_bt, 2, 3)

    self.layout.addWidget(self.details_l2_label, 3, 0)
    self.layout.addWidget(self.details_l2_line, 3, 1, 1, 2)
    self.layout.addWidget(self.details_l2_bt, 3, 3)

    self.layout.addWidget(self.csvs_cosine_label, 4, 0)
    self.layout.addWidget(self.csvs_cosine_line, 4, 1, 1, 2)
    self.layout.addWidget(self.csvs_cosine_bt, 4, 3)

    self.layout.addWidget(self.csvs_l2_label, 5, 0)
    self.layout.addWidget(self.csvs_l2_line, 5, 1, 1, 2)
    self.layout.addWidget(self.csvs_l2_bt, 5, 3)

    self.layout.addWidget(self.precision_label, 6, 0)
    self.layout.addWidget(self.precision_line, 6, 1, 1, 2)

    self.layout.addWidget(self.confirm_button, 7, 2)

    self.setLayout(self.layout)

  def confirm_clicked(self):
    self.settings.morphs_dir = self.morphs_dir_line.text()
    self.settings.stills_dir = self.stills_dir_line.text()
    self.settings.details_cosine_path = self.details_cosine_line.text()
    self.settings.details_l2_path = self.details_l2_line.text()
    self.settings.csvs_cosine_path = self.csvs_cosine_line.text()
    self.settings.csvs_l2_path = self.csvs_l2_line.text()
    
    # TO DO: Input validation on self.precision_line
    self.settings.precision = int(self.precision_line.text())
    self.close()

  def get_dir(self, data:str):
    path = str(QtWidgets.QFileDialog.getExistingDirectory(self, str(Path.home())))

    if data == 'morphs_dir':
      self.settings.morphs_dir = path
    elif data == 'stills_dir':
      self.settings.stills_dir = path
    elif data == 'csvs_cosine':
      self.settings.csvs_cosine_path = path
    elif data == 'csvs_l2':
      self.settings.csvs_l2_path = path
    else:
      pass
      
    self.update_lines()

  def get_file(self, data:str):
    path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', str(Path.home()))[0])
    if data == 'details_cosine':
      self.settings.details_cosine_path = path
    elif data == 'details_l2':
      self.settings.details_l2_path = path
    else:
      pass
    
    self.update_lines()

  def update_lines(self):
    self.morphs_dir_line.setText(self.settings.morphs_dir)
    self.stills_dir_line.setText(self.settings.stills_dir)
    self.details_cosine_line.setText(self.settings.details_cosine_path)
    self.details_l2_line.setText(self.settings.details_l2_path)
    self.csvs_cosine_line.setText(self.settings.csvs_cosine_path)
    self.csvs_l2_line.setText(self.settings.csvs_l2_path)

  def execr(self) -> utils.GUISettings:
    self.exec()
    return self.settings