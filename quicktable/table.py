from itertools import islice, takewhile
from collections import OrderedDict, namedtuple

from quicktable import Column


class Table:
    def __init__(self, *schema):
        self.columns = OrderedDict((name, Column(kind)) for name, kind in schema)
        self.row_tuple = namedtuple('Row', self.columns.keys())

    @property
    def schema(self):
        return [(name, column.kind) for name, column in self.columns.items()]

    def append(self, *values):
        """Append the values as a new row to the table."""
        if len(values) != len(self.columns):
            raise ValueError('Must supply the same number of values as there are columns.')

        try:
            for value, column in zip(values, self.columns.values()):
                column.values.append(value)
        except TypeError:
            # If an invalid type was appended to an array, pop the other new column values before failing.
            previous_length = len(list(self.columns.values())[-1].values)

            for column in takewhile(lambda col: len(col.values) > previous_length, self.columns.values()):
                column.values.pop()

            raise

    def extend(self, *rows):
        for row in rows:
            self.append(*row)

    def filter(self, function):
        return filter(function, self)

    @staticmethod
    def _map_unpack(function, iterable):
        """Unpack each element of iterable into map."""
        return map(lambda element: function(*element), iterable)

    def __iter__(self):
        return iter(self._map_unpack(self.row_tuple, zip(*self.columns.values())))

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step

            start = start or 0
            stop = stop or len(self)
            step = step or 1
            if stop > len(self):
                stop = len(self)  # or stop is very big on Python 2.7 and throws MemoryError

            table = Table(*self.schema)
            table.extend(*[self[i] for i in range(start, stop, step)])
            return table

        return self.row_tuple(*[column[index] for column in self.columns.values()])

    def __len__(self):
        return len(next(iter(self.columns.values())).values)

    def __eq__(self, other):
        if not self.schema == other.schema:
            return False

        return all(this_row == other_row for this_row, other_row in zip(self, other))

    def __str__(self):
        return '<quicktable.Table object at {0}>'.format(hex(id(self)))

    def __repr__(self):
        return str(self)