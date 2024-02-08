Python interface to matroid database
====================================

This database was retrieved from
<https://www-imai.is.s.u-tokyo.ac.jp/~ymatsu/matroid/index.html>
(Yoshitake Matsumoto, *Database of Matroids*, 2012; accessed: 2023.12.02).

Usage:

  >>> from matroid_database import all_matroids_revlex
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

  >>> from matroid_database import unorientable_matroids_revlex
  >>> for m in unorientable_matroids_revlex(8, 3):
  ...     print(m)
  0******0******0**********0********0*******0****0**0*****
  0******0******0***0******0*0**0*************************
  0000************0**********0****0**********0**0***0*****

  >>> from matroid_database import all_matroids_bases
  >>> for m in all_matroids_bases(4, 2):
  ...     print(m)
  [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]
  [(0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]
  [(0, 2), (1, 2), (0, 3), (1, 3)]
  [(1, 2), (1, 3), (2, 3)]
  [(0, 3), (1, 3), (2, 3)]
  [(1, 3), (2, 3)]
  [(2, 3)]
