# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from unittest import TestCase
import operator
from itertools import islice, cycle
from functools import partial
from streams import Stream


class UnitTests(TestCase):

    def test_stream_creation(self):
        """
        Basic Stream creation works as expected.
        """
        self.assertListEqual(
            Stream([1,2,3,4]).to_list(),
            [1, 2, 3, 4]
        )

        self.assertListEqual(
            Stream([1,2,3,4], [5,6,7,8,9]).to_list(),
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        )

    def test_stream_from_iter(self):
        """
        Stream creation works with iterators.
        """
        self.assertListEqual(
            Stream(iter(range(10))).to_list(),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        )

        self.assertListEqual(
            Stream(iter(range(10)), iter(range(5))).to_list(),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
        )

    def test_all_match(self):
        """
        Stream.all_match returns True, if all elements in the stream match the
        predicate, False otherwise
        """
        self.assertTrue(Stream(range(10)).all_match(partial(operator.gt, 10)))
        self.assertFalse(Stream(range(10)).all_match(partial(operator.gt, 5)))

    def test_any_match(self):
        """
        Stream.any_match returns True, if any element in the stream matches the
        predicate, False otherwise
        """
        self.assertTrue(Stream(range(10)).all_match(partial(operator.gt, 10)))
        self.assertFalse(Stream(range(10)).all_match(partial(operator.lt, 10)))

    def test_average(self):
        """
        Stream.average returns the numeric average of the stream.
        """
        self.assertEqual(Stream([0, 2, 7]).average(), 3.0)
        self.assertEqual(Stream([0, 0, 5, 5]).average(), 2.5)

    def test_count(self):
        """
        Stream.count returns the number of elements in the stream.
        """
        def gen():
            for x in []:
                yield x

        self.assertEqual(Stream([]).count(), 0)
        self.assertEqual(Stream(iter([])).count(), 0)
        self.assertEqual(Stream(gen()).count(), 0)
        self.assertEqual(Stream(range(0)).count(), 0)

        self.assertEqual(Stream(range(10)).count(), 10)

    def test_distinct(self):
        """
        Stream.distinct returns a new stream with distinct items from
        original stream.
        """
        self.assertListEqual(
            Stream(list(range(5)) * 2).distinct().to_list(),
            [0, 1, 2, 3, 4]
        )

        self.assertListEqual(
            Stream(islice(cycle('ABC'), 10)).distinct().to_list(),
            ['A', 'B', 'C']
        )

        objs = [object(), object()] * 5
        self.assertListEqual(
            Stream(objs).distinct().to_list(),
            objs[:2]
        )

    def test_enumerate(self):
        """
        Stream.enumerate returns a tuple stream of (n, i) tuples in the
        same fashion as builtin.enumerate.
        """
        l = [5, 6, 7, 8, 9]
        self.assertListEqual(
            Stream(l).enumerate().to_list(),
            list(enumerate(l))
        )

        self.assertListEqual(
            Stream(l).enumerate(1).to_list(),
            list(enumerate(l, 1))
        )

        self.assertListEqual(
            Stream(l).enumerate(-10).to_list(),
            list(enumerate(l, -10))
        )
