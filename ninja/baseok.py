import sys
sys.dont_write_bytecode=True # don't write irritating .pyc files

from base import *

@ok
def _baseok():
  x= o(n=0.11111111111)
  assert str(x) == "<n: 0.1111>"
  with options():
     The.misc.round = 2
     assert str(x) == '<n: 0.11>'
  assert str(x) == "<n: 0.1111>"
  
oks()
   
