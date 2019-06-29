import unittest

from etl import data_processing


class TestDataProcessing(unittest.TestCase):
    def test_string_grouping(self):
        input = "abcdefghj"
        expected = ["a b c".split(" "),
                    "d e f".split(" "),
                    "g h j".split(" ")
                    ]
        actual = data_processing.grouper(input, 3)

        for e, a in zip(expected, actual):
            self.assertEqual(len(e), len(a))
            for i, j in zip(e, a):
                self.assertEqual(i, j)

    def test_list_input(self):
        input = range(100)
        n = 10
        actual = data_processing.grouper(input, n)

        for a in actual:
            self.assertEqual(len(a), n)

    def test_filling_exhaused_source(self):
        input = range(7)
        n = 5

        actual = list(data_processing.grouper(input, n, fillvalue=0))
        expected = [list(range(5)), [5, 6, 0, 0, 0]]
        for e, a in zip(expected, actual):
            self.assertEqual(e, list(a))





