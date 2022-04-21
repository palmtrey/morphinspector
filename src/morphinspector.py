##
# @mainpage Face Morphing Research
#
# @section description_main Description
# A collection of Python programs used in Clarkon University's CAMEL labs
# research in face morphing.
#
#
# Copyright (c) 2022 Cameron M Palmer, campalme@clarkson.edu. All rights reserved.

import gui

if __name__ == '__main__':
  settings = gui.GUISettings('../images/morphs_renamed', '../images/stills_renamed', '.jpg', use_saved_details=True, details_cosine_path='../details_cosine.txt', details_l2_path='../details_l2.txt', precision=4)
  gui = gui.MorphInspectorGUI(settings)
  gui.start()
