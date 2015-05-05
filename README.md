quicktable
==========

quicktable is a Pythonic representation of tabular data. quicktable is designed to have no dependancies on external
modules, be beautifully represented in code and require very little learning to use.

Quick Reference
---------------

Using quicktable is very simple; in the below example initialise a table with a schema, add some data to it and finally
print it out.

```python
>>> from quicktable import Table, Schema
>>> schema = Schema(['Name', 'Age'], [str, int])
>>> table = Table(schema)
>>> table.append('Ash', 10)
>>> table.append('Misty', 12)
>>> print(table)
| Name  | (int) Age |
| Ash   | 10        |
| Misty | 12        |
```

You can add new columns to an existing column statically or dynamically:

```python
>>> table.extend('Profession', str, 'Trainer')
>>> table.extend('YearsToAdult', int, lambda row: 18 - row.Age)
>>> print(table)
| Name  | (int) Age | Profession | (int) YearsToAdult |
| Ash   | 10        | Trainer    | 8                  |
| Misty | 12        | Trainer    | 6                  |
```