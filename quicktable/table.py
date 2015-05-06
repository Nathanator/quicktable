from itertools import islice
from collections import OrderedDict, namedtuple

from quicktable import Column


class Table:
    def __init__(self, *schema):
        self.columns = OrderedDict((name, Column(kind)) for name, kind in schema)
        self.row_tuple = namedtuple('Row', self.columns.keys())

    def append(self, *values):
        """Append the values as a new row to the table."""
        for value, column in zip(values, self.columns.values()):
            column.values.append(value)

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
            return list(islice(self, index.start, index.stop, index.step))

        return self.row_tuple(*[column[index] for column in self.columns.values()])

    def __len__(self):
        return len(next(iter(self.columns.values())).values)

    def __str__(self):
        return '<quicktable.Table object at {0}>'.format(hex(id(self)))

    def __repr__(self):
        return str(self)