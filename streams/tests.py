# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from unittest import TestCase


class UnitTests(TestCase):

    def test_stream_creation(self):
        """
        >>> import streams
        >>> streams.Stream([1,2,3,4]).to_list()
        [1, 2, 3, 4]
        >>> streams.Stream([1,2,3,4], [5,6,7,8,9]).to_list()
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
