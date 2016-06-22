"""
# base.py: Stuff I need Before Anything Else Can Work

"""
from __future__ import division,print_function
import sys,re,traceback,copy
sys.dont_write_bytecode=True # don't write irritating .pyc files
from contextlib import contextmanager

"""___________________________________________________

## Generic container trick (fields, but no methods).
"""

class o:
  def __init__(i, **adds): i.__dict__.update(adds)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __repr__(i)        : return kv(i.__dict__)

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

# 'The' is the place to hold global options. `the


The = o(misc=o(round=4))

def isa(x,y): return isinstance(x,y)

def kv(d, private="_",
       places=None):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  places = The.misc.round if places is None else 4
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,places) if isa(x,float) else x
  return '<'+', '.join(['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]) + '>'

@contextmanager
def options():
  "Allow for temporary change the options, which can be reversed."
  global The
  safe = o()
  for k,v in The.__dict__.items():
    safe[k]= o(**{k2:v2 for k2,v2 in v.__dict__.items()})
  yield
  print(1,The,safe)
  The = safe
  print(2,The,safe)
