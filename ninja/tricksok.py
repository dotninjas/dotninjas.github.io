from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

from tricks import *

@ok
def _rand():
  """Seed control: the same 'random' nums will
     print after resetting the seed"""
  rseed(1)
  print(r3s([r() for _ in range(5)]))
  rseed(1)
  print(r3s([r() for _ in range(5)]))
  
@ok
def _kv():
  txt =str(o(a=1,b=2,c=3))
  print(txt=="['a: 1', 'b: 2', 'c: 3']",txt)

def _fail1():
  assert False,"assertion fail, but the tests continue"

@ok
def _fail():
  _fail1()

  
@ok
def _thing():
  x = thing('x11.1')
  print(x,isa(x,str))

oks()
