"""
# base.py: Stuff I need Before Anything Else Can Work

"""
from __future__ import division,print_function
import sys,re,traceback,unittests,traceback
sys.dont_write_bytecode=True # don't write irritating .pyc files
from contextlib import contextmanager

"""___________________________________________________

## Generic container trick (fields, but no methods).
"""
def isa(x,y): return isinstance(x,y)

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

def kv(d, private="_"):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,The.misc.round) if isa(x,float) else x
  return '<'+', '.join(['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]) + '>'

