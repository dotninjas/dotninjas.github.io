import sys
sys.dont_write_bytecode=True # don't write irritating .pyc files

from base import *



def _baseok():
  print(22)
  o1 = o(n=0.11111111111)
  assert str(o1) == "<n: 0.1111>"
  with options():
     The.misc.round = 2
     assert str(o1) == '<n: 0.11>'
  print(str(o1))
  assert str(o1) == "<n: 0.1111>"


_baseok()
_baseok()

oks()
