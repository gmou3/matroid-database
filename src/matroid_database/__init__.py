r"""
Python interface to matroid database.

Tests::

>>> from matroid_database import *

>>> for m in all_matroids_revlex(2, 1):
...     print(m)
**
0*

>>> for m in all_matroids_bases(2, 1):
...     print(m)
[(0,), (1,)]
[(1,)]

>>> for m in all_matroids_revlex(2, 2):
...     print(m)
*

>>> for m in all_matroids_bases(2, 2):
...     print(m)
[(0, 1)]

>>> for m in all_matroids_revlex(5, 2):
...     print(m)
**********
0*********
0****0****
00*0**0***
000*******
000******0
0000**0***
0000**0**0
00000*00**
000000****
0000000***
00000000**
000000000*

>>> list(all_matroids_revlex(10, 5))
Traceback (most recent call last):
...
ValueError: unable to open .../allr5n10.txt.xz
Available (n, r):
all: (<=12, 1-2), (<=11, 3), (<=9, 4)
unorientable: (7-11, 3), (7-9, 4)

>>> [sum(1 for m in all_matroids_revlex(n, 1)) for n in range(1, 13)]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
>>> [sum(1 for m in all_matroids_bases(n, 1)) for n in range(1, 13)]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

>>> [sum(1 for m in all_matroids_revlex(n, 2)) for n in range(2, 13)]
[1, 3, 7, 13, 23, 37, 58, 87, 128, 183, 259]
>>> [sum(1 for m in all_matroids_bases(n, 2)) for n in range(2, 13)]
[1, 3, 7, 13, 23, 37, 58, 87, 128, 183, 259]

>>> [sum(1 for m in all_matroids_revlex(n, 3)) for n in range(3, 12)]
[1, 4, 13, 38, 108, 325, 1275, 10037, 298491]
>>> [sum(1 for m in all_matroids_bases(n, 3)) for n in range(3, 12)]
[1, 4, 13, 38, 108, 325, 1275, 10037, 298491]

>>> [sum(1 for m in all_matroids_revlex(n, 4)) for n in range(4, 10)]
[1, 5, 23, 108, 940, 190214]
>>> [sum(1 for m in all_matroids_bases(n, 4)) for n in range(4, 10)]
[1, 5, 23, 108, 940, 190214]

>>> [sum(1 for m in unorientable_matroids_revlex(n, 3)) for n in range(7, 12)]
[1, 3, 18, 201, 9413]
>>> [sum(1 for m in unorientable_matroids_bases(n, 3)) for n in range(7, 12)]
[1, 3, 18, 201, 9413]

>>> [sum(1 for m in unorientable_matroids_revlex(n, 4)) for n in range(7, 10)]
[1, 34, 12284]
>>> [sum(1 for m in unorientable_matroids_bases(n, 4)) for n in range(7, 10)]
[1, 34, 12284]
"""


def _open_data(module, name):
    import lzma
    from importlib.resources import files

    path = files(module).joinpath(name + '.txt.xz')
    try:
        return lzma.open(path.open('rb'), 'rt')
    except FileNotFoundError:
        raise ValueError(
            "unable to open %s" % path +
            "\nAvailable (n, r):" +
            "\nall: (<=12, 1-2), (<=11, 3), (<=9, 4)" +
            "\nunorientable: (7-11, 3), (7-9, 4)"
        )


def all_matroids_revlex(n, r):
    """
    Return an iterator over the revlex encodings of all matroids of given
    number of elements and rank.
    """
    with _open_data(__package__, f"_all/allr{r}n{n:02d}") as f:
        while s := f.readline():
            yield s.strip()


def unorientable_matroids_revlex(n, r):
    """
    Return an iterator over the revlex encodings of unorientable matroids of
    given number of elements and rank.
    """
    type = "unorientable"
    with _open_data(__package__, f"_{type}/{type}r{r}n{n:02d}") as f:
        while s := f.readline():
            yield s.strip()


def all_matroids_bases(n, r):
    """
    Return an iterator over the lists of bases of all matroids of given number
    of elements and rank.
    """
    from itertools import combinations

    def revlex_sort_key(s):
        return tuple(reversed(s))

    subsets = sorted(combinations(range(n), r), key=revlex_sort_key)

    for revlex in all_matroids_revlex(n, r):
        B = [s for s, c in zip(subsets, revlex) if c == '*']
        yield B


def unorientable_matroids_bases(n, r):
    """
    Return an iterator over the lists of bases of unorientable matroids of
    given number of elements and rank.
    """
    from itertools import combinations

    def revlex_sort_key(s):
        return tuple(reversed(s))

    subsets = sorted(combinations(range(n), r), key=revlex_sort_key)

    for revlex in unorientable_matroids_revlex(n, r):
        B = [s for s, c in zip(subsets, revlex) if c == '*']
        yield B
