from analyse import analyse, set_just_annotate, set_force_new_video, set_just_align


def run_both():
    """ Runs both, the first and the second run."""
    run(is_first_run=True)
    run(is_first_run=False)


def run_just_annotate():
    """ Runs only annotation from the pickled file."""
    set_just_annotate(True)
    set_force_new_video(True)
    run()
    set_just_annotate(False)
    set_force_new_video(False)


def align_first():
    """ Runs alignment only. """
    set_just_align(True)
    run()
    set_just_align(False)


def run(is_first_run=None):
    """ Runs the analysis of all the files.
    
    :arg is_first_run: (bool): iff True, all guided mechanics are hidden, csv is stored in this folder
    """
    a = is_first_run
    ############################################# SINGLE BEE #######################################################
    ## 190822
    # 1stRun 1 -> 1 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_111607344_1BEE_generated_20210430_080914_nn.csv', 1, is_first_run=a)

    # 1stRun 156 -> 61 -> 15 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_141925574_1bee_generated_20210504_081658_nn.csv', 1, is_first_run=a)

    ## 190823
    # 1stRun 6 -> 3 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_153007029_1BEE_generated_20210507_091854_nn.csv', 1, is_first_run=a)

    # 1stRun 15 -> 9 -> 6 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_114450691_1BEE_generated_20210506_100518_nn.csv', 1, is_first_run=a)

    ## 190903
    # 1stRun 19 -> 4 -> 3 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_134034775_1BEE_generated_20210511_083234_nn.csv', 1, is_first_run=a)

    # 1stRun 62 -> 26 -> 3 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_172942424_1BEE_generated_20210520_073610_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190904
    # 1stRun 4 -> 3 -> 3 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_124852149_1BEE_generated_20210520_095527_nn.csv', 1, is_first_run=a)

    # 1stRun 1 -> 1 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_165817979_1BEE_generated_20210525_103941_nn.csv', 1, is_first_run=a)

    ## 190905
    # 1stRun 112 -> 47 -> 17 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_113138227_1BEE_generated_20210528_064758_nn.csv', 1, is_first_run=a)

    ## 190906
    # 1stRun 2 -> 2 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_152940727_1BEE_generated_20210607_101247_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190916
    # 1stRun 391 -> 273 -> 22 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_122643082_1BEE_generated_20210608_090120_nn.csv', 1, is_first_run=a)

    # 1stRun 123 -> 24 -> 13 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_160703748_1BEE_generated_20210611_111022_nn.csv', 1, is_first_run=a)

    # 1stRun 748 -> 445 -> 29 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_163119085_1BEE_generated_20210618_080129_nn.csv', 1, is_first_run=a)

    ## 190917
    # 1stRun 8 -> 8 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_115622949_1BEE_generated_20210902_081924_nn.csv', 1, is_first_run=a)

    # 1stRun 16 -> 6 -> 5 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_105812177_1BEE_generated_20210803_083548_nn.csv', 1, is_first_run=a)

    # 1stRun 12 -> 7 -> 4 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_152245969_1BEE_generated_20210903_103442_nn.csv', 1, is_first_run=a)

    # 1stRun 917 -> 699 -> 12 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_153417672_1BEE_generated_20210906_080339_nn.csv', 1, is_first_run=a)

    ## 190918
    # 1stRun 418 -> 321 -> 12 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_152011250_1BEE_generated_20210907_090200_nn.csv', 1, is_first_run=a)

    # 1stRun 48 -> 19 -> 8 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_145147096_1BEE_generated_20210906_104220_nn.csv', 1, is_first_run=a)

    # 1stRun 79 -> 53 -> 5 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_111016982_1BEE_generated_20210910_081829_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190919
    # 1stRun 7 -> 6 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_143424171_1BEE_generated_20210908_103953_nn.csv', 1, is_first_run=a)

    # 1stRun 103 -> 49 -> 24 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_110353881_1BEE_generated_20210908_084510_nn.csv', 1, is_first_run=a)

    # 1stRun 39 -> 3 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_153051804_1BEE_generated_20210909_090515_nn.csv', 1, is_first_run=a)

    ## 190920
    # 1stRun 6 -> 5 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_111833317_1BEE_generated_20210910_074102_nn.csv', 1, is_first_run=a)

    # 1stRun 999 -> 743 -> 38 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_145859333_1BEE_generated_20210910_083808_nn.csv', 1, is_first_run=a)

    # 1stRun 9 -> 7 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_154830359_1BEE_generated_20210910_090500_nn.csv', 1, is_first_run=a)

    ## 190922
    # 1stRun 11 -> 1 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_120740072_1BEE_generated_20210913_082513_nn.csv', 1, is_first_run=a)

    # 1stRun 4 -> 3 -> 3 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_171602695_1BEE_generated_20210913_105305_nn.csv', 1, is_first_run=a)

    # 1stRun 25 -> 9 -> 5 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_155939352_1BEE_generated_20210913_100501_nn.csv', 1, is_first_run=a)

    ## 190924
    # 1stRun 44 -> 32 -> 10 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_153426086_1BEE_generated_20210914_093742_nn.csv', 1, is_first_run=a)

    # 1stRun 617 -> 414 -> 43 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_111059331_1BEE_generated_20210916_090912_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190925
    # 1stRun 922 -> 683 -> 54 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_101651861_1BEE_generated_20210921_073505_nn.csv', 1, is_first_run=a)

    # 1stRun 16 -> 5 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_132615155_1BEE_generated_20210917_104344_nn.csv', 1, is_first_run=a)

    ## 190926
    # 1stRun 499 -> 344 -> 22 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_153031662_1BEE_generated_20210927_090504_nn.csv', 1, is_first_run=a)

    # 1stRun 24 -> 9 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_122135161_1BEE_generated_20210924_100636_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190927
    # 1stRun 5 -> 2 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_110140688_1BEE_generated_20210929_105511_nn.csv', 1, is_first_run=a)

    # 1stRun 88 -> 25 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_142316901_1BEE_generated_20211006_092457_nn.csv', 1, is_first_run=a)

    # 1stRun 538 -> 349 -> 25 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_111245617_1BEE_generated_20210929_105817_nn.csv', 1, is_first_run=a)

    ## 190928
    # 1stRun 3 -> 3 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_163456673_1BEE_generated_20211011_071038_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190929
    # 1stRun 88 -> 55 -> 19 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_124230212_1BEE_generated_20211012_095333_nn.csv', 1, is_first_run=a)

    # 1stRun 63 -> 15 -> 7 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_160530530_1BEE_generated_20211018_081442_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 190930
    # 1stRun 523 -> 331 -> 42 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_145350661_1BEE_generated_20211018_102533_nn.csv', 1, is_first_run=a)

    # 1stRun 33 -> 18 -> 8 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_112905317_1BEE_generated_20211019_103540_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    # 1stRun 378 -> 227 -> 28 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_115128061_1BEE_generated_20211020_072929_nn.csv', 1, is_first_run=a)

    ## 191001
    # 1stRun 31 -> 11 -> 3 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_114401465_1BEE_generated_20211026_100501_nn.csv', 1, is_first_run=a)

    # 1stRun 3 -> 1 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_143255621_1BEE_generated_20211029_082206_nn.csv', 1, is_first_run=a)

    ## 191002
    # 1stRun 281 -> 189 -> 67 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_104343446_1BEE_generated_20211220_113343_nn.csv', 1, is_first_run=a)

    # 1stRun 121 -> 58 -> 17 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_135837756_1BEE_generated_20211222_092214_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    ## 191003
    # 1stRun 5 -> 3 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_131823429_1BEE_generated_20220103_114647_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    # 1stRun 405 -> 295 -> 96 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_101739372_1BEE_generated_20211222_111933_nn.csv', 1, is_first_run=a)

    ## 191007
    # 1stRun 9 -> 7 -> 6 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_151826322_1BEE_generated_20220105_091320_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    # 1stRun 8 -> 1 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_143443948_1BEE_generated_20220104_115223_nn.csv', 1, is_first_run=a)

    ## 191008
    # 1stRun 37 -> 29 -> 9 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_162311875_1BEE_generated_20220107_085313_nn.csv', 1, is_first_run=a)

    # 1stRun 2 -> 2 -> 1 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_111526719_1BEE_generated_20220105_110112_nn.csv', 1, is_first_run=a)

    # 1stRun 109 -> 24 -> 21 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_151959136_1BEE_generated_20220107_074215_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    # 1stRun 349 -> 155 -> 26 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_124602433_1BEE_generated_20220107_072300_nn.csv', 1, is_first_run=a)

    ## 191011
    # 1stRun 41 -> 9 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_151039091_1BEE_generated_20220107_103850_nn.csv', 1, is_first_run=a)

    # 1stRun 60 -> 24 -> 8 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_140303626_1BEE_generated_20220107_094318_nn.csv', 1, is_first_run=a)

    ## 191014
    # 1stRun 378 -> 279 -> 191 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_160829309_1BEE_generated_20220110_083510_nn.csv', 1, has_tracked_video=True, is_first_run=a)

    # 1stRun 7 -> 3 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_171503396_1BEE_generated_20220111_102855_nn.csv', 1, is_first_run=a)

    ## 191016
    # 1stRun 216 -> 150 -> 25 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_130021334_1BEE_generated_20220118_094841_nn.csv', 1, is_first_run=a)

    # 1stRun 7 -> 2 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_120823730_1BEE_generated_20220111_120510_nn.csv', 1, is_first_run=a)

    ## 191017
    # 1stRun 14 -> 7 -> 4 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_123055432_1BEE_generated_20220121_112104_nn.csv', 1, is_first_run=a)

    # 1stRun 98 -> 22 -> 6 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_163619189_1BEE_generated_20220125_073904_nn.csv', 1, is_first_run=a)

    # 1stRun 80 -> 33 -> 7 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_131704603_1BEE_generated_20220121_114648_nn.csv', 1, is_first_run=a)

    ## 191018
    # 1stRun 45 -> 23 -> 4 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_123336571_1BEE_generated_20220126_083927_nn.csv', 1, is_first_run=a)

    ############################################# 2 BEES #######################################################
    ## 190822
    # 1stRun 65 -> 49 -> 33 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    # 1stRun 79 -> 62 -> 43 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_143216366_2bees_generated_20210504_064410_nn.csv', 2, is_first_run=a)

    ## 190823
    # 1stRun 171 -> 55 -> 24 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_115857275_2BEES_generated_20210507_083510_nn.csv', 2, is_first_run=a)

    # 1stRun 55 -> 40 -> 23 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_154249666_2BEES_generated_20210510_095112_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    ## 190903
    # 1stRun 187 -> 135 -> 111 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_162330843_2BEES_generated_20210520_072141_nn.csv', 2, is_first_run=a)

    # 1stRun 1034 -> 649 -> 13 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_122246620_2BEES_generated_20210511_083802_nn.csv', 2, is_first_run=a)

    ## 190904
    # 1stRun 1016 -> 742 -> 682 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_113737340_2BEES_generated_20210521_065405_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    # 1stRun 475 -> 360 -> 25 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_155648360_2BEES_generated_20210521_104649_nn.csv', 2, is_first_run=a)

    ## 190905
    # 1stRun 257 -> 150 -> 73 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_120614441_2BEES_generated_20210528_103143_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    # 1stRun 11 -> 5 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_115416146_2BEES_generated_20210528_065454_nn.csv', 2, is_first_run=a)

    ## 190906
    # 1stRun 27 -> 19 -> 8 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_155121999_2BEES_generated_20210607_101833_nn.csv', 2, is_first_run=a)

    ## 190916
    # 1stRun 653 -> 471 -> 166 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_161941067_2BEES_generated_20210618_075432_nn.csv', 2, is_first_run=a)

    # 1stRun 28 -> 23 -> 9 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_164302025_2BEES_generated_20210618_095944_nn.csv', 2, is_first_run=a)

    # 1stRun 488 -> 402 -> 170 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_123747096_2BEES_generated_20210608_091639_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    ## 190917
    # 1stRun 54 -> 33 -> 11 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_110943703_2BEES_generated_20210809_091448_nn.csv', 2, is_first_run=a)

    ## 190918
    # 1stRun 60 -> 54 -> 35 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_112137922_2BEES_generated_20210907_082919_nn.csv', 2, is_first_run=a)

    ## 190919
    # 1stRun 747 -> 609 -> 40 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_151934478_2BEES_generated_20210909_085536_nn.csv', 2, is_first_run=a)

    # 1stRun 319 -> 180 -> 81 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_144516547_2BEES_generated_20210909_084032_nn.csv', 2, is_first_run=a)

    # 1stRun 91 -> 65 -> 53 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_111450677_2BEES_generated_20210908_084940_nn.csv', 2, is_first_run=a)

    ## 190920
    # 1stRun 85 -> 69 -> 40 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_151014398_2BEES_generated_20210910_084442_nn.csv', 2, is_first_run=a)

    # 1stRun 83 -> 63 -> 40 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_113115350_2BEES_generated_20210909_101941_nn.csv', 2, is_first_run=a)

    # 1stRun 212 -> 147 -> 91 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_160116039_2BEES_generated_20210910_090924_nn.csv', 2, is_first_run=a)

    ## 190922
    # 1stRun 159 -> 104 -> 61 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_161322983_2BEES_generated_20210913_102101_nn.csv', 2, is_first_run=a)

    # 1stRun 316 -> 214 -> 162 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_130906274_2BEES_generated_20210913_092109_nn.csv', 2, is_first_run=a)

    # 1stRun 625 -> 458 -> 300 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_121938174_2BEES_generated_20210913_085059_nn.csv', 2, is_first_run=a)

    ## 190924
    # 1stRun 36 -> 32 -> 26 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_112217708_2BEES_generated_20210916_091354_nn.csv', 2, is_first_run=a)

    # 1stRun 418 -> 246 -> 162 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_122343640_2BEES_generated_20210914_092735_nn.csv', 2, is_first_run=a)

    # 1stRun 148 -> 85 -> 52 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_123434181_2BEES_generated_20210917_092643_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    ## 190925
    # 1stRun 54 -> 44 -> 25 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_133724029_2BEES_generated_20210923_080417_nn.csv', 2, is_first_run=a)

    # 1stRun 554 -> 329 -> 29 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_143533237_2BEES_generated_20210924_100804_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    # 1stRun 43 -> 37 -> 12 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_102758971_2BEES_generated_20210921_074320_nn.csv', 2, is_first_run=a)

    ## 190926
    # 1stRun 581 -> 464 -> 126 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_123223794_2BEES_generated_20210927_081758_nn.csv', 2, is_first_run=a)

    # 1stRun 18 -> 13 -> 5 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_154111693_2BEES_generated_20210927_091414_nn.csv', 2, is_first_run=a)

    ## 190927
    # 1stRun 184 -> 143 -> 21 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_132217029_2BEES_generated_20211004_071921_nn.csv', 2, is_first_run=a)

    # 1stRun 51 -> 23 -> 2 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_143420053_2BEES_generated_20211006_092747_nn.csv', 2, is_first_run=a)

    # 1stRun 135 -> 15 -> 5 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_100233130_2BEES_generated_20210929_091856_nn.csv', 2, is_first_run=a)

    ## 190928
    # 1stRun 169 -> 95 -> 73 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_123940860_2BEES_generated_20211008_095306_nn.csv', 2, is_first_run=a)

    # 1stRun 724 -> 542 -> 36 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_153817856_2BEES_generated_20211008_100947_nn.csv', 2, is_first_run=a)

    # 1stRun 306 -> 197 -> 71 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_111833804_2BEES_generated_20211007_085259_nn.csv', 2, is_first_run=a)

    ## 190929
    # 1stRun 788 -> 513 -> 49 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_162730690_2BEES_generated_20211015_100752_nn.csv', 2, is_first_run=a)

    # 1stRun 19 -> 17 -> 7 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_125545491_2BEES_generated_20211012_100745_nn.csv', 2, is_first_run=a)

    ## 190930
    # 1stRun 541 -> 386 -> 333 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_114339021_2BEES_generated_20211019_104420_nn.csv', 2, is_first_run=a)

    # 1stRun 121 -> 66 -> 16 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_150452483_2BEES_generated_20211018_104843_nn.csv', 2, is_first_run=a)

    # 1stRun 1302 -> 960 -> 558 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_120228598_2BEES_generated_20211020_095955_nn.csv', 2, is_first_run=a)

    ## 191001
    # 1stRun 529 -> 268 -> 57 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_115603481_2BEES_generated_20211026_103521_nn.csv', 2, is_first_run=a)

    # 1stRun 153 -> 107 -> 55 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_144417877_2BEES_generated_20211029_092222_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    ## 191002
    # 1stRun 157 -> 134 -> 98 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_140936347_2BEES_generated_20211221_093930_nn.csv', 2, is_first_run=a)

    # 1stRun 619 -> 429 -> 34 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_105500687_2BEES_generated_20211220_114055_nn.csv', 2, is_first_run=a)

    # 1stRun 98 -> 20 -> 4 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_143119090_2BEES_generated_20211221_111932_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    ## 191003
    # 1stRun 91 -> 68 -> 52 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_102832784_2BEES_generated_20220103_103753_nn.csv', 2, is_first_run=a)

    # 1stRun 89 -> 74 -> 63 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_132915716_2BEES_generated_20211222_105538_nn.csv', 2, is_first_run=a)

    ## 191007
    # 1stRun 24 -> 7 -> 6 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_144544947_2BEES_generated_20220104_112017_nn.csv', 2, is_first_run=a)

    # 1stRun 37 -> 28 -> 24 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_122803196_2BEES_generated_20220104_101818_nn.csv', 2, is_first_run=a)

    # 1stRun 523 -> 362 -> 46 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_115433391_2BEES_generated_20220104_100304_nn.csv', 2, is_first_run=a)

    ## 191008
    # 1stRun 336 -> 222 -> 195 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_153418530_2BEES_generated_20220107_080413_nn.csv', 2, is_first_run=a)

    # 1stRun 969 -> 827 -> 134 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_112936550_2BEES_generated_20220105_111045_nn.csv', 2, is_first_run=a)

    # 1stRun 86 -> 64 -> 18 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_163427285_2BEES_generated_20220107_090018_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    ## 191011
    # 1stRun 825 -> 611 -> 232 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_152233987_2BEES_generated_20220107_104708_nn.csv', 2, has_tracked_video=True, is_first_run=a)

    # 1stRun 240 -> 179 -> 117 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_141916327_2BEES_generated_20220107_095706_nn.csv', 2, is_first_run=a)

    ## 191014
    # 1stRun 64 -> 31 -> 10 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_172842098_2BEES_generated_20220111_104227_nn.csv', 2, is_first_run=a)

    # 1stRun 70 -> 44 -> 22 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_162334757_2BEES_generated_20220110_083827_nn.csv', 2, is_first_run=a)

    ## 191016
    # 1stRun 78 -> 49 -> 29 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_133611699_2BEES_generated_20220118_100833_nn.csv', 2, is_first_run=a)

    # 1stRun 396 -> 232 -> 64 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_171520886_2BEES_generated_20220120_075538_nn.csv', 2, is_first_run=a)

    # 1stRun 141 -> 104 -> 48 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_163301329_2BEES_generated_20220119_104052_nn.csv', 2, is_first_run=a)

    # 1stRun 138 -> 119 -> 84 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_131135997_2BEES_generated_20220118_100012_nn.csv', 2, is_first_run=a)

    # 1stRun 167 -> 91 -> 78 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_122105848_2BEES_generated_20220113_080621_nn.csv', 2, is_first_run=a)

    # 1stRun 184 -> 118 -> 69 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_154420868_2BEES_generated_20220118_102934_nn.csv', 2, is_first_run=a)

    ## 191017
    # 1stRun 113 -> 73 -> 43 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_164812357_2BEES_generated_20220125_075409_nn.csv', 2, is_first_run=a)

    # 1stRun 468 -> 281 -> 82 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_174407911_2BEES_generated_20220125_081624_nn.csv', 2, is_first_run=a)

    ## 191018
    ############################################# 5 BEES #######################################################
    ## 190822
    # 1stRun 526 -> 396 -> 243 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_144547243_5BEE_generated_20210504_081238_nn.csv', 5, is_first_run=a)

    # 1stRun 1416 -> 1085 -> 810 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_114441236_5BEE_generated_20210503_090128_nn.csv', 5, is_first_run=a)

    ## 190823
    # 1stRun 393 -> 263 -> 166 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_155506355_5BEES_generated_20210507_092606_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    # 1stRun 987 -> 785 -> 149 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_121326323_5BEES_generated_20210505_103301_nn.csv', 5, is_first_run=a)

    ## 190903
    # 1stRun 617 -> 478 -> 269 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_123857257_5BEES_generated_20210518_100530_nn.csv', 5, is_first_run=a)

    # 1stRun 1019 -> 717 -> 566 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_163604204_5BEES_generated_20210518_101800_nn.csv', 5, is_first_run=a)

    ## 190904
    # 1stRun 1342 -> 901 -> 434 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_114931998_5BEES_generated_20210521_070732_nn.csv', 5, is_first_run=a)

    # 1stRun 822 -> 566 -> 372 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_160843461_5BEES_generated_20210521_105526_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    ## 190905
    # 1stRun 1101 -> 886 -> 688 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_103753565_5BEES_generated_20210526_083605_nn.csv', 5, is_first_run=a)

    ## 190906
    # 1stRun 328 -> 258 -> 82 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_143609641_5BEES_generated_20210528_110432_nn.csv', 5, is_first_run=a)

    ## 190916
    # 1stRun 548 -> 373 -> 176 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_124925687_5BEES_generated_20210609_101547_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    # 1stRun 1015 -> 888 -> 245 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_151445887_5BEES_generated_20210611_081733_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    # 1stRun 1434 -> 1007 -> 656 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_113158422_5BEES_generated_20210608_081108_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    ## 190917
    # 1stRun 1414 -> 1038 -> 168 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_114532886_5BEES_generated_20210902_081441_nn.csv', 5, is_first_run=a)

    # 1stRun 866 -> 536 -> 316 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_160849711_5BEES_generated_20210906_082822_nn.csv', 5, is_first_run=a)

    # 1stRun 459 -> 383 -> 235 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_154522776_5BEES_generated_20210906_082408_nn.csv', 5, is_first_run=a)

    # 1stRun 836 -> 616 -> 431 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_112136007_5BEES_generated_20210902_080346_nn.csv', 5, is_first_run=a)

    ## 190918
    # 1stRun 466 -> 365 -> 226 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_114551738_5BEES_generated_20210907_085114_nn.csv', 5, is_first_run=a)

    # 1stRun 366 -> 287 -> 158 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_120819051_5BEES_generated_20210907_085557_nn.csv', 5, is_first_run=a)

    ## 190919
    # 1stRun 702 -> 578 -> 260 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_145642660_5BEES_generated_20210909_084740_nn.csv', 5, is_first_run=a)

    # 1stRun 1697 -> 1444 -> 368 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_112617498_5BEES_generated_20210908_085446_nn.csv', 5, is_first_run=a)

    ## 190920
    # 1stRun 265 -> 215 -> 135 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_114320364_5BEES_generated_20210910_074848_nn.csv', 5, is_first_run=a)

    # 1stRun 649 -> 511 -> 315 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_152130894_5BEES_generated_20210910_085916_nn.csv', 5, is_first_run=a)

    ## 190922
    # 1stRun 2167 -> 1557 -> 670 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_162519839_5BEES_generated_20210913_102458_nn.csv', 5, is_first_run=a)

    # 1stRun 434 -> 339 -> 199 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_123119233_5BEES_generated_20210913_090143_nn.csv', 5, is_first_run=a)

    # 1stRun 790 -> 587 -> 332 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_170407464_5BEES_generated_20210913_105016_nn.csv', 5, is_first_run=a)

    ## 190924
    # 1stRun 285 -> 234 -> 169 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_155725679_5BEES_generated_20210917_100221_nn.csv', 5, is_first_run=a)

    # 1stRun 1897 -> 1338 -> 1075 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_113338700_5BEES_generated_20210914_101003_nn.csv', 5, is_first_run=a)

    ## 190925
    # 1stRun 1493 -> 1291 -> 192 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_134854595_5BEES_generated_20210924_083726_nn.csv', 5, is_first_run=a)

    # 1stRun 492 -> 369 -> 210 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_112612419_5BEES_generated_20210924_083010_nn.csv', 5, is_first_run=a)

    # 1stRun 734 -> 548 -> 298 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_103938051_5BEES_generated_20210921_075443_nn.csv', 5, is_first_run=a)

    ## 190926
    # 1stRun 547 -> 397 -> 226 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_124309395_5BEES_generated_20210927_082242_nn.csv', 5, is_first_run=a)

    # 1stRun 294 -> 240 -> 93 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_155223608_5BEES_generated_20210927_093159_nn.csv', 5, is_first_run=a)

    # 1stRun 623 -> 495 -> 331 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_132749818_5BEES_generated_20210927_090107_nn.csv', 5, is_first_run=a)

    ## 190927
    # 1stRun 1428 -> 1078 -> 263 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_101404167_5BEES_generated_20210929_092615_nn.csv', 5, is_first_run=a)

    # 1stRun 986 -> 779 -> 477 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_133332371_5BEES_generated_20211004_102602_nn.csv', 5, is_first_run=a)

    ## 190928
    # 1stRun 549 -> 409 -> 289 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_154847464_5BEES_generated_20211008_101525_nn.csv', 5, is_first_run=a)

    # 1stRun 479 -> 375 -> 279 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_112914182_5BEES_generated_20211007_090731_nn.csv', 5, is_first_run=a)

    ## 190929
    # 1stRun 1307 -> 1161 -> 444 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_112828476_5BEES_generated_20211012_091617_nn.csv', 5, is_first_run=a)

    # 1stRun 558 -> 435 -> 275 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_130356796_5BEES_generated_20211012_105136_nn.csv', 5, is_first_run=a)

    ## 190930
    # 1stRun 1386 -> 437 -> 243 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_151542123_5BEES_generated_20211021_091655_nn.csv', 5, is_first_run=a)

    # 1stRun 834 -> 687 -> 247 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_140834155_5BEES_generated_20211020_104342_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    # 1stRun 852 -> 619 -> 175 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_104322704_5BEES_generated_20211019_090528_nn.csv', 5, is_first_run=a)

    ## 191001
    # 1stRun 1092 -> 729 -> 165 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_120735689_5BEES_generated_20211028_091356_nn.csv', 5, is_first_run=a)

    # 1stRun 1254 -> 773 -> 443 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_145518021_5BEES_generated_20211029_092528_nn.csv', 5, is_first_run=a)

    ## 191002
    # 1stRun 524 -> 423 -> 219 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_142032986_5BEES_generated_20211221_094249_nn.csv', 5, is_first_run=a)

    # 1stRun 444 -> 336 -> 219 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_111706536_5BEES_generated_20211221_081534_nn.csv', 5, is_first_run=a)

    # 1stRun 436 -> 331 -> 208 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_110612551_5BEES_generated_20211220_114435_nn.csv', 5, is_first_run=a)

    ## 191003
    # 1stRun 1417 -> 936 -> 741 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_103917347_5BEES_generated_20220103_105438_nn.csv', 5, has_tracked_video=True, is_first_run=a)

    ## 191007
    # 1stRun 1120 -> 806 -> 102 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_145646554_5BEES_generated_20220105_090348_nn.csv', 5, is_first_run=a)

    # 1stRun 642 -> 464 -> 213 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_120518095_5BEES_generated_20220104_100559_nn.csv', 5, is_first_run=a)

    ## 191008
    # 1stRun 416 -> 332 -> 204 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_114125349_5BEES_generated_20220105_113930_nn.csv', 5, is_first_run=a)

    # 1stRun 518 -> 365 -> 235 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_154602285_5BEES_generated_20220107_081659_nn.csv', 5, is_first_run=a)

    ## 191011
    # 1stRun 1212 -> 890 -> 521 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_143312165_5BEES_generated_20220107_101757_nn.csv', 5, is_first_run=a)

    ## 191014
    # 1stRun 430 -> 330 -> 217 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_163535092_5BEES_generated_20220110_112801_nn.csv', 5, is_first_run=a)

    ## 191016
    ## 191017
    # 1stRun 1621 -> 1294 -> 232 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_170435649_5BEES_generated_20220125_080034_nn.csv', 5, is_first_run=a)

    ## 191018
    ############################################# 7 BEES #######################################################
    ## 190822
    # 1stRun 701 -> 499 -> 289 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_115819107_7BEE_generated_20210504_064122_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    ## 190823
    # 1stRun 477 -> 357 -> 192 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_124111790_7BEES_generated_20210507_070601_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    # 1stRun 895 -> 632 -> 354 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_161115188_7BEES_generated_20210507_093529_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    ## 190903
    # 1stRun 1581 -> 1249 -> 884 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_164946455_7BEES_generated_20210520_072655_nn.csv', 7, is_first_run=a)

    # 1stRun 1787 -> 1450 -> 1081 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_125405366_7BEES_generated_20210511_101622_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    ## 190904
    # 1stRun 588 -> 510 -> 344 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_120427978_7BEES_generated_20210520_094906_nn.csv', 7, is_first_run=a)

    # 1stRun 519 -> 435 -> 318 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_162106341_7BEES_generated_20210525_094920_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    ## 190905
    # 1stRun 487 -> 413 -> 251 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_105024299_7BEES_generated_20210527_095135_nn.csv', 7, is_first_run=a)

    ## 190906
    # 1stRun 1961 -> 1602 -> 602 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_160755199_7BEES_generated_20210607_103715_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    # 1stRun 1641 -> 1312 -> 822 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_144808288_7BEES_generated_20210601_065020_nn.csv', 7, is_first_run=a)

    ## 190916
    # 1stRun 1045 -> 783 -> 538 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_114706187_7BEES_generated_20210608_083833_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    # 1stRun 1008 -> 819 -> 240 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_152713294_7BEES_generated_20210611_093450_nn.csv', 7, is_first_run=a)

    ## 190917
    # 1stRun 623 -> 494 -> 85 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_144741012_7BEES_generated_20210903_084740_nn.csv', 7, is_first_run=a)

    # 1stRun 2032 -> 1775 -> 392 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_101841919_7BEES_generated_20210802_103203_nn.csv', 7, is_first_run=a)

    # 1stRun 879 -> 765 -> 382 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_113355567_7BEES_generated_20210902_080817_nn.csv', 7, is_first_run=a)

    ## 190918
    # 1stRun 1448 -> 1225 -> 239 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_103136704_7BEES_generated_20210907_080630_nn.csv', 7, is_first_run=a)

    ## 190919
    # 1stRun 578 -> 469 -> 286 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_150757868_7BEES_generated_20210909_085206_nn.csv', 7, is_first_run=a)

    ## 190920
    # 1stRun 1128 -> 846 -> 472 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_153621158_7BEES_generated_20210910_090227_nn.csv', 7, is_first_run=a)

    # 1stRun 1986 -> 1540 -> 793 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_115510532_7BEES_generated_20210910_075313_nn.csv', 7, is_first_run=a)

    ## 190922
    # 1stRun 1829 -> 1539 -> 375 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_124337481_7BEES_generated_20210913_090812_nn.csv', 7, is_first_run=a)

    # 1stRun 1316 -> 1016 -> 485 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_163734553_7BEES_generated_20210913_103924_nn.csv', 7, is_first_run=a)

    ## 190924
    # 1stRun 1242 -> 1031 -> 500 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_120836685_7BEES_generated_20210917_090547_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    # 1stRun 978 -> 760 -> 414 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_160900567_7BEES_generated_20210917_100948_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    # 1stRun 649 -> 531 -> 386 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_114532177_7BEES_generated_20210917_080433_nn.csv', 7, is_first_run=a)

    ## 190925
    # 1stRun 580 -> 477 -> 294 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_140057430_7BEES_generated_20210924_084455_nn.csv', 7, is_first_run=a)

    # 1stRun 984 -> 669 -> 521 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_105112451_7BEES_generated_20210923_075138_nn.csv', 7, is_first_run=a)

    ## 190926
    # 1stRun 584 -> 502 -> 350 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_125410450_7BEES_generated_20210927_085009_nn.csv', 7, is_first_run=a)

    # 1stRun 1770 -> 847 -> 338 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_160353069_7BEES_generated_20210928_090140_nn.csv', 7, is_first_run=a)

    ## 190927
    # 1stRun 2584 -> 1465 -> 453 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_134508012_7BEES_generated_20211004_104131_nn.csv', 7, is_first_run=a)

    # 1stRun 557 -> 440 -> 256 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_102553712_7BEES_generated_20210929_094812_nn.csv', 7, has_tracked_video=True, is_first_run=a)

    ## 190928
    # 1stRun 881 -> 714 -> 293 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_155945481_7BEES_generated_20211008_101936_nn.csv', 7, is_first_run=a)

    # 1stRun 1659 -> 1400 -> 417 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_120344285_7BEES_generated_20211007_100845_nn.csv', 7, is_first_run=a)

    ## 190929
    # 1stRun 1969 -> 1351 -> 759 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_120828030_7BEES_generated_20211012_093441_nn.csv', 7, is_first_run=a)

    # 1stRun 2181 -> 1928 -> 522 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_154221664_7BEES_generated_20211015_082847_nn.csv', 7, is_first_run=a)

    ## 190930
    # 1stRun 1026 -> 867 -> 389 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_105454916_7BEES_generated_20211019_094651_nn.csv', 7, is_first_run=a)

    # 1stRun 1804 -> 1430 -> 532 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_141958074_7BEES_generated_20211018_100514_nn.csv', 7, is_first_run=a)

    ## 191001
    # 1stRun 2175 -> 1407 -> 492 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_110859586_7BEES_generated_20211026_091754_nn.csv', 7, is_first_run=a)

    # 1stRun 1340 -> 1060 -> 720 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_135710524_7BEES_generated_20211028_093407_nn.csv', 7, is_first_run=a)

    ## 191002
    # 1stRun 1411 -> 1106 -> 525 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_132353995_7BEES_generated_20211221_111451_nn.csv', 7, is_first_run=a)

    # 1stRun 2086 -> 1488 -> 1162 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_100933697_7BEES_generated_20211102_112714_nn.csv', 7, is_first_run=a)

    ## 191003
    # 1stRun 1500 -> 1087 -> 743 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_124508386_7BEES_generated_20211222_110729_nn.csv', 7, is_first_run=a)

    # 1stRun 1322 -> 1104 -> 707 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_105007235_7BEES_generated_20211222_105307_nn.csv', 7, is_first_run=a)

    ## 191007
    # 1stRun 1352 -> 1144 -> 412 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_121631764_7BEES_generated_20220104_101432_nn.csv', 7, is_first_run=a)

    # 1stRun 1545 -> 1093 -> 661 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_150734667_7BEES_generated_20220105_090956_nn.csv', 7, is_first_run=a)

    ## 191008
    # 1stRun 1570 -> 1360 -> 297 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_155753645_7BEES_generated_20220107_083514_nn.csv', 7, is_first_run=a)

    # 1stRun 964 -> 722 -> 428 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_121926491_7BEES_generated_20220107_065423_nn.csv', 7, is_first_run=a)

    # 1stRun 990 -> 721 -> 373 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_115300009_7BEES_generated_20220107_064230_nn.csv', 7, is_first_run=a)

    ## 191011
    # 1stRun 1106 -> 865 -> 597 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_144612813_7BEES_generated_20220107_102150_nn.csv', 7, is_first_run=a)

    ## 191014
    # 1stRun 2091 -> 1783 -> 532 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_164746859_7BEES_generated_20220110_114635_nn.csv', 7, is_first_run=a)

    ## 191016
    # 1stRun 769 -> 624 -> 385 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_165116992_7BEES_generated_20220120_073941_nn.csv', 7, is_first_run=a)

    # 1stRun 917 -> 754 -> 403 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_155641331_7BEES_generated_20220119_090250_nn.csv', 7, is_first_run=a)

    ## 191017
    # 1stRun 1691 -> 1378 -> 530 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_171732489_7BEES_generated_20220125_080511_nn.csv', 7, is_first_run=a)

    # 1stRun 746 -> 585 -> 395 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_175536577_7BEES_generated_20220125_085512_nn.csv', 7, is_first_run=a)

    # 1stRun 2029 -> 1492 -> 513 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_124248837_7BEES_generated_20220121_113202_nn.csv', 7, is_first_run=a)

    ## 191018
    # 1stRun 995 -> 793 -> 460 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_124446161_7BEES_generated_20220126_101034_nn.csv', 7, is_first_run=a)

    ############################################# 10 BEES #######################################################
    ## 190822
    # 1stRun 2126 -> 1549 -> 633 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_121127355_10BEE_generated_20210430_102736_nn.csv', 10, is_first_run=a)

    # 1stRun 1707 -> 1319 -> 984 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_151158355_10BEE_generated_20210504_082545_nn.csv', 10, is_first_run=a)

    ## 190823
    # 1stRun 2225 -> 1836 -> 850 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_162410226_10BEES_generated_20210510_080842_nn.csv', 10, is_first_run=a)

    ## 190903
    # 1stRun 2837 -> 2351 -> 1668 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_131117672_10BEES_generated_20210511_062341_nn.csv', 10, is_first_run=a)

    # 1stRun 865 -> 726 -> 316 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_170217904_10BEES_generated_20210512_071725_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 190904
    # 1stRun 1338 -> 1167 -> 487 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_121723342_10BEES_generated_20210520_103316_nn.csv', 10, is_first_run=a)

    # 1stRun 1250 -> 875 -> 442 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_163324719_10BEES_generated_20210525_100838_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 190905
    # 1stRun 1478 -> 1352 -> 439 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_110548502_10BEES_generated_20210527_094614_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 190906
    # 1stRun 1494 -> 1303 -> 757 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_150041160_10BEES_generated_20210601_071145_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 190916
    # 1stRun 1576 -> 1378 -> 741 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_120207930_10BEES_generated_20210608_085327_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    # 1stRun 1548 -> 1253 -> 852 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_153917173_10BEES_generated_20210611_102923_nn.csv', 10, is_first_run=a)

    ## 190917
    # 1stRun 1734 -> 1409 -> 609 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_103038278_10BEES_generated_20210802_104137_nn.csv', 10, is_first_run=a)

    # 1stRun 2698 -> 2168 -> 813 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_145905704_10BEES_generated_20210903_091715_nn.csv', 10, is_first_run=a)

    ## 190918
    # 1stRun 1485 -> 1205 -> 857 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_104441181_10BEES_generated_20210907_080942_nn.csv', 10, is_first_run=a)

    ## 190919
    # 1stRun 1358 -> 1197 -> 757 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_141048700_10BEES_generated_20210908_091000_nn.csv', 10, is_first_run=a)

    ## 190920
    # 1stRun 2069 -> 1608 -> 732 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_143418975_10BEES_generated_20210910_081548_nn.csv', 10, is_first_run=a)

    ## 190922
    # 1stRun 1034 -> 855 -> 623 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_164935024_10BEES_generated_20210913_104649_nn.csv', 10, is_first_run=a)

    # 1stRun 1010 -> 865 -> 644 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_125541361_10BEES_generated_20210916_083116_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 190924
    # 1stRun 1592 -> 1247 -> 621 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_162018096_10BEES_generated_20210917_101357_nn.csv', 10, is_first_run=a)

    # 1stRun 2198 -> 1648 -> 1034 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_163201296_10BEES_generated_20210917_101746_nn.csv', 10, is_first_run=a)

    # 1stRun 2148 -> 1788 -> 658 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_115712296_10BEES_generated_20210917_080744_nn.csv', 10, is_first_run=a)

    ## 190925
    # 1stRun 2234 -> 1963 -> 651 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_110237085_10BEES_generated_20210924_082144_nn.csv', 10, is_first_run=a)

    ## 190926
    # 1stRun 1346 -> 1049 -> 635 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_161520655_10BEES_generated_20210928_090610_nn.csv', 10, is_first_run=a)

    ## 190927
    # 1stRun 2202 -> 1949 -> 465 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_135709044_10BEES_generated_20211005_094101_nn.csv', 10, is_first_run=a)

    # 1stRun 2172 -> 1876 -> 1009 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_103759768_10BEES_generated_20210929_104342_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 190928
    # 1stRun 982 -> 806 -> 370 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_122031371_10BEES_generated_20211007_103125_nn.csv', 10, is_first_run=a)

    # 1stRun 1740 -> 1381 -> 824 *
    #  ->  ->
    analyse('../data/Video_tracking/190928/20190928_161235208_10BEES_generated_20211008_102614_nn.csv', 10, is_first_run=a)

    ## 190929
    # 1stRun 1103 -> 984 -> 521 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_121957315_10BEES_generated_20211012_094335_nn.csv', 10, is_first_run=a)

    # 1stRun 1815 -> 1488 -> 555 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_155407984_10BEES_generated_20211015_094028_nn.csv', 10, is_first_run=a)

    ## 190930
    # 1stRun 2938 -> 2269 -> 1077 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_143111210_10BEES_generated_20211018_101123_nn.csv', 10, is_first_run=a)

    # 1stRun 1893 -> 1682 -> 745 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_110620060_10BEES_generated_20211019_095354_nn.csv', 10, is_first_run=a)

    ## 191001
    # 1stRun 1925 -> 1582 -> 750 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_140821748_10BEES_generated_20211028_094845_nn.csv', 10, is_first_run=a)

    # 1stRun 990 -> 825 -> 501 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_112031240_10BEES_generated_20211026_092048_nn.csv', 10, is_first_run=a)

    ## 191002
    # 1stRun 2269 -> 1791 -> 733 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_102112781_10BEES_generated_20211220_113720_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    # 1stRun 2036 -> 1487 -> 857 *
    #  ->  ->
    analyse('../data/Video_tracking/191002/20191002_133525621_10BEES_generated_20211222_080816_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    ## 191003
    # 1stRun 1615 -> 1259 -> 904 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_125620288_10BEES_generated_20211222_105417_nn.csv', 10, is_first_run=a)

    # 1stRun 1601 -> 1306 -> 691 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_095527912_10BEES_generated_20211222_105139_nn.csv', 10, is_first_run=a)

    ## 191007
    # 1stRun 2952 -> 2581 -> 1093 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_141118287_10BEES_generated_20220104_105737_nn.csv', 10, is_first_run=a)

    # 1stRun 2191 -> 1878 -> 738 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_111802396_10BEES_generated_20220103_115134_nn.csv', 10, is_first_run=a)

    ## 191008
    # 1stRun 1109 -> 982 -> 600 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_161034917_10BEES_generated_20220107_084847_nn.csv', 10, is_first_run=a)

    # 1stRun 2013 -> 1624 -> 1078 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_120529380_10BEES_generated_20220107_064857_nn.csv', 10, is_first_run=a)

    ## 191011
    # 1stRun 1716 -> 1357 -> 774 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_145822566_10BEES_generated_20220107_102527_nn.csv', 10, is_first_run=a)

    ## 191014
    # 1stRun 2613 -> 2116 -> 1217 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_170158067_10BEES_generated_20220111_080114_nn.csv', 10, is_first_run=a)

    ## 191016
    # 1stRun 2493 -> 2028 -> 937 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_132346782_10BEES_generated_20220118_100307_nn.csv', 10, is_first_run=a)

    # 1stRun 1220 -> 1037 -> 693 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_160838515_10BEES_generated_20220119_090556_nn.csv', 10, is_first_run=a)

    # 1stRun 1076 -> 888 -> 596 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_123316519_10BEES_generated_20220113_125257_nn.csv', 10, is_first_run=a)

    # 1stRun 2090 -> 1496 -> 920 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_170332465_10BEES_generated_20220120_075126_nn.csv', 10, is_first_run=a)

    ## 191017
    # 1stRun 1194 -> 989 -> 483 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_132743751_10BEES_generated_20220121_115258_nn.csv', 10, has_tracked_video=True, is_first_run=a)

    # 1stRun 1762 -> 1399 -> 578 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_125419660_10BEES_generated_20220121_113743_nn.csv', 10, is_first_run=a)

    ## 191018
    # 1stRun 1316 -> 1126 -> 664 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_131957590_10BEES_generated_20220125_104309_nn.csv', 10, is_first_run=a)

    # 1stRun 2768 -> 2433 -> 448 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_125650447_10BEES_generated_20220125_102149_nn.csv', 10, is_first_run=a)

    ############################################# 15 BEES #######################################################
    ## 190822
    # 1stRun 2174 -> 1764 -> 1344 *
    #  ->  ->
    analyse('../data/Video_tracking/190822/20190822_122407809_15BEE_generated_20210803_085008_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    ## 190823
    # 1stRun 2190 -> 1935 -> 1095 *
    #  ->  ->
    analyse('../data/Video_tracking/190823/20190823_163934743_15BEES_generated_20210510_082044_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    ## 190903
    # 1stRun 2337 -> 2052 -> 1281 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_171612563_15BEES_generated_20210518_101121_nn.csv', 15, is_first_run=a)

    # 1stRun 3212 -> 2783 -> 1652 *
    #  ->  ->
    analyse('../data/Video_tracking/190903/20190903_132435095_15BEES_generated_20210511_063736_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    ## 190904
    # 1stRun 1428 -> 1270 -> 762 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_164507538_15BEES_generated_20210525_103318_nn.csv', 15, is_first_run=a)

    # 1stRun 3496 -> 3084 -> 1514 *
    #  ->  ->
    analyse('../data/Video_tracking/190904/20190904_123252421_15BEES_generated_20210521_063745_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    ## 190905
    # 1stRun 2374 -> 2195 -> 858 *
    #  ->  ->
    analyse('../data/Video_tracking/190905/20190905_111848284_15BEES_generated_20210527_103530_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    ## 190906
    # 1stRun 2220 -> 1911 -> 974 *
    #  ->  ->
    analyse('../data/Video_tracking/190906/20190906_151436479_15BEES_generated_20210607_081516_nn.csv', 15, is_first_run=a)

    ## 190916
    # 1stRun 3346 -> 2938 -> 751 *
    #  ->  ->
    analyse('../data/Video_tracking/190916/20190916_155142744_15BEES_generated_20210611_105921_nn.csv', 15, is_first_run=a)

    ## 190917
    # 1stRun 2294 -> 1997 -> 1374 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_151102123_15BEES_generated_20210903_100118_nn.csv', 15, is_first_run=a)

    # 1stRun 3739 -> 3337 -> 992 *
    #  ->  ->
    analyse('../data/Video_tracking/190917/20190917_104532152_15BEES_generated_20210803_082437_nn.csv', 15, is_first_run=a)

    ## 190918
    # 1stRun 1903 -> 1758 -> 1114 *
    #  ->  ->
    analyse('../data/Video_tracking/190918/20190918_105639722_15BEES_generated_20210907_081259_nn.csv', 15, is_first_run=a)

    ## 190919
    # 1stRun 3200 -> 2743 -> 1779 *
    #  ->  ->
    analyse('../data/Video_tracking/190919/20190919_105145877_15BEES_generated_20210908_083852_nn.csv', 15, is_first_run=a)

    ## 190920
    # 1stRun 1961 -> 1628 -> 897 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_144702326_15BEES_generated_20210910_082748_nn.csv', 15, is_first_run=a)

    # 1stRun 2925 -> 2639 -> 1020 *
    #  ->  ->
    analyse('../data/Video_tracking/190920/20190920_110628291_15BEES_generated_20210909_095322_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    ## 190922
    # 1stRun 3337 -> 2955 -> 1284 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_154352238_15BEES_generated_20210913_095813_nn.csv', 15, is_first_run=a)

    # 1stRun 2154 -> 1828 -> 1059 *
    #  ->  ->
    analyse('../data/Video_tracking/190922/20190922_115427042_15BEES_generated_20210913_074557_nn.csv', 15, is_first_run=a)

    ## 190924
    # 1stRun 2413 -> 2124 -> 1427 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_105949133_15BEES_generated_20210916_083521_nn.csv', 15, is_first_run=a)

    # 1stRun 2236 -> 1931 -> 1142 *
    #  ->  ->
    analyse('../data/Video_tracking/190924/20190924_152226497_15BEES_generated_20210914_095925_nn.csv', 15, is_first_run=a)

    ## 190925
    # 1stRun 1904 -> 1655 -> 1093 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_142354429_15BEES_generated_20210924_084837_nn.csv', 15, is_first_run=a)

    # 1stRun 1993 -> 1727 -> 1077 *
    #  ->  ->
    analyse('../data/Video_tracking/190925/20190925_111416348_15BEES_generated_20210924_082629_nn.csv', 15, is_first_run=a)

    ## 190926
    # 1stRun 2712 -> 2188 -> 1261 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_162712758_15BEES_generated_20210928_090840_nn.csv', 15, is_first_run=a)

    # 1stRun 1974 -> 1727 -> 677 *
    #  ->  ->
    analyse('../data/Video_tracking/190926/20190926_131641554_15BEES_generated_20210927_085812_nn.csv', 15, is_first_run=a)

    ## 190927
    # 1stRun 2255 -> 1792 -> 721 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_105015136_15BEES_generated_20211001_084351_nn.csv', 15, is_first_run=a)

    # 1stRun 1906 -> 1663 -> 500 *
    #  ->  ->
    analyse('../data/Video_tracking/190927/20190927_140903972_15BEES_generated_20211006_092141_nn.csv', 15, is_first_run=a)

    ## 190928
    ## 190929
    # 1stRun 3051 -> 2575 -> 908 *
    #  ->  ->
    analyse('../data/Video_tracking/190929/20190929_160530530_15BEES_generated_20211015_094803_nn.csv', 15, is_first_run=a)

    ## 190930
    # 1stRun 2350 -> 1902 -> 1277 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_144234627_15BEES_generated_20211018_100830_nn.csv', 15, is_first_run=a)

    # 1stRun 2089 -> 1790 -> 1021 *
    #  ->  ->
    analyse('../data/Video_tracking/190930/20190930_111749856_15BEES_generated_20211019_101232_nn.csv', 15, is_first_run=a)

    ## 191001
    # 1stRun 3989 -> 3543 -> 1817 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_141957735_15BEES_generated_20211028_095546_nn.csv', 15, has_tracked_video=True, is_first_run=a)

    # 1stRun 2823 -> 2406 -> 1442 *
    #  ->  ->
    analyse('../data/Video_tracking/191001/20191001_113225056_15BEES_generated_20211026_092637_nn.csv', 15, is_first_run=a)

    ## 191002
    ## 191003
    # 1stRun 2674 -> 2335 -> 1468 *
    #  ->  ->
    analyse('../data/Video_tracking/191003/20191003_130715174_15BEES_generated_20220103_113351_nn.csv', 15, is_first_run=a)

    ## 191007
    # 1stRun 2606 -> 2342 -> 1251 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_142243717_15BEES_generated_20220105_085425_nn.csv', 15, is_first_run=a)

    # 1stRun 3524 -> 3055 -> 1803 *
    #  ->  ->
    analyse('../data/Video_tracking/191007/20191007_112941330_15BEES_generated_20220104_095854_nn.csv', 15, is_first_run=a)

    ## 191008
    # 1stRun 2960 -> 2454 -> 1718 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_110243113_15BEES_generated_20220105_103922_nn.csv', 15, is_first_run=a)

    # 1stRun 2664 -> 2194 -> 1432 *
    #  ->  ->
    analyse('../data/Video_tracking/191008/20191008_150528777_15BEES_generated_20220107_072438_nn.csv', 15, is_first_run=a)

    ## 191011
    # 1stRun 2884 -> 2500 -> 1270 *
    #  ->  ->
    analyse('../data/Video_tracking/191011/20191011_134945372_15BEES_generated_20220107_091631_nn.csv', 15, is_first_run=a)

    ## 191014
    # 1stRun 3340 -> 2980 -> 1555 *
    #  ->  ->
    analyse('../data/Video_tracking/191014/20191014_155509712_15BEES_generated_20220110_074244_nn.csv', 15, is_first_run=a)

    ## 191016
    # 1stRun 2671 -> 2316 -> 1539 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_162046345_15BEES_generated_20220119_095913_nn.csv', 15, is_first_run=a)

    # 1stRun 2249 -> 1965 -> 1376 *
    #  ->  ->
    analyse('../data/Video_tracking/191016/20191016_124613239_15BEES_generated_20220117_104800_nn.csv', 15, is_first_run=a)

    ## 191017
    # 1stRun 2760 -> 2355 -> 1436 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_130555083_15BEES_generated_20220121_114232_nn.csv', 15, is_first_run=a)

    # 1stRun 2566 -> 2068 -> 1297 *
    #  ->  ->
    analyse('../data/Video_tracking/191017/20191017_133858498_15BEES_generated_20220124_101400_nn.csv', 15, is_first_run=a)

    ## 191018
    # 1stRun 2791 -> 2304 -> 1606 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_133057695_15BEES_generated_20220126_102759_nn.csv', 15, is_first_run=a)

    # 1stRun 2606 -> 2235 -> 1912 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_142523619_15BEES_generated_20220125_103406_nn.csv', 15, is_first_run=a)

    # 1stRun 2171 -> 1935 -> 1527 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_143615609_15BEES_generated_20220126_104502_nn.csv', 15, is_first_run=a)

    # 1stRun 1843 -> 1565 -> 1107 *
    #  ->  ->
    analyse('../data/Video_tracking/191018/20191018_130828543_15BEES_generated_20220125_102542_nn.csv', 15, is_first_run=a)


if __name__ == "__main__":
    # align_first()
    run(is_first_run=True)
    # print("get_all_overlaps_count()", get_all_overlaps_count())
    # print("get_all_allowed_overlaps_count()", get_all_allowed_overlaps_count())
    # print("get_all_seen_overlaps_deleted()", get_all_seen_overlaps_deleted())
    # run_both()
    # run_just_annotate()
