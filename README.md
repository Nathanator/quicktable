quicktable
==========

quicktable is a Pythonic representation of tabular data. quicktable is designed to have no dependencies on external
modules, be beautifully represented in code and require very little learning to use.

quicktables can be filtered, unioned, pivoted and its columns can be transformed, removed, extended and renamed among
other operations. Read the full documentation to see what quicktables are capable of.

Installation
------------

`pip install quicktable`

Quick Reference
---------------

Using quicktable is very simple; in the below example we initialise a table with a schema, add some data to it and
finally print it out.

```python
>>> from quicktable import Table
>>> table = Table(('Name', str), ('Age', int))
>>> table.append('Ash', 10)
>>> table.append('Misty', 12)
>>> print(table)
| Name  | (int) Age |
| Ash   | 10        |
| Misty | 12        |
```

quicktable columns can be extended statically or dynamically:

```python
>>> table = table.extend('Profession', str, 'Trainer')
>>> table = table.extend('YearsToAdult', int, lambda row: 18 - row.Age)
>>> print(table)
| Name  | (int) Age | Profession | (int) YearsToAdult |
| Ash   | 10        | Trainer    | 8                  |
| Misty | 12        | Trainer    | 6                  |
```

quicktables can be easily filtered

```python
>>> table = table.filter(lambda row: row.Name == 'Ash')
>>> print(table)
| Name  | (int) Age | Profession | (int) YearsToAdult |
| Ash   | 10        | Trainer    | 8                  |
```