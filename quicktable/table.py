from itertools import islice
from collections import OrderedDict


from quicktable import Column


class Table:
    def __init__(self, *schema):
        self.columns = OrderedDict((name, Column(kind)) for name, kind in schema)

    def append(self, *values):
        for value, column in zip(values, self.columns.values()):
            column.values.append(value)

    def __iter__(self):
        return zip(*self.columns.values())

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(islice(self, index.start, index.stop, index.step))

        return tuple(column[index] for column in self.columns.values())