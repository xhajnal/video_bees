from analyse import analyse


if __name__ == "__main__":
    ## SINGLE BEE xxxx22
    # already done
    # 1
    analyse('../data/Video_tracking/190822/20190822_111607344_1BEE_generated_20210430_080914_nn.csv', 1)
    # 156 -> 87 -> 11 -> 1
    analyse('../data/Video_tracking/190822/20190822_141925574_1bee_generated_20210504_081658_nn.csv', 1)

    ## xxxx23
    # hardcore, not merging traces
    # 15 -> 9 -> 1 done
    # 1 jump back and forth
    analyse('../data/Video_tracking/190823/20190823_114450691_1BEE_generated_20210506_100518_nn.csv', 1)
    # 6 -> 3 -> 1 done
    analyse('../data/Video_tracking/190823/20190823_153007029_1BEE_generated_20210507_091854_nn.csv', 1)

    ## TWO BEES xxxx22
    # 65 -> 56 -> 34
    # a lot of jump back and forth
    analyse('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', 2)
    # 79 -> 70 -> 28
    # 1 jump back and forth
    analyse('../data/Video_tracking/190822/20190822_143216366_2bees_generated_20210504_064410_nn.csv', 2)

    ## xxxx23
    # 171 -> 122 (outside arena) -> 66  -> 3
    # hardcore, a lot of discontinuous traces
    # some jump back and forth
    analyse('../data/Video_tracking/190823/20190823_115857275_2BEES_generated_20210507_083510_nn.csv', 2)
    # 55 -> 53 (outside arena) -> 46 -> 9
    # 4 jump back and forth
    analyse('../data/Video_tracking/190823/20190823_154249666_2BEES_generated_20210510_095112_nn.csv', 2)

    ## FIVE BEES xxxx22
    # 1416 -> 1091 -> 743
    # some jump back and forth
    analyse('../data/Video_tracking/190822/20190822_114441236_5BEE_generated_20210503_090128_nn.csv', 5)
    # 526 -> 415 -> 117
    # some jump back and forth
    analyse('../data/Video_tracking/190822/20190822_144547243_5BEE_generated_20210504_081238_nn.csv', 5)

    ## xxxx23
    # 987 -> 791 -> 50
    # a LOT jump back and forth
    analyse('../data/Video_tracking/190823/20190823_121326323_5BEES_generated_20210505_103301_nn.csv', 5)
    # 393 -> 279 -> 256
    # 1 jump back and forth
    analyse('../data/Video_tracking/190823/20190823_155506355_5BEES_generated_20210507_092606_nn.csv', 5)

    ## SEVEN BEES xxxx22
    # 701 -> 506 -> 192
    # some jump there and back
    analyse('../data/Video_tracking/190822/20190822_115819107_7BEE_generated_20210504_064122_nn.csv', 7)

    ## xxxx23
    # 477 -> 473 (outside arena) -> 372 -> 128
    # 3 jump there and back
    analyse('../data/Video_tracking/190823/20190823_124111790_7BEES_generated_20210507_070601_nn.csv', 7)
    # 895 -> 638 -> 188
    analyse('../data/Video_tracking/190823/20190823_161115188_7BEES_generated_20210507_093529_nn.csv', 7)

    ## TEN BEES xxxx22
    # 2126 -> 1551 ->
    # medium amount of jump there and back
    analyse('../data/Video_tracking/190822/20190822_121127355_10BEE_generated_20210430_102736_nn.csv', 10)
    # 1707 -> 1320 ->
    # some jump there and back
    analyse('../data/Video_tracking/190822/20190822_151158355_10BEE_generated_20210504_082545_nn.csv', 10)

    ## xxxx23
    # 2225 -> 1837 ->
    # medium amount jump there and back
    analyse('../data/Video_tracking/190823/20190823_162410226_10BEES_generated_20210510_080842_nn.csv', 10)

    ## FIFTEEN BEES xxxx22
    # 2174 -> 1764 ->
    # some jump there and back
    analyse('../data/Video_tracking/190822/20190822_122407809_15BEE_generated_20210803_085008_nn.csv', 15)

    ## xxxx23
    # 2190 -> 1938 ->
    # few jump there and back
    analyse('../data/Video_tracking/190823/20190823_163934743_15BEES_generated_20210510_082044_nn.csv', 15)
