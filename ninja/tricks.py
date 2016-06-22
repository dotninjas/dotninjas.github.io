"""
# tricks.py  : Standard Python tricks

(C) 2016 tim@menzies.us, MIT license

___________________________________________________

## Header tricks

"""
from __future__ import division,print_function
import sys,random,re,copy,os,inspect,traceback
sys.dont_write_bytecode=True # don't write irritating .pyc files

"""___________________________________________________

## Generic container trick (fields, but no methods).
"""

class o:
  def __init__(i, **adds): i.__dict__.update(adds)
  def __repr__(i)        : return str(kv(i.__dict__))

"""___________________________________________________

## Meta tricks (one day, this will make sense)
"""

def same(z): return z

def ok(*lst):
  for one in lst: unittest(one)
  return one

def oks():
  print(unittest.score())

class unittest:
  tries = fails = 0  #  tracks the record so far
  @staticmethod
  def score():
    t = unittest.tries
    f = unittest.fails
    return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
      t,f,int(round(t*100/(t+f+0.001))))
  def __init__(i,test):
    unittest.tries += 1
    try:
      print("\n-----| %s |-----------------------" % test.__name__)
      if test.__doc__:
         print("# "+ re.sub(r'\n[ \t]*',"\n# ",test.__doc__)+"\n")
      test()
    except Exception,e:
      unittest.fails += 1
      print(traceback.format_exc())
      print(unittest.score(),':',test.__name__)

"""___________________________________________________

## Options trick
"""

# 'The' is the place to hold global options

# 'The' is the place to hold global options

The=Then=o(tricks=o(round=2))

def then():
  Then = copy.deepcopy(The)

def now():
  The = copy.deepcopy(Then)
  
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

def r2(f)    : return round(f, 2)
def r3(f)    : return round(f, 3)
def r4(f)    : return round(f, 4)

def r2s(lst) : return map(r2,lst)
def r3s(lst) : return map(r3,lst)
def r4s(lst) : return map(r4,lst)

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


