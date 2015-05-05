from itertools import islice
from collections import OrderedDict, namedtuple

from quicktable import Column


class Table:
    def __init__(self, *schema):
        self.columns = OrderedDict((name, Column(kind)) for name, kind in schema)
        self.row_tuple = namedtuple('Row', self.columns.keys())

    def append(self, *values):
        for value, column in zip(values, self.columns.values()):
            column.values.append(value)

    def __iter__(self):
        return iter(map(lambda row: self.row_tuple(*row), zip(*self.columns.values())))

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(islice(self, index.start, index.stop, index.step))

        return self.row_tuple(*[column[index] for column in self.columns.values()])