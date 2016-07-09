# Lib.py
# Holds standard tools.

# ___________________________________________________
# Standard headers

from __future__ import division,print_function
import sys,random,re,copy
sys.dont_write_bytecode=True # don't write irritating .pyc files

# ___________________________________________________
# Generic container (fields, but no methods).

class o:
  def __init__(i, **entries): i.__dict__.update(entries)
  def __repr__(i):  return str(kv(i.__dict__))

  # ___________________________________________________
# 'The' is the place to hold global options

The=o()

# ___________________________________________________
# Standard alias tricks

rseed=random.seed
r=random.random
copy=copy.deepcopy

# ___________________________________________________
# Dictionary tricks

def kv(d, private="_", places=4):
  "Print dicts, keys sorted (ignoring 'private' keys"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,places) if isa(x,float) else x
  return ['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]

# ___________________________________________________
# Printing tricks

def dot(x='.'):
  "Write without new line"
  sys.stdout.write(x)
  sys.stdout.flush()

# ___________________________________________________
# Type tricks

def isa(x,y): return isinstance(x,y)
def isSym(x): return isa(x,str)

def thing(x):
  "Coerce to a float or an int or a string"
  try: return int(x)
  except ValueError:
    try: return float(x)
    except ValueError:
      return x

# __________________________________________________
# Maths tricks

def normalDiff(mu1,sd1,n1,mu2,sd2,n2): 
    delta = mu2 - mu1
    if s1+s2:
      delta =  delta/((sd1/n1 + sd2/n2)**0.5)
    return delta

def lstDiff(lst1,lst2):
 """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    tmp1 = tmp2 = 0
    n1,n2 = len(lst1), len(lst2)
    mu1   = sum(lst1) / n1
    mu2   = sum(lst2) / n2
    tmp1  = sum( (y1 - mu1)**2 for y1 in lst1 )
    tmp2  = sum( (y2 - mu2)**2 for y2 in lst2 )
    sd1   = ( tmp1 / (n1 - 1) )**0.5
    sd2   = ( tmp2 / (n2 - 1) )**0.5
    return normalDiff(mu1,sd1,n1,mu2,sd2,n2)
  
# ___________________________________________________
# Meta tricks (one day, this will make sense)

def same(z): return z

