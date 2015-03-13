from __future__ import division
from itertools import islice, chain, starmap

try:
    from future_builtins import filter, map
except:
    if isinstance(filter(True, []), list):
        from itertools import ifilter as filter, imap as map

EMPTY = object()

class Stream(object):
    def __init__(self, *iterables):
        if len(iterables) == 1:
            self._iterable = iterables[0]
        else:
            self._iterable = chain.from_iterable(iterables)

    @classmethod
    def _make_stream(cls, iterable):
        return cls(iterable)

    def all_match(self, predicate):
        """
        Returns True if all elements in the stream match the
        predicate, False otherwise
        """
        return all(predicate(i) for i in self._iterable)

    def any_match(self, predicate):
        """
        Returns True if any element in the stream matches the
        predicate, False otherwise
        """
        return any(predicate(i) for i in self._iterable)

    def none_match(self, predicate):
        """
        Returns True if no elements in the stream match the
        predicate, False otherwise
        """
        return not any(predicate(i) for i in self._iterable)

    def apply_to(self, func):
        """
        Calls the given function with the stream as the parameter;
        that is apply_to(list) is the same as list(stream).
        """
        return func(self._iterable)

    def average(self):
        """
        Returns the numeric average of this stream
        """

        the_sum = 0
        number = 0
        for i in self._iterable:
            the_sum += i
            number += 1

        return the_sum / number

    def collect(self, supplier, accumulator, combiner):
        raise NotImplementedError

    def count(self):
        """
        Return the number of the elements in this stream
        """

        return sum(1 for i in self._iterable)

    def distinct(self):
        """
        Return a stream with distinct elements from this stream.
        The elements must be hashable.
        """

        def gen():
            seen = set()
            for e in self._iterable:
                if e not in seen:
                    seen.add(e)
                    yield e

        return self._make_stream(gen())

    def enumerate(self, start=0):
        return self._make_stream(enumerate(self._iterable, start))

    @classmethod
    def empty(cls):
        return cls([])

    def filter(self, predicate):
        return self._make_stream(filter(predicate, self._iterable))

    def find_any(self):
        return next(self._iterable, EMPTY)

    def find_first(self):
        return next(self._iterable, EMPTY)

    def flat_map(self, *a, **kw):
        raise NotImplementedError

    def for_each(self, action):
        return self.for_each_ordered(action)

    def for_each_ordered(self, action):
        for i in self._iterable:
            action(i)

    @classmethod
    def generate(cls, supplier):
        def gen():
            while 1:
                yield supplier()

        return cls._make_stream(gen())

    def __getitem__(self, item):
        if isinstance(item, slice):
            rv_gen = islice(self._iterable, item.start, item.stop, item.step)
            return self._make_stream(rv_gen)

        else:
            raise IndexError("Streams only support slicing, not element indexing")

    def __iter__(self):
        return iter(self._iterable)

    def limit(self, n):
        return self._make_stream(islice(self._iterable, n))

    # PY2 compat
    def next(self):
        return self.__next__()

    def __next__(self):
        return next(self._iterable)

    def map(self, mapper, *others):
        return self._make_stream(map(mapper, self._iterable, *others))

    def max(self, key=None):
        if key == None:
            return max(self._iterable)

        return max(self._iterable, key=key)

    def min(self, key=None):
        if key == None:
            return min(self._iterable)

        return min(self._iterable, key=key)

    @classmethod
    def of(cls, *values):
        return cls._make_stream(values)

    def parallel(self):
        return self

    def peek(self, action):
        def gen():
            for i in self._iterable:
                action(i)
                yield i

        return self._make_stream(gen())

    def sequential(self):
        return self

    def skip(self, n):
        """
        Skips ``n`` elements from this stream and return a stream
        of the rest.
        """
        return self._make_stream(islice(self._iterable, n, None))

    def sorted(self, key=None, reverse=False):
        """
        Return a new stream with sorted elements.
        """
        new_data = sorted(self._iterable, key=key, reverse=reverse)
        return self._make_stream(new_data)

    def starmap(self, mapper):
        """
        Maps the iterable arguments from the stream through the func as::

            new_e = func(*old_e)

        """
        return self._make_stream(starmap(mapper, self._iterable))

    def starapply_to(self, func):
        """
        Calls the given function with the unpacked stream as parameters;
        that is starapply_to(func) is the same as func(*stream).
        """
        return func(*self._iterable)

    def streammap(self, func):
        """
        Map each iterable element through the function as a stream
        """

        def wrapper(value):
            return func(self._make_stream(value))

        return self.map(wrapper)

    def sum(self):
        return sum(self._iterable)

    def to_list(self):
        return list(self._iterable)
