from array import array
from unittest import TestCase
from collections import OrderedDict

from quicktable import Table, Column


class TestTable(TestCase):
    def setUp(self):
        self.table = Table(('Pokemon', str), ('Level', int), ('Type', str))

    def test_columns(self):
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

        self.assertEqual((self.table[0], self.table[1]), (
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

    def test_append_missing_values(self):
        with self.assertRaises(ValueError):
            self.table.append('This is not a Pokemon.')

    def test_append_wrong_type(self):
        with self.assertRaises(TypeError):
            self.table.append('Pikachu', 'Not a level', 'Electric')

    def test_append_wrong_type_cleanup(self):
        self.table.extend(('Charmander', 14, 'Fire'), ('Squirtle', 12, 'Water'))

        try:
            self.table.append('Pikachu', 'Not a level', 'Electric')
        except TypeError:
            pass

        values = list(self.table.columns.values())

        self.assertEqual(
            (values[0].values, values[1].values, values[2].values),
            (['Charmander', 'Squirtle'], array('i', [14, 12]), ['Fire', 'Water'])
        )

    def test_schema(self):
        self.assertEqual([('Pokemon', str), ('Level', int), ('Type', str)], self.table.schema)

    def test_equal_schema_match(self):
        table = Table(*self.table.schema)
        self.assertTrue(table == self.table)

    def test_equal_schema_mismatch(self):
        table = Table(('Pokemon', str))
        self.assertFalse(table == self.table)

    def test_equal_content_match(self):
        table = Table(*self.table.schema)
        table.extend(('Charmander', 14, 'Fire'), ('Pikachu', 20, 'Electric'))
        self.table.extend(('Charmander', 14, 'Fire'), ('Pikachu', 20, 'Electric'))

        self.assertTrue(table == self.table)

    def test_equal_content_mismatch(self):
        table = Table(*self.table.schema)
        table.extend(('Charmander', 14, 'Fire'), ('Pikachu', 20, 'Electric'))
        self.table.extend(('Charmander', 14, 'Fire'), ('Pikachu', 12, 'Electric'))

        self.assertFalse(table == self.table)

    def test_slice_stop(self):
        self.table.extend(
            ('Charmander', 14, 'Fire'),
            ('Squirtle', 12, 'Water'),
            ('Pikachu', 20, 'Electric'),
            ('Bulbasaur', 7, 'Grass')
        )

        expected = Table(*self.table.schema)
        expected.extend(('Charmander', 14, 'Fire'), ('Squirtle', 12, 'Water'))

        self.assertEqual(self.table[:2], expected)

    def test_slice_start(self):
        self.table.extend(
            ('Charmander', 14, 'Fire'),
            ('Squirtle', 12, 'Water'),
            ('Pikachu', 20, 'Electric'),
            ('Bulbasaur', 7, 'Grass')
        )

        expected = Table(*self.table.schema)
        expected.extend(('Squirtle', 12, 'Water'), ('Pikachu', 20, 'Electric'), ('Bulbasaur', 7, 'Grass'))

        self.assertEqual(self.table[1:], expected)

    def test_slice_step(self):
        self.table.extend(
            ('Charmander', 14, 'Fire'),
            ('Squirtle', 12, 'Water'),
            ('Pikachu', 20, 'Electric'),
            ('Bulbasaur', 7, 'Grass')
        )

        expected = Table(*self.table.schema)
        expected.extend(('Charmander', 14, 'Fire'), ('Pikachu', 20, 'Electric'))

        self.assertEqual(self.table[::2], expected)