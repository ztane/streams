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
        predicate, False otherwise.
        """
        self.assertTrue(Stream(range(10)).all_match(partial(operator.gt, 10)))
        self.assertFalse(Stream(range(10)).all_match(partial(operator.gt, 5)))

    def test_any_match(self):
        """
        Stream.any_match returns True, if any element in the stream matches the
        predicate, False otherwise.
        """
        self.assertTrue(Stream(range(10)).any_match(partial(operator.gt, 10)))
        self.assertTrue(Stream(range(10)).any_match(partial(operator.eq, 9)))
        self.assertFalse(Stream(range(10)).any_match(partial(operator.eq, 10)))

    def test_none_match(self):
        """
        Stream.none_match returns True, if no elements in the stream match the
        predicate, False otherwise.
        """
        self.assertTrue(Stream(range(10)).none_match(partial(operator.lt, 10)))
        self.assertFalse(Stream(range(10)).none_match(partial(operator.gt, 10)))

    def test_apply_to(self):
        """
        Stream.apply_to applies the given function to the iterable and returns
        the result.
        """
        iterable = object()
        unit = lambda x: x
        self.assertIs(
            Stream(iterable).apply_to(unit),
            iterable
        )

        self.assertEqual(Stream(range(10)).apply_to(sum), sum(range(10)))

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

    def test_empty(self):
        """
        Stream.empty creates an empty stream.
        """
        self.assertListEqual(Stream.empty().to_list(), [])

    def test_filter(self):
        """
        Stream.filter returns only elements matching predicate.
        """
        self.assertListEqual(
            Stream(range(10)).filter(partial(operator.gt, 10)).to_list(),
            list(range(10))
        )
        self.assertListEqual(
            Stream(range(10)).filter(partial(operator.gt, 5)).to_list(),
            list(range(5))
        )

    def test_for_each(self):
        """
        Stream.for_each calls given action for each item.
        """
        l = list(range(10))
        Stream(l[:]).for_each(lambda x: self.assertEqual(x, l.pop(0)))

    def test_generate(self):
        """
        Stream.generate calls given supplier repeatedly providing items
        (potentially indefinitely).
        """
        supplier = lambda i=iter(range(10)): next(i)
        self.assertListEqual(
            Stream.generate(supplier).to_list(),
            list(range(10))
        )

        sentinel = object()
        supplier = lambda: sentinel
        self.assertListEqual(
            Stream.generate(supplier)[:10].to_list(),
            [sentinel] * 10
        )

    def test_getitem(self):
        """
        Streams support slicing, but not indexing.
        """
        self.assertListEqual(
            Stream(range(100))[:10].to_list(),
            list(range(10))
        )

        try:
            Stream(range(100))[10]

        except IndexError:
            pass

        else:
            self.fail("Indexing streams should raise IndexError")

    def test_iter(self):
        """
        Stream supports iterator methods ``__iter__`` and ``__next__``
        (``next`` for PY2 people).
        """
        l = list(range(10))
        for x in Stream(l[:]):
            self.assertEqual(x, l.pop(0))

        self.assertListEqual(
            list(Stream(range(10))),
            list(range(10))
        )

        s = Stream(iter(range(10)))
        for x in range(10):
            self.assertEqual(x, next(s))

    def test_map(self):
        """
        Stream.map maps mapper over iterables.
        """
        self.assertListEqual(
            Stream(range(10)).map(lambda x: x + 1).to_list(),
            list(range(1, 11))
        )

    def test_max(self):
        """
        Stream.max returns the maximum value of iterable, optionally
        according to ``key``.
        """
        self.assertEqual(Stream(range(10)).max(), 9)
        self.assertTupleEqual(
            Stream(zip(range(9, -1, -1), range(10, 20))).max(
                key=operator.itemgetter(1)
            ),
            (0, 19)
        )

    def test_min(self):
        """
        Stream.min returns the minimum value of iterable, optionally
        according to ``key``.
        """
        self.assertEqual(Stream(range(10)).min(), 0)
        self.assertTupleEqual(
            Stream(zip(range(9, -1, -1), range(10, 20))).min(
                key=operator.itemgetter(1)
            ),
            (9, 10)
        )
