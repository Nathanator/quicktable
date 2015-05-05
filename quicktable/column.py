class Column:
    def __init__(self, kind):
        self.kind = kind
        self.values = []

    def __str__(self):
        return '<quicktable.Column ({0}) object at {1}>'.format(self.kind.__name__, hex(id(self)))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, index):
        return self.values[index]