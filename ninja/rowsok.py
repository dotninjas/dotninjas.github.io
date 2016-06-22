from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from rows import *

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
  "Handle one list of numbers"
  l = Log()
  for x in ["?","?", 600 , 470 , 170 , 430 , 300]:
    l += x
  assert 164.711 <= l.about.sd() <= 164.712
  assert l.about.lo == 170
  assert l.about.up == 600

@ok
def _logs():
  "Handle 10 lists, each of which contains 1 word and 4 numbers"
  rseed(1)
  l = Logs()
  for _ in xrange(10):
    l += ["word"] + [r()**(0.1*n) for n in xrange(4)]
  print([x.about for x in l.cols.values()])
  
oks()
