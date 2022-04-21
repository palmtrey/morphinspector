from PIL import Image
import PyQt6.QtCore as QtCore
import PyQt6.QtGui as QtGui
import PyQt6.QtWidgets as QtWidgets
import windows

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
  def __init__(self, image:str, parent=None):
    super().__init__()
    self.p = QtGui.QPixmap(image)
    pil_img = Image.open(image)
    self.native_height = pil_img.size[0]
    self.native_width = pil_img.size[1]

  def setPixmap(self, p):
    self.p = QtGui.QPixmap(p)
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

  def __init__(self, image:str, type:str):
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

class WindowWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
  
  def resizeEvent(self, event):
    new_size = QtCore.QSize(2, 1)
    new_size.scale(event.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    self.resize(new_size)
  
