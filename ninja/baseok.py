import sys
sys.dont_write_bytecode=True # don't write irritating .pyc files

from base import *



print(22)
o1 = o(n=0.11111111111)
assert str(o1) == "<n: 0.1111>"
with options() as old:
  old .misc.round = 2
  assert str(o1) == '<n: 0.11>'
print(str(o1))
assert str(o1) == "<n: 0.1111>"
print("!",The.misc.round)
oks()
