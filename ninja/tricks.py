"""
# tricks.py  : Standard Python tricks

(C) 2016 tim@menzies.us, MIT license

___________________________________________________

## Header tricks
"""
from __future__ import division,print_function
import sys,random,re,copy,os
sys.dont_write_bytecode=True # don't write irritating .pyc files

from base import *
"""

## Optioins for Tricks

"""


The.tricks = o(round=3)

"""___________________________________________________
 
## Standard alias tricks
"""

rseed=random.seed
r=random.random
copy=copy.deepcopy

"""__________________________________________________

## Stabndard maths tricks

"""

def less(x,y) : return x < y
def more(x,y) : return x > y


"""__________________________________________________

## Stabndard lst tricks

"""

def first(x)  : return x[0]
def second(x) : return x[1]
def last(x)   : return x[-1]

"""___________________________________________________

## Printing tricks
"""

def dot(x='.'):
  "Write without new line"
  sys.stdout.write(x)
  sys.stdout.flush()

def ro(f)     : return round(f, The.tricks.round)
def ro2(f)    : return round(f, 2)
def ro3(f)    : return round(f, 3)
def ro(f)     : return round(f, 4)

def ros(lst)  : return map(ro,lst)
def ros2(lst) : return map(r2,lst)
def ros3(lst) : return map(r3,lst)
def ros4(lst) : return map(r4,lst)

"""___________________________________________________

## Type tricks
"""

def isSym(x): return isa(x,str)

def atom(x):
  "Coerce to a float or an int or a string"
  try: return int(x)
  except ValueError:
    try: return float(x)
    except ValueError:
      return x


"""___________________________________________________

## Cache tricks
"""

def cached(x,y,cache,f):
  if id(x) > id(y):
    x,y = y,x
  key = (id(x),id(y))
  if key in cache:
    return cache[key]
  else:
    new = cache[key] = f(x,y)
    return new

"""__________________________________________________

### Command line tricks

"""

def args(*lst):
  import argparse
  parser = argparse.ArgumentParser(
    description=lst[0])
  p  = parser.add_argument
  for arg,types,default,meta,help in lst[1:]:
    parser.add_argument(arg,
                        type=types,
                        default=default,
                        metavar=meta,
                        help=help)
  return parser.parse_args()

def twiddle():
  chars = '|/-\\'
  for c in chars + chars + chars:
    sys.stdout.write(c)
    sys.stdout.write('\b')
    sys.stdout.flush()
