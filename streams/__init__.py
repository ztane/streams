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
        Returns true if the `predicate(i)` does not yield 
        a true value for any item in the stream

        This is a terminal operator
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
        """
        Returns a slice of this stream, as a stream
        """
        if isinstance(item, slice):
            rv_gen = islice(self._iterable, item.start, item.stop, item.step)
            return self._make_stream(rv_gen)

        else:
            raise IndexError("Streams only support slicing, not element indexing")

    def __iter__(self):
        """
        Returns an iterator for the contents of this stream
        """
        return iter(self._iterable)

    def limit(self, n):
        """
        Returns a stream that will contain up to n elements of this stream.
        """
        return self._make_stream(islice(self._iterable, n))

    # PY2 compat
    def next(self):
        """
        Yields the next element from this stream
        """
        return self.__next__()

    def __next__(self):
        """
        Yields the next element from this stream
        """
        return next(self._iterable)

    def map(self, mapper, *others):
        """
        Returns a new stream that consists of the elements of
        this stream mapped through the given mapping function.

        This is a terminal operation
        """
        return self._make_stream(map(mapper, self._iterable, *others))

    def max(self, key=None):
        """
        Returns the maximum value in this stream, optionally
        sorted by the given key function.
        """
        if key == None:
            return max(self._iterable)

        return max(self._iterable, key=key)

    def min(self, key=None):
        """
        Returns the minimum value in this stream, optionally
        sorted by the given key function.

        This is a terminal operation
        """
        if key == None:
            return min(self._iterable)

    @classmethod
    def of(self, *values):
        """
        Returns a new stream whose elements are the star arguments
        given to this function.

        Stream.of(1, 2, 3) returns a stream that yields 1, 2 and 3.
        """

        return self._make_stream(values)

    def parallel(self):
        """
        Return a possibly parallelized version of this stream.
        A parallel stream is unordered; the order of elements is
        not specified at the terminal operation.
        """

        return self

    def peek(self, action):
        """
        Invoke action(e) for each element that passes through the
        stream at this point.
        """
        def gen():
            for i in self._iterable:
                action(i)
                yield i

        return self._make_stream(gen())

    def sequential(self):
        """
        Convert the stream into a sequential stream
        """
        return self

    def skip(self, n):
        """
        Skips ``n`` elements from this stream and return a stream
        of the rest.
        """
        return self._make_stream(islice(self._iterable, n, None))

    def sorted(self, key=None, reverse=False):
        """
        Sort the elements, as if by builtin `sorted`; return a new
        sequential stream whose elements are in the given sorted order.
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
        Map each iterable element through the function, and return
        a stream of streams.
        """
        def wrapper(value):
            return func(self._make_stream(value))

        return self.map(wrapper)

    def sum(self):
        """
        Returns the sum of this stream. The elements must be summable
        together.
        """
        return sum(self._iterable)

    def to_list(self):
        return list(self._iterable)
