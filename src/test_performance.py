import analyse
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
    #### EASY
    # Already done and SAVED
    analyse('../data/Video_tracking/190822/20190822_111607344_1BEE_generated_20210430_080914_nn.csv', 1, is_first_run=a)

    # WTF 123 -> 35 -> 1  Done
    analyse('../data/Video_tracking/190916/20190916_160703748_1BEE_generated_20210611_111022_nn.csv', 1, is_first_run=a)

    ## INTERMEDIATE
    # 156 -> 87 -> 11 -> 1
    # 156 -> 69 -> 9 -> 1 (4/10/22)
    analyse('../data/Video_tracking/190822/20190822_141925574_1bee_generated_20210504_081658_nn.csv', 1, is_first_run=a)

    # WTF 391 -> 291 -> 3
    # 391 -> 291 -> 1 (not guided)
    # 391 -> 291 -> 1 (by min_trace_len)
    analyse('../data/Video_tracking/190916/20190916_122643082_1BEE_generated_20210608_090120_nn.csv', 1, is_first_run=a)

    ## HARD
    # WTF 748 -> 449 -> 3
    # WTF 748 -> 449 -> 1 (not guided)
    analyse('../data/Video_tracking/190916/20190916_163119085_1BEE_generated_20210618_080129_nn.csv', 1, is_first_run=a)

    # 917 -> 701 -> 1 *
    analyse("../data/Video_tracking/190917/20190917_153417672_1BEE_generated_20210906_080339_nn.csv", 1, is_first_run=a)

    # 999 -> 744 -> 29 *
    analyse("../data/Video_tracking/190920/20190920_145859333_1BEE_generated_20210910_083808_nn.csv", 1, is_first_run=a)

    ## 190924
    # WTF with larger force_merge_vicinity fewer traces
    # 617 -> 422 -> 21
    # 617 -> 422 -> 3
    # 617 -> 422 -> 1, video-guided delete
    analyse("../data/Video_tracking/190924/20190924_111059331_1BEE_generated_20210916_090912_nn.csv", 1, has_tracked_video=True, is_first_run=a)

    ## 190925
    # 922 -> 692 -> 45
    # 922 -> 692 -> 42
    # 922 -> 692 -> 3
    analyse("../data/Video_tracking/190925/20190925_101651861_1BEE_generated_20210921_073505_nn.csv", 1, is_first_run=a)

    ############################################ 2 BEES #######################################################
    # EASY
    # 11 -> 8 -> 2 *
    analyse("../data/Video_tracking/190905/20190905_115416146_2BEES_generated_20210528_065454_nn.csv", 2, is_first_run=a)

    # 28 -> 26 -> 8 *
    analyse("../data/Video_tracking/190916/20190916_164302025_2BEES_generated_20210618_095944_nn.csv", 2, is_first_run=a)

    # INTERMEDIATE
    ## 190822
    # a lot of jump back and forth
    # one swap of traces
    # 65 -> 56 -> 25 (12/10/22)
    # 65 -> 56 -> 2 (16/10/22)
    analyse("../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv", 2, [41159], has_tracked_video=True, is_first_run=a)

    # HARD
    # 1034 -> 650 -> 4 *
    analyse("../data/Video_tracking/190903/20190903_122246620_2BEES_generated_20210511_083802_nn.csv", 2, is_first_run=a)

    ## 190904
    # 1016 -> 748 -> 637
    analyse("../data/Video_tracking/190904/20190904_113737340_2BEES_generated_20210521_065405_nn.csv", 2, has_tracked_video=True, is_first_run=a)

    # 747 -> 609 -> 4 *
    # got more traces with higher min_trace_len
    analyse("../data/Video_tracking/190919/20190919_151934478_2BEES_generated_20210909_085536_nn.csv", 2, is_first_run=a)

    ############################################# 5 BEES #######################################################
    #### EASY
    # 265 -> 230 -> 142
    analyse("../data/Video_tracking/190920/20190920_114320364_5BEES_generated_20210910_074848_nn.csv", 5, is_first_run=a)

    # 285 -> 246 -> 216
    analyse("../data/Video_tracking/190924/20190924_155725679_5BEES_generated_20210917_100221_nn.csv", 5,
            is_first_run=a)

    # 328 -> 284 -> 66
    analyse("../data/Video_tracking/190906/20190906_143609641_5BEES_generated_20210528_110432_nn.csv", 5,
            is_first_run=a)

    # 379 -> 266 -> 223
    analyse("../data/Video_tracking/190823/20190823_155506355_5BEES_generated_20210507_092606_nn.csv", 5,
            has_tracked_video=True, is_first_run=a)

    ## INTERMEDIATE
    # 548 -> 418 -> 159
    analyse("../data/Video_tracking/190916/20190916_124925687_5BEES_generated_20210609_101547_nn.csv", 5,
            has_tracked_video=True, is_first_run=a)

    # # 526 -> 415 -> 253
    analyse("../data/Video_tracking/190822/20190822_144547243_5BEE_generated_20210504_081238_nn.csv", 5, is_first_run=a)

    # 459 -> 403 -> 306
    analyse("../data/Video_tracking/190917/20190917_154522776_5BEES_generated_20210906_082408_nn.csv", 5, is_first_run=a)

    # 987 -> 791 -> 141
    analyse("../data/Video_tracking/190823/20190823_121326323_5BEES_generated_20210505_103301_nn.csv", 5, is_first_run=a)

    ## HARD
    # 1414 -> 1044 -> 239
    analyse("../data/Video_tracking/190917/20190917_114532886_5BEES_generated_20210902_081441_nn.csv", 5, is_first_run=a)

    # 1342 -> 908 -> 387
    analyse("../data/Video_tracking/190904/20190904_114931998_5BEES_generated_20210521_070732_nn.csv", 5, is_first_run=a)

    # 1697 -> 1445 -> 522
    analyse("../data/Video_tracking/190919/20190919_112617498_5BEES_generated_20210908_085446_nn.csv", 5, is_first_run=a)

    # 2167 -> 1561 -> 445
    analyse("../data/Video_tracking/190922/20190922_162519839_5BEES_generated_20210913_102458_nn.csv", 5, is_first_run=a)

    # 1897 -> 1339 -> 958
    analyse("../data/Video_tracking/190924/20190924_113338700_5BEES_generated_20210914_101003_nn.csv", 5, is_first_run=a)

    ############################################# 7 BEES #######################################################
    ## EASY
    # 477 -> 357 -> 225 *
    analyse("../data/Video_tracking/190823/20190823_124111790_7BEES_generated_20210507_070601_nn.csv", 7,
            has_tracked_video=True, is_first_run=a)

    # 519 -> 435 -> 385 *
    analyse("../data/Video_tracking/190904/20190904_162106341_7BEES_generated_20210525_094920_nn.csv", 7,
            has_tracked_video=True, is_first_run=a)


    ## INTERMEDIATE
    # 701 -> 499 -> 365 *
    analyse("../data/Video_tracking/190822/20190822_115819107_7BEE_generated_20210504_064122_nn.csv", 7,
            has_tracked_video=True, is_first_run=a)

    # 895 -> 632 -> 394 *
    analyse("../data/Video_tracking/190823/20190823_161115188_7BEES_generated_20210507_093529_nn.csv", 7,
            has_tracked_video=True, is_first_run=a)

    ## HARD
    # 1787 -> 1450 -> 1146 *
    analyse("../data/Video_tracking/190903/20190903_125405366_7BEES_generated_20210511_101622_nn.csv", 7,
            has_tracked_video=True, is_first_run=a)

    # 1961 -> 1602 -> 691 *
    analyse("../data/Video_tracking/190906/20190906_160755199_7BEES_generated_20210607_103715_nn.csv", 7, has_tracked_video=True, is_first_run=a)

    # 2584 -> 1465 -> 626 *
    analyse("../data/Video_tracking/190927/20190927_134508012_7BEES_generated_20211004_104131_nn.csv", 7,
            is_first_run=a)

    ############################################# 10 BEES #######################################################
    ## TODO FINISH
    # # 865 -> 726 -> 409 *
    # analyse("../data/Video_tracking/190903/20190903_170217904_10BEES_generated_20210512_071725_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 190822
    # # 2126 -> 1549 -> 790 *
    # analyse("../data/Video_tracking/190822/20190822_121127355_10BEE_generated_20210430_102736_nn.csv", 10, is_first_run=a)
    #
    # # 1707 -> 1319 -> 1103 *
    # analyse("../data/Video_tracking/190822/20190822_151158355_10BEE_generated_20210504_082545_nn.csv", 10, is_first_run=a)
    #
    # ## 190823
    # # 2225 -> 1836 -> 986 *
    # analyse("../data/Video_tracking/190823/20190823_162410226_10BEES_generated_20210510_080842_nn.csv", 10, is_first_run=a)
    #
    # ## 190903
    # # 2837 -> 2351 -> 1868 *
    # analyse("../data/Video_tracking/190903/20190903_131117672_10BEES_generated_20210511_062341_nn.csv", 10, is_first_run=a)
    #
    # ## 190904
    # # 1338 -> 1167 -> 655 *
    # analyse("../data/Video_tracking/190904/20190904_121723342_10BEES_generated_20210520_103316_nn.csv", 10,
    #         is_first_run=a)
    #
    # # 1250 -> 875 -> 495 *
    # analyse("../data/Video_tracking/190904/20190904_163324719_10BEES_generated_20210525_100838_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 190905
    # #  ->  ->
    # analyse("../data/Video_tracking/190905/20190905_110548502_10BEES_generated_20210527_094614_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 190906
    # #  ->  ->
    # analyse("../data/Video_tracking/190906/20190906_150041160_10BEES_generated_20210601_071145_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 190916
    # #  ->  ->
    # analyse("../data/Video_tracking/190916/20190916_120207930_10BEES_generated_20210608_085327_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190916/20190916_153917173_10BEES_generated_20210611_102923_nn.csv", 10, is_first_run=a)
    #
    # ## 190917
    # #  ->  ->
    # analyse("../data/Video_tracking/190917/20190917_103038278_10BEES_generated_20210802_104137_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190917/20190917_145905704_10BEES_generated_20210903_091715_nn.csv", 10, is_first_run=a)
    #
    # ## 190918
    # #  ->  ->
    # analyse("../data/Video_tracking/190918/20190918_104441181_10BEES_generated_20210907_080942_nn.csv", 10, is_first_run=a)
    #
    # ## 190919
    # #  ->  ->
    # analyse("../data/Video_tracking/190919/20190919_141048700_10BEES_generated_20210908_091000_nn.csv", 10, is_first_run=a)
    #
    # ## 190920
    # #  ->  ->
    # analyse("../data/Video_tracking/190920/20190920_143418975_10BEES_generated_20210910_081548_nn.csv", 10, is_first_run=a)
    #
    # ## 190922
    # #  ->  ->
    # analyse("../data/Video_tracking/190922/20190922_164935024_10BEES_generated_20210913_104649_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190922/20190922_125541361_10BEES_generated_20210916_083116_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 190924
    # #  ->  ->
    # analyse("../data/Video_tracking/190924/20190924_162018096_10BEES_generated_20210917_101357_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190924/20190924_163201296_10BEES_generated_20210917_101746_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190924/20190924_115712296_10BEES_generated_20210917_080744_nn.csv", 10, is_first_run=a)
    #
    # ## 190925
    # #  ->  ->
    # analyse("../data/Video_tracking/190925/20190925_110237085_10BEES_generated_20210924_082144_nn.csv", 10, is_first_run=a)
    #
    # ## 190926
    # #  ->  ->
    # analyse("../data/Video_tracking/190926/20190926_161520655_10BEES_generated_20210928_090610_nn.csv", 10, is_first_run=a)
    #
    # ## 190927
    # #  ->  ->
    # analyse("../data/Video_tracking/190927/20190927_135709044_10BEES_generated_20211005_094101_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190927/20190927_103759768_10BEES_generated_20210929_104342_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 190928
    # #  ->  ->
    # analyse("../data/Video_tracking/190928/20190928_122031371_10BEES_generated_20211007_103125_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190928/20190928_161235208_10BEES_generated_20211008_102614_nn.csv", 10, is_first_run=a)
    #
    # ## 190929
    # #  ->  ->
    # analyse("../data/Video_tracking/190929/20190929_121957315_10BEES_generated_20211012_094335_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190929/20190929_155407984_10BEES_generated_20211015_094028_nn.csv", 10, is_first_run=a)
    #
    # ## 190930
    # #  ->  ->
    # analyse("../data/Video_tracking/190930/20190930_143111210_10BEES_generated_20211018_101123_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190930/20190930_110620060_10BEES_generated_20211019_095354_nn.csv", 10, is_first_run=a)
    #
    # ## 191001
    # #  ->  ->
    # analyse("../data/Video_tracking/191001/20191001_140821748_10BEES_generated_20211028_094845_nn.csv", 10, is_first_run=a)
    #
    # # 990 -> 825 -> 672 *
    # analyse("../data/Video_tracking/191001/20191001_112031240_10BEES_generated_20211026_092048_nn.csv", 10, is_first_run=a)
    #
    # ## 191002
    # #  ->  ->
    # analyse("../data/Video_tracking/191002/20191002_102112781_10BEES_generated_20211220_113720_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191002/20191002_133525621_10BEES_generated_20211222_080816_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # ## 191003
    # #  ->  ->
    # analyse("../data/Video_tracking/191003/20191003_125620288_10BEES_generated_20211222_105417_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191003/20191003_095527912_10BEES_generated_20211222_105139_nn.csv", 10, is_first_run=a)
    #
    # ## 191007
    # #  ->  ->
    # analyse("../data/Video_tracking/191007/20191007_141118287_10BEES_generated_20220104_105737_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191007/20191007_111802396_10BEES_generated_20220103_115134_nn.csv", 10, is_first_run=a)
    #
    # ## 191008
    # #  ->  ->
    # analyse("../data/Video_tracking/191008/20191008_161034917_10BEES_generated_20220107_084847_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191008/20191008_120529380_10BEES_generated_20220107_064857_nn.csv", 10, is_first_run=a)
    #
    # ## 191011
    # #  ->  ->
    # analyse("../data/Video_tracking/191011/20191011_145822566_10BEES_generated_20220107_102527_nn.csv", 10, is_first_run=a)
    #
    # ## 191014
    # #  ->  ->
    # analyse("../data/Video_tracking/191014/20191014_170158067_10BEES_generated_20220111_080114_nn.csv", 10, is_first_run=a)
    #
    # ## 191016
    # #  ->  ->
    # analyse("../data/Video_tracking/191016/20191016_132346782_10BEES_generated_20220118_100307_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191016/20191016_160838515_10BEES_generated_20220119_090556_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191016/20191016_123316519_10BEES_generated_20220113_125257_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191016/20191016_170332465_10BEES_generated_20220120_075126_nn.csv", 10, is_first_run=a)
    #
    # ## 191017
    # #  ->  ->
    # analyse("../data/Video_tracking/191017/20191017_132743751_10BEES_generated_20220121_115258_nn.csv", 10, has_tracked_video=True, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191017/20191017_125419660_10BEES_generated_20220121_113743_nn.csv", 10, is_first_run=a)
    #
    # ## 191018
    # #  ->  ->
    # analyse("../data/Video_tracking/191018/20191018_131957590_10BEES_generated_20220125_104309_nn.csv", 10, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191018/20191018_125650447_10BEES_generated_20220125_102149_nn.csv", 10, is_first_run=a)
    #
    # ############################################# 15 BEES #######################################################
    # ## 190822
    # #  ->  ->
    # analyse("../data/Video_tracking/190822/20190822_122407809_15BEE_generated_20210803_085008_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # ## 190823
    # #  ->  ->
    # analyse("../data/Video_tracking/190823/20190823_163934743_15BEES_generated_20210510_082044_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # ## 190903
    # #  ->  ->
    # analyse("../data/Video_tracking/190903/20190903_171612563_15BEES_generated_20210518_101121_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190903/20190903_132435095_15BEES_generated_20210511_063736_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # ## 190904
    # #  ->  ->
    # analyse("../data/Video_tracking/190904/20190904_164507538_15BEES_generated_20210525_103318_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190904/20190904_123252421_15BEES_generated_20210521_063745_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # ## 190905
    # #  ->  ->
    # analyse("../data/Video_tracking/190905/20190905_111848284_15BEES_generated_20210527_103530_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # ## 190906
    # #  ->  ->
    # analyse("../data/Video_tracking/190906/20190906_151436479_15BEES_generated_20210607_081516_nn.csv", 15, is_first_run=a)
    #
    # ## 190916
    # #  ->  ->
    # analyse("../data/Video_tracking/190916/20190916_155142744_15BEES_generated_20210611_105921_nn.csv", 15, is_first_run=a)
    #
    # ## 190917
    # #  ->  ->
    # analyse("../data/Video_tracking/190917/20190917_151102123_15BEES_generated_20210903_100118_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190917/20190917_104532152_15BEES_generated_20210803_082437_nn.csv", 15, is_first_run=a)
    #
    # ## 190918
    # #  ->  ->
    # analyse("../data/Video_tracking/190918/20190918_105639722_15BEES_generated_20210907_081259_nn.csv", 15, is_first_run=a)
    #
    # ## 190919
    # #  ->  ->
    # analyse("../data/Video_tracking/190919/20190919_105145877_15BEES_generated_20210908_083852_nn.csv", 15, is_first_run=a)
    #
    # ## 190920
    # #  ->  ->
    # analyse("../data/Video_tracking/190920/20190920_144702326_15BEES_generated_20210910_082748_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190920/20190920_110628291_15BEES_generated_20210909_095322_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # ## 190922
    # #  ->  ->
    # analyse("../data/Video_tracking/190922/20190922_154352238_15BEES_generated_20210913_095813_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190922/20190922_115427042_15BEES_generated_20210913_074557_nn.csv", 15, is_first_run=a)
    #
    # ## 190924
    # #  ->  ->
    # analyse("../data/Video_tracking/190924/20190924_105949133_15BEES_generated_20210916_083521_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190924/20190924_152226497_15BEES_generated_20210914_095925_nn.csv", 15, is_first_run=a)
    #
    # ## 190925
    # #  ->  ->
    # analyse("../data/Video_tracking/190925/20190925_142354429_15BEES_generated_20210924_084837_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190925/20190925_111416348_15BEES_generated_20210924_082629_nn.csv", 15, is_first_run=a)
    #
    # ## 190926
    # #  ->  ->
    # analyse("../data/Video_tracking/190926/20190926_162712758_15BEES_generated_20210928_090840_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190926/20190926_131641554_15BEES_generated_20210927_085812_nn.csv", 15, is_first_run=a)
    #
    # ## 190927
    # #  ->  ->
    # analyse("../data/Video_tracking/190927/20190927_105015136_15BEES_generated_20211001_084351_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190927/20190927_140903972_15BEES_generated_20211006_092141_nn.csv", 15, is_first_run=a)
    #
    # ## 190928
    # ## 190929
    # #  ->  ->
    # analyse("../data/Video_tracking/190929/20190929_160530530_15BEES_generated_20211015_094803_nn.csv", 15, is_first_run=a)
    #
    # ## 190930
    # #  ->  ->
    # analyse("../data/Video_tracking/190930/20190930_144234627_15BEES_generated_20211018_100830_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/190930/20190930_111749856_15BEES_generated_20211019_101232_nn.csv", 15, is_first_run=a)
    #
    # ## 191001
    # #  ->  ->
    # analyse("../data/Video_tracking/191001/20191001_141957735_15BEES_generated_20211028_095546_nn.csv", 15, has_tracked_video=True, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191001/20191001_113225056_15BEES_generated_20211026_092637_nn.csv", 15, is_first_run=a)
    #
    # ## 191002
    # ## 191003
    # #  ->  ->
    # analyse("../data/Video_tracking/191003/20191003_130715174_15BEES_generated_20220103_113351_nn.csv", 15, is_first_run=a)
    #
    # ## 191007
    # #  ->  ->
    # analyse("../data/Video_tracking/191007/20191007_142243717_15BEES_generated_20220105_085425_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191007/20191007_112941330_15BEES_generated_20220104_095854_nn.csv", 15, is_first_run=a)
    #
    # ## 191008
    # #  ->  ->
    # analyse("../data/Video_tracking/191008/20191008_110243113_15BEES_generated_20220105_103922_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191008/20191008_150528777_15BEES_generated_20220107_072438_nn.csv", 15, is_first_run=a)
    #
    # ## 191011
    # #  ->  ->
    # analyse("../data/Video_tracking/191011/20191011_134945372_15BEES_generated_20220107_091631_nn.csv", 15, is_first_run=a)
    #
    # ## 191014
    # #  ->  ->
    # analyse("../data/Video_tracking/191014/20191014_155509712_15BEES_generated_20220110_074244_nn.csv", 15, is_first_run=a)
    #
    # ## 191016
    # #  ->  ->
    # analyse("../data/Video_tracking/191016/20191016_162046345_15BEES_generated_20220119_095913_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191016/20191016_124613239_15BEES_generated_20220117_104800_nn.csv", 15, is_first_run=a)
    #
    # ## 191017
    # #  ->  ->
    # analyse("../data/Video_tracking/191017/20191017_130555083_15BEES_generated_20220121_114232_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191017/20191017_133858498_15BEES_generated_20220124_101400_nn.csv", 15, is_first_run=a)
    #
    # ## 191018
    # #  ->  ->
    # analyse("../data/Video_tracking/191018/20191018_133057695_15BEES_generated_20220126_102759_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191018/20191018_142523619_15BEES_generated_20220125_103406_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191018/20191018_143615609_15BEES_generated_20220126_104502_nn.csv", 15, is_first_run=a)
    #
    # #  ->  ->
    # analyse("../data/Video_tracking/191018/20191018_130828543_15BEES_generated_20220125_102542_nn.csv", 15, is_first_run=a)


if __name__ == "__main__":
    # align_first()
    run(is_first_run=True)
    # run_both()
    # run_just_annotate()
