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
