import gui
import json
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

  with open('../resources/version.json', 'r') as f:
    utils.report('Running Morph Inspector version ' + str(json.load(f)), utils.ReportType.INFO)

  gui = gui.MorphInspectorGUI(settings)
  gui.start()
