from src.parse import parse_traces, Trace

with open('../test/test.csv', newline='') as csvfile:
    traces = parse_traces(csvfile)
    # print()
    print(traces[0])
    spam0 = Trace(traces[0], 0)
    assert spam0.frame_range == (1620, 1622)
    assert spam0.number_of_frames == 3
    assert spam0.frame_range_len == 2
    assert spam0.trace_lenn == 4.242640687119286
    assert spam0.max_step_len == 2.8284271247461903
    assert spam0.max_step_len_step_index == 1
    assert spam0.max_step_len_line == 5
    assert spam0.max_step_len_frame_number == 1621

    spam1 = Trace(traces[1], 1)
    assert spam1.frame_range == (1620, 1622)
    assert spam1.number_of_frames == 3
    assert spam1.frame_range_len == 2
    assert spam1.trace_lenn == 7.621232784634294
    assert spam1.max_step_len == 5.385164807134505
    assert spam1.max_step_len_step_index == 0
    assert spam1.max_step_len_line == 3
    assert spam1.max_step_len_frame_number == 1620

    spam0.show_step_lenghts_hist()