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
import utils

if __name__ == '__main__':
  settings = utils.GUISettings(
             morphs_dir='', 
             stills_dir='', 
             still_ext='.jpg', 
             details_cosine_path='../_data/stats/details_cosine.txt', 
             details_l2_path='../_data/stats/details_l2.txt', 
             precision=4
             )

  gui = gui.MorphInspectorGUI(settings)
  gui.start()
