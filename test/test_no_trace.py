import unittest
from misc import *

class MyTestCase(unittest.TestCase):
    ## NO TRACE TESTS
    def test_misc(self):
        self.assertEqual(get_last_digit(5), 5)
        self.assertEqual(get_last_digit(61), 1)
        self.assertEqual(get_last_digit(848745), 5)

        self.assertEqual(calculate_cosine_similarity([1, 0], [0, 1]), 0)
        self.assertNotAlmostEqual(calculate_cosine_similarity([1, 0], [1, 1]), 0.707)
        self.assertEqual(calculate_cosine_similarity([1, 1], [1, 1]), 1)
        self.assertEqual(calculate_cosine_similarity([2, 2], [3, 3]), 1)

        self.assertEqual(to_vect([5], [3]), [-2])
        self.assertEqual(to_vect([8, 5], [7, 3]), [-1, -2])
        self.assertEqual(to_vect([5, 8, 5], [10, 7, 3]), [5, -1, -2])

        self.assertEqual(nice_range_print([605, 610]), "605-10")
        self.assertEqual(nice_range_print([605, 710]), "605 - 710")
        self.assertEqual(nice_range_print([605, 1710]), "605 - 1710")
        self.assertEqual(nice_range_print([605, 1610]), "605 - 1610")

        self.assertEqual(delete_indices([], [8, 9]), [8, 9])
        self.assertEqual(delete_indices([0], [8, 9]), [9])
        self.assertEqual(delete_indices([1], [8, 9]), [8])
        self.assertEqual(delete_indices([0, 1], [8, 9]), [])
        self.assertEqual(delete_indices([0, 1], [8, 9, 10]), [10])
        self.assertEqual(delete_indices([1], [8, 9, 10]), [8, 10])
        self.assertEqual(delete_indices([1, 1], [8, 9, 10]), [8, 10])


        self.assertEqual(take(0, [8, 9, 10]), [])
        self.assertEqual(take(1, [8, 9, 10]), [8])
        self.assertEqual(take(2, [8, 9, 10]), [8, 9])
        self.assertEqual(take(3, [8, 9, 10]), [8, 9, 10])

        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([8]), (8,))
        self.assertEqual(flatten((8, 7)), (8, 7))
        self.assertEqual(flatten(((8, 7))), (8, 7))
        self.assertEqual(flatten(((8, 7))), (8, 7))
        self.assertEqual(flatten(((8, (7)))), (8, 7))
        self.assertEqual(flatten(((8, (7, 9)))), (8, 7, 9))
        self.assertEqual(flatten(((8, 9, (7)))), (8, 9, 7))

        self.assertEqual(range_len((7, 7)), 0)
        self.assertEqual(range_len((7, 8)), 1)
        self.assertEqual(range_len((0, 10)), 10)
        self.assertEqual(range_len((1, 11)), 10)

        self.assertEqual(margin_range((7, 7), 0), (7, 7))
        self.assertEqual(margin_range((5, 6), 0), (5, 6))
        self.assertEqual(margin_range((5, 6), 1), (4, 7))
        self.assertEqual(margin_range((5, 6), 4), (1, 10))

        self.assertTrue(is_in([1, 7], [8, 9]) is False)
        self.assertTrue(is_in([1, 7], [7, 9]) is False)
        self.assertTrue(is_in([8, 9], [1, 7]) is False)
        self.assertTrue(is_in([7, 9], [1, 7]) is False)
        self.assertTrue(is_in([1, 7], [2, 6]) is False)
        self.assertTrue(is_in([4, 6], [3, 9]) is True)
        self.assertTrue(is_in([1, 7], [2, 7]) is False)
        self.assertTrue(is_in([3, 6], [3, 9]) is True)
        self.assertTrue(is_in([1, 7], [1, 7]) is True)

        self.assertTrue(has_overlap([1, 7], [8, 9]) is False)
        self.assertTrue(has_overlap([1, 7], [7, 9]) is True)
        self.assertTrue(has_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(has_overlap([7, 9], [1, 7]) is True)
        self.assertTrue(has_overlap([1, 7], [2, 6]) is True)
        self.assertTrue(has_overlap([4, 6], [3, 9]) is True)
        self.assertTrue(has_overlap([1, 7], [2, 7]) is True)
        self.assertTrue(has_overlap([3, 6], [3, 9]) is True)
        self.assertTrue(has_overlap([1, 7], [1, 7]) is True)
        self.assertTrue(has_overlap([1620, 1625], [1620, 1620]) is True)

        self.assertTrue(has_strict_overlap([1, 7], [8, 9]) is False)
        self.assertTrue(has_strict_overlap([5, 6], [6, 10]) is False)
        self.assertTrue(has_strict_overlap([1, 7], [7, 9]) is False)
        self.assertTrue(has_strict_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(has_strict_overlap([7, 9], [1, 7]) is False)
        self.assertTrue(has_strict_overlap([1, 7], [2, 6]) is True)
        self.assertTrue(has_strict_overlap([4, 6], [3, 9]) is True)
        self.assertTrue(has_strict_overlap([1, 7], [2, 7]) is True)
        self.assertTrue(has_strict_overlap([3, 6], [3, 9]) is True)
        self.assertTrue(has_strict_overlap([1, 7], [1, 7]) is True)
        self.assertTrue(has_strict_overlap([1620, 1625], [1620, 1620]) is False)

        self.assertTrue(get_overlap([1, 7], [8, 9]) is False)
        self.assertEqual(get_overlap([1, 7], [7, 9]), [7, 7])
        self.assertTrue(get_overlap([8, 9], [1, 7]) is False)
        self.assertEqual(get_overlap([7, 9], [1, 7]), [7, 7])
        self.assertEqual(get_overlap([1, 7], [2, 6]), [2, 6])
        self.assertEqual(get_overlap([4, 6], [3, 9]), [4, 6])
        self.assertEqual(get_overlap([1, 7], [2, 7]), [2, 7])
        self.assertEqual(get_overlap([3, 6], [3, 9]), [3, 6])
        self.assertEqual(get_overlap([1, 7], [1, 7]), [1, 7])

        self.assertEqual(get_gap([1, 7], [8, 9]), [7, 8])
        self.assertEqual(get_gap([1, 7], [7, 9]), [7, 7])
        self.assertEqual(get_gap([8, 9], [1, 7]), [7, 8])
        self.assertEqual(get_gap([7, 9], [1, 7]), [7, 7])
        self.assertEqual(get_gap([1, 7], [2, 6]), False)
        self.assertEqual(get_gap([4, 6], [3, 9]), False)
        self.assertEqual(get_gap([1, 7], [2, 7]), False)
        self.assertEqual(get_gap([3, 6], [3, 9]), False)
        self.assertEqual(get_gap([1, 7], [1, 7]), False)

        self.assertEqual(get_strict_gap([1, 7], [8, 9]), [7, 8])
        self.assertEqual(get_strict_gap([1, 7], [7, 9]), False)
        self.assertEqual(get_strict_gap([8, 9], [1, 7]), [7, 8])
        self.assertEqual(get_strict_gap([7, 9], [1, 7]), False)
        self.assertEqual(get_strict_gap([1, 7], [2, 6]), False)
        self.assertEqual(get_strict_gap([4, 6], [3, 9]), False)
        self.assertEqual(get_strict_gap([1, 7], [2, 7]), False)
        self.assertEqual(get_strict_gap([3, 6], [3, 9]), False)
        self.assertEqual(get_strict_gap([1, 7], [1, 7]), False)

        self.assertTrue(get_strict_overlap([1, 7], [8, 9]) is False)
        self.assertTrue(get_strict_overlap([1, 7], [7, 9]) is False)
        self.assertTrue(get_strict_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(get_strict_overlap([7, 9], [1, 7]) is False)
        self.assertEqual(get_strict_overlap([1, 7], [2, 6]), [2, 6])
        self.assertEqual(get_strict_overlap([4, 6], [3, 9]), [4, 6])
        self.assertEqual(get_strict_overlap([1, 7], [2, 7]), [2, 7])
        self.assertEqual(get_strict_overlap([3, 6], [3, 9]), [3, 6])
        self.assertEqual(get_strict_overlap([1, 7], [1, 7]), [1, 7])

        self.assertTrue(is_before([1, 7], [8, 9]) is True)
        self.assertTrue(is_before([1, 7], [7, 9]) is False)
        self.assertTrue(is_before([8, 9], [1, 7]) is False)
        self.assertTrue(is_before([7, 9], [1, 7]) is False)
        self.assertTrue(is_before([1, 7], [2, 6]) is False)
        self.assertTrue(is_before([4, 6], [3, 9]) is False)
        self.assertTrue(is_before([1, 7], [2, 7]) is False)
        self.assertTrue(is_before([3, 6], [3, 9]) is False)
        self.assertTrue(is_before([1, 7], [1, 7]) is False)

        self.assertEqual(get_index_of_shortest_range([]), -1)
        self.assertEqual(get_index_of_shortest_range([(1, 1)]), 0)
        self.assertTrue(get_index_of_shortest_range([(1, 1), (2, 2)]) == (0, 1))
        self.assertEqual(get_index_of_shortest_range([(1, 1), (2, 3)]), 0)
        self.assertEqual(get_index_of_shortest_range([(1, 1), (2, 3), (2, 2)]), (0, 2))
        self.assertEqual(get_index_of_shortest_range([(1, 5), (2, 3), (2, 2)]), 2)

        self.assertEqual(merge_dictionary({8: 1}, {9: 9}), {8: 1, 9: 9})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {9: 9}), {7: 1, 8: 1, 9: 9})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {7: 9}), {7: 10, 8: 1})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {8: 9}), {7: 1, 8: 10})

        # strictly further
        self.assertEqual(merge_sorted_dictionaries({(6, 7): 1}, {(8, 9): 6}), {(6, 7): 1, (8, 9): 6})
        self.assertEqual(merge_sorted_dictionaries({(8, 9): 6}, {(6, 7): 1}), {(6, 7): 1, (8, 9): 6})
        self.assertEqual(merge_sorted_dictionaries({(8, 9): 6, (6, 7): 1}, {}), {(6, 7): 1, (8, 9): 6})
        self.assertEqual(merge_sorted_dictionaries({}, {(8, 9): 6, (6, 7): 1}), {(6, 7): 1, (8, 9): 6})
        # more left
        self.assertEqual(merge_sorted_dictionaries({(8, 7): 1}, {(9, 7): 9}), {(8, 7): 1, (9, 7): 9})
        self.assertEqual(merge_sorted_dictionaries({(9, 7): 9}, {(8, 7): 1}), {(8, 7): 1, (9, 7): 9})
        self.assertEqual(merge_sorted_dictionaries({(9, 7): 9, (8, 7): 1}, {}), {(8, 7): 1, (9, 7): 9})
        # more up
        self.assertEqual(merge_sorted_dictionaries({(8, 7): 1}, {(8, 8): 9}), {(8, 7): 1, (8, 8): 9})
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9}, {(8, 7): 1}), {(8, 7): 1, (8, 8): 9})
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9, (8, 7): 1}, {}), {(8, 7): 1, (8, 8): 9})
        #
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9, (10, 11): 0}, {(8, 7): 1}), {(8, 7): 1, (8, 8): 9, (10, 11): 0})
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9, (10, 11): 0}, {(8, 7): 1, (15, 16): 7}), {(8, 7): 1, (8, 8): 9, (10, 11): 0, (15, 16): 7})

        self.assertEqual(get_leftmost_point([[0, 0]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 2]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 2], [4, 5]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[1, 2], [4, 5], [0, 0]]), ([0, 0], 2))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 0]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 0], [4, 0]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[1, 0], [4, 0], [0, 0]]), ([0, 0], 2))

        # m = 2
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [[41621, 41663], [41688, 41699]], strict=True), {})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [[41621, 41663], [41688, 41699]]), {})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)], strict=True), {(0, 2): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(9, 11), (6, 8), (7, 10)], strict=True), {(1, 2): [7, 8], (0, 2): [9, 10]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (7, 10), (9, 11)], strict=True), {(0, 1): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(7, 10), (6, 8), (9, 11)], strict=True), {(0, 1): [7, 8], (0, 2): [9, 10]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)], strict=True, skip_whole_in=True), {(0, 2): [7, 8], (1, 2): [9, 10]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 10), (7, 10)], strict=True, skip_whole_in=True), {(0, 2): [7, 8]})

        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]),
                                       [[None, False, list([7, 8])],
                                        [0, None, list([9, 10])],
                                        [0, 0, None]]))
        self.assertEqual(m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]), {(0, 2): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]), {})

        # m = 3
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)], strict=True), {})
        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]),
                                       [[[None, None, None], [9, None, False], [9, 9, None]],
                                        [[9, 9, 9], [9, None, None], [9, 9, None]],
                                        [[9, 9, 9], [9, 9, 9], [9, 9, None]]]))

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)], strict=True), {})
        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]),
                                       [[[None, None, None], [9, None, list([9, 10])], [9, 9, None]],
                                        [[9, 9, 9], [9, None, None], [9, 9, None]],
                                        [[9, 9, 9], [9, 9, 9], [9, 9, None]]]))

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)], strict=True), {(0, 1, 2): [9, 10]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]), {(0, 1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (6, 10), (3, 7)], strict=True),
                         {(0, 1, 2): [9, 10], (0, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (6, 10), (3, 7)]), {(0, 1, 2): [9, 10], (0, 2, 3): [6, 7]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (9, 11)], strict=True, skip_whole_in=True), {})


        # m = 4
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (9, 11), (6, 10), (3, 7)], strict=True), {})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (9, 11), (6, 10), (3, 7)]), {})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7)], strict=True), {(0, 1, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7)]), {(0, 1, 2, 3): [6, 7]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7), (5, 6)], strict=True, skip_whole_in=True),
                         {(0, 1, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7), (5, 6)], strict=True), {(0, 1, 2, 3): [6, 7]})

        # self.assertTrue(np.array_equal(get_submatrix(np.arange(10)*2, [1]), 2))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[1, 2, 3], [4, 5, 6]]), [1]), [4, 5, 6]))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[1, 2, 3], [4, 5, 6]]), [1, 2]), 6))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]), [1, 1]), [10, 11, 12]))

        self.assertEqual(convert_frame_number_back(1620, '../test/test_converted.csv'), 1621)

if __name__ == '__main__':
    unittest.main()