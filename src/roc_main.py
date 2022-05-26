import json
import roc_curve
import sklearn.metrics

def main():
    # All Ranks
    xy = roc_curve.gen_roc_curve(
        '../data/stats/nearface_out/morphs/clarkson_morphs_scanned_l2',
        '../data/stats/nearface_out/stills/clarkson_stills_l2_threshold',
        0.001) 

    with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc.json', 'w') as f:
        json.dump(xy, f)

    # Rank A
    xya = roc_curve.gen_roc_curve(
        '../data/stats/nearface_out/morphs/ranking_subsets/clarkson_scanned_subset_l2/rank_a',
        '../data/stats/nearface_out/stills/clarkson_stills_l2_threshold',
        0.001) 
    
    with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc_ranka.json', 'w') as f:
        json.dump(xya, f)


    # Rank B
    xyb = roc_curve.gen_roc_curve(
        '../data/stats/nearface_out/morphs/ranking_subsets/clarkson_scanned_subset_l2/rank_b',
        '../data/stats/nearface_out/stills/clarkson_stills_l2_threshold',
        0.001) 
    
    with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc_rankb.json', 'w') as f:
        json.dump(xyb, f)

    
    # Rank C
    xyc = roc_curve.gen_roc_curve(
        '../data/stats/nearface_out/morphs/ranking_subsets/clarkson_scanned_subset_l2/rank_c',
        '../data/stats/nearface_out/stills/clarkson_stills_l2_threshold',
        0.001) 
    
    with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc_rankc.json', 'w') as f:
        json.dump(xyc, f)
    
    
    # with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc.json', 'r') as f:
    #     xy = json.load(f)

    # with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc_ranka.json', 'r') as f:
    #     xya = json.load(f)

    # with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc_rankb.json', 'r') as f:
    #     xyb = json.load(f)

    # with open('../data/stats/roc_curves/clarkson_morphs_scanned_rc_rankc.json', 'r') as f:
    #     xyc = json.load(f)



    
    print('All Ranks AUC: ' + str(sklearn.metrics.auc(xy[0], xy[1])))
    print('Rank A AUC: ' + str(sklearn.metrics.auc(xya[0], xya[1])))
    print('Rank B AUC: ' + str(sklearn.metrics.auc(xyb[0], xyb[1])))
    print('Rank C AUC: ' + str(sklearn.metrics.auc(xyc[0], xyc[1])))
   
    roc_curve.plot_multiple_roc_curve(
        xy,
        'Clarkson Print & Scan L2 ROC Curves',
        xy1=xya,
        xy2=xyb,
        xy3=xyc,
        xy0_label='All Ranks',
        xy1_label='Rank A',
        xy2_label='Rank B',
        xy3_label='Rank C')

    # print(sklearn.metrics.auc(xy[0], xy[1]))


    # roc_curve.compare_all_stills(
    #     '../data/images/frll_stills', 
    #     '../data/stats/nearface_out/stills/frll_stills_l2_threshold',
    #     compare_all=True, use_threshold=True)

if __name__ == '__main__':
    main()