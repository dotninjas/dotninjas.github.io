from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from logs import *

@ok
def _sample():
  rseed(1)
  print(The.logs.few)
  s = Sample(list('i have gone to seek a great perhaps'),few=8)
  assert s.some == [' ', ' ', 'n', 'p', 'v', 'e', 'r', 'p']

@ok
def _sym():
  print(Sym(list('i have gone to seek a great perhaps')))

@ok
def _col():
  rseed(1)
  n= Num( [ 600 , 470 , 170 , 430 , 300])
  print(n,n.sd())
  assert 164.711 <= n.sd() <= 164.712
  assert n.lo == 170
  assert n.up == 600

@ok
def _log():
  l = Log()
  for x in ["?","?", 600 , 470 , 170 , 430 , 300]:
    l += x
  assert 164.711 <= l.thing.sd() <= 164.712
  assert l.thing.lo == 170
  assert l.thing.up == 600

@ok
def _tub():
  rseed(1)
  l = Logs()
  for _ in xrange(10):
    l += ["thing"] + [r()**(0.1*n) for n in xrange(4)]
  print([x.thing for x in l.cols.values()])
  
oks()
