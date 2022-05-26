import json
import ranking
import roc_curve
import utils
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np


def main():
    ranking.export_ranked_morphs('../data/stats/details_frll_scanned_l2.txt', 0.86, 'ranked_frll_morphs_p&s.json')
    pass

if __name__ == '__main__':
    main()
