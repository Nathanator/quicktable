from unittest import TestCase
from collections import OrderedDict

from quicktable import Table, Column


class TestTable(TestCase):
    def setUp(self):
        self.table = Table(('Pokemon', str), ('Level', int), ('Type', str))

    def test_schema(self):
        expected = OrderedDict()
        expected['Pokemon'] = Column(str)
        expected['Level'] = Column(int)
        expected['Type'] = Column(str)

        self.assertEqual(self.table.columns, expected)

    def test_row_tuple(self):
        expected = ('Pokemon', 'Level', 'Type')
        self.assertEqual(expected, self.table.row_tuple._fields)

    def test_append(self):
        self.table.append('Pikachu', 20, 'Electric')
        self.assertEqual(self.table[0], self.table.row_tuple(Pokemon='Pikachu', Level=20, Type='Electric'))

    def test_append_multiple(self):
        self.table.append('Charmander', 14, 'Fire')
        self.table.append('Squirtle', 12, 'Water')

        self.assertEqual(
            (self.table[0], self.table[1]), (
                self.table.row_tuple(Pokemon='Charmander', Level=14, Type='Fire'),
                self.table.row_tuple(Pokemon='Squirtle', Level=12, Type='Water'),
            )
        )

    def test_extend(self):
        self.table.extend(('Charmander', 14, 'Fire'), ('Squirtle', 12, 'Water'))

        self.assertEqual(
            (self.table[0], self.table[1]), (
                self.table.row_tuple(Pokemon='Charmander', Level=14, Type='Fire'),
                self.table.row_tuple(Pokemon='Squirtle', Level=12, Type='Water'),
            )
        )
