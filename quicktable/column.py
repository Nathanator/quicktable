from array import array


class Column:
    KIND_MAP = {
        str: list,
        int: lambda: array('i'),
    }

    def __init__(self, kind):
        self.kind = kind
        self.values = self.KIND_MAP[kind]()

    def __eq__(self, other):
        return self.kind == other.kind and self.values == other.values

    def __str__(self):
        return str(self[:5])

    def __repr__(self):
        return '<quicktable.Column ({0}) object at {1}>'.format(self.kind.__name__, hex(id(self)))

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, index):
        return self.values[index]