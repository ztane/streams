# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from unittest import TestCase


class UnitTests(TestCase):

    def test_stream_creation(self):
        """
        Basic Stream creation works as expected.
        """
        from streams import Stream

        self.assertListEqual(
            Stream([1,2,3,4]).to_list(),
            [1, 2, 3, 4]
        )

        self.assertListEqual(
            Stream([1,2,3,4], [5,6,7,8,9]).to_list(),
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        )

    def test_stream_from_gen(self):
        """
        Stream creation works with generators.
        """
        from streams import Stream

        self.assertListEqual(
            Stream(iter(range(10))).to_list(),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        )

        self.assertListEqual(
            Stream(iter(range(10)), iter(range(5))).to_list(),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
        )
