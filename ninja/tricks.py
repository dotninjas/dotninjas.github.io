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

"""___________________________________________________

##  Dictionary tricks
"""

def kv(d, private="_",
       places=The.tricks.round):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,places) if isa(x,float) else x
  return ['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]

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

def isa(x,y): return isinstance(x,y)
def isSym(x): return isa(x,str)

def thing(x):
  "Coerce to a float or an int or a string"
  try: return int(x)
  except ValueError:
    try: return float(x)
    except ValueError:
      return x


