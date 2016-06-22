"""
# base.py: Stuff I need Before Anything Else Can Work

"""
from __future__ import division,print_function
import sys,re,traceback
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

The=o()

def then():
  Then = copy.deepcopy(The)

def now():
  The = copy.deepcopy(Then)
