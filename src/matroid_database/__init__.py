r"""
Python interface to matroid database.

Tests::

>>> from matroid_database import *

>>> for m in all_matroids_revlex(0, 0):
...     print(m)
*

>>> for m in all_matroids_bases(0, 0):
...     print(m)
[()]

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
ValueError: unable to open .../n10r05.txt(.xz)
Available (n, r):
all: (<=9, *), (10, *-5), (11, <=3|>=8), (12, <=3|>=10)
unorientable: (7-11, 3), (7-9, 4)

>>> all_matroids_expected = [
...     [1, 1, 1, 1, 1,  1,  1,   1,   1,      1,     1,      1,        1,],
...     [   1, 2, 3, 4,  5,  6,   7,   8,      9,    10,     11,       12,],
...     [      1, 3, 7, 13, 23,  37,  58,     87,   128,    183,      259,],
...     [         1, 4, 13, 38, 108, 325,   1275, 10037, 298491, 31899134,],
...     [            1,  5, 23, 108, 940, 190214,                         ],
...     [                1,  6,  37, 325, 190214,                         ],
...     [                    1,   7,  58,   1275,                         ],
...     [                         1,   8,     87, 10037,                  ],
...     [                              1,      9,   128, 298491,          ],
...     [                                      1,    10,    183,          ],
...     [                                             1,     11,      259,],
...     [                                                     1,       12,],
...     [                                                               1,],
... ]
>>> for r, counts in enumerate(all_matroids_expected):
...     for n in range(r, r + len(counts)):
...         expected = counts[n - r]
...         assert sum(1 for m in all_matroids_revlex(n, r)) == expected
...         if expected < 10**6:
...             assert sum(1 for m in all_matroids_bases(n, r)) == expected

>>> unorientable_matroids_tests = [
...     (range(7, 12), 3, [1,  3,    18, 201, 9413,]),
...     (range(7, 10), 4, [1, 34, 12284,           ]),
... ]
>>> for n_range, r, counts in unorientable_matroids_tests:
...     for n in n_range:
...         expected = counts[n - n_range.start]
...         assert sum(1 for m in unorientable_matroids_revlex(n, r)) == expected
...         assert sum(1 for m in unorientable_matroids_bases(n, r)) == expected
"""


def _open_data(module, name):
    import lzma
    from importlib.resources import files

    # Open 'txt' file
    path = files(module).joinpath(name + '.txt')
    try:
        return path.open('r')
    except FileNotFoundError:
        pass

    # Fall back to compressed '.txt.xz' file
    path = files(module).joinpath(name + '.txt.xz')
    try:
        return lzma.open(path.open('rb'), 'rt')
    except FileNotFoundError:
        raise ValueError(
            "unable to open %s" % name + '.txt(.xz)' +
            "\nAvailable (n, r):" +
            "\nall: (<=9, *), (10, *-5), (11, <=3|>=8), (12, <=3|>=10)" +
            "\nunorientable: (7-11, 3), (7-9, 4)"
        )


def all_matroids_revlex(n, r):
    """
    Return an iterator over the revlex encodings of all matroids of given
    number of elements and rank.
    """
    with _open_data(__package__, f"_all/n{n:02d}r{r:02d}") as f:
        while s := f.readline():
            yield s.strip()


def unorientable_matroids_revlex(n, r):
    """
    Return an iterator over the revlex encodings of unorientable matroids of
    given number of elements and rank.
    """
    with _open_data(__package__, f"_unorientable/n{n:02d}r{r:02d}") as f:
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
