#!/usr/bin/python
from __future__ import division,print_function
import sys,re,random,argparse
sys.dont_write_bytecode=True

ABOUT=[
  "sway: Data mining+optimization",
  "(C) 2016, tim@menzies.us MIT,v2",
  ("--seed",   61409389,   int,   "int", "random number seed"),
  ("--samples",     256,   int,   "int", "keep at most, say, 256 samples"),
  ("--cdomBigger", 0.01, float, "float", "continous domination bigger; e.g. 1.01"),
  ("--kind",      "Row",   str,   "str", "kind of model class for each Row"),
  ("--swayBigger", 1.01, float, "float", "SWAY projections bigger; e.g. 1.01"),
  ("--swayCull",    0.5,   int, "float", "SWAY's smallest population size; e.g. 0.5"),
  ("--swayStop",     20,   int,   "int", "SWAY's smallest size, leaf clusters; e.g. 20")
] 

def cmdline(lst):
  parser = argparse.ArgumentParser(prog=lst[0], description= lst[1])
  for (key, d, t, m,h,) in lst[2:]:
    parser.add_argument(key,default=d,type=t,metavar=m,help=h)
  return parser.parse_args()

THE = cmdline(ABOUT)

"""
Warning: no normalization on objectives. eval
functions need to be well-behaved i.e. ideally 0..1
but realistically, not deliver numbers that are
orders of magnitude different
"""

def same(x)  : return x
def less(x,y): return x < y
def more(x,y): return x > y
def max(x,y) : return x if x>y else y
def min(x,y) : return x if x<y else y
def any(lst) : return random.choose(list)
def rseed(s) : random.seed(s or THE.seed)

def atom(x):
  try: return float(x),Num
  except ValueError: return x,Sym
  
class Row(object):
  rid = 0
  def __init__(i,lst):
    i.contents=lst
    i.rid = Row.rid = Row.rid+1
  def __repr__(i)       : return '#%s,%s' % (i.rid,i.contents)
  def __getitem__(i,k)  : return i.contents[k]
  def __setitem__(i,k,v): i.contents[k] = v


#---------    
 
class Model(Row):
  def __init__(i.lst):
    super(Model, i).__init__(lst)
    i.labelled=False
  def label(i,tbl,cost=1):
     """Row labels are cached back into the row. So labelling
        N times only incur a single labelling cost."""
    if not i.labelled:
      i.label1()
      tbl.cost += cost
      for col in tbl.dep:
        col.add( i[col.pos] ) # and remember the new values
      i.labelled = True
    return i
  def label1(i):
    "Rewritten by subclass"
    return i
  
class Summary: pass

class Num(Summary):
  def __init__(i):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
  def add(i,x):
    x = float(x)
    if x > i.up: i.up=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    return x
  def sub(i,x):
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  def norm(i,x):
    tmp= (x - i.lo) / (i.hi - i.lo + 10**-32)
    return min(1, max(0,tmp))
  def dist(i,x,y):
    return i.norm(x) - i.norm(y)
  def furthest(i,x) :
    return i.up if x <(i.up-i.lo)/2 else i.lo

class Sym(Summary):
  def __init__(i) :
     i.counts, i.most, i.mode, i.n = {},0,None,0
  def add(i,x):
    i.n += 1
    new = i.counts[x] = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new,x
    return x
  def sub(i,x):
    i.n -= 1
    i.counts[x] -= 1
    if x == i.mode:
      i.most, i.mode = None,None
  def norm(i,x)   : return x
  def dist(i,x,y) : return 0 if x==y else 1
  def furthest(i,x): return "SoMEcrazyTHing"
  def k(i):
    return len(i.counts.keys())
  def ent(i):
    """Measures how many symbols are mixed up together.  If only one symbol, then
       ent=0 (nothing mixed up)."""
    tmp = 0
    for val in i.counts.values():
      p = val/i.n
      if p:
        tmp -= p*math.log(p,2)
    return tmp

class Thing(Summary):
  "some thing that can handle  Nums or Syms"
  UNKNOWN = "?"
  def __init__(i, pos, txt):
    i.txt, i.pos, i.details, i.samples = txt, pos, None, Sample()
  def add(i,x):
    if x != Thing.UNKNOWN:
      if i.details is None:
        x,what  = atom(x)
        i.details = what()
      x = i.details.add(x)
      i.samples.add(x)
    return x

class Sample:
  def __init__(i, init=[]):
    i.n, i.some, i.ordered = 0, [], False
    map(i.add,init)
  def add(i,x):
    i.ordered = False
    i.n += 1
    now  = len(i.some)
    if now < THE.samples:
      i.some += [x]
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
  
class Table:
  KINDS = {'Row':Row,'Model':Model}
  LOVE  = ">"
  HATE  = "<"
  KLASS = "="
  SKIP  = "-"
  def __init__(i):
    i.rows = []
    i.cost = 0
    i.cols,  i.objs, i.decs = [], [], []
    i.klass, i.gets, i.dep  = [], [], []
  def cloned(i):
    yield [col.txt for cols in i.cols]
    for row in i.rows:
      yield row.contents
  def __call__(i,row):
    if i.cols:
      kind    = Table.kinds[THE.kind]
      row     = [i.cols[put].add(row[get]) for put,get in enumerate(i.gets)])
      i.rows += [ kind(row) ]
    else:
      for get,cell in enumerate(row):
        if cell[0] != Table.SKIP:
          i.gets += [get]
          col     = Thing( len(i.cols) , cell)    
          i.cols += [col]
          if   cell[0] == Table.LOVE  : i.objs  += [(col,more)]
          elif cell[0] == Table.HATE  : i.objs  += [(col,less)]
          elif cell[0] == Table.KLASS : i.klass += [col]
          else                        : i.decs  += [col]
          #---------------------------------------
          for col,_ in i.objs  : i.dep   += [col]
          for col   in i.klass : i.dep   += [col]
  def distance(i,r1,r2,f=2):
    inc,n = 0, 10**-32
    for col in i.decs:
      n    += 1
      x, y  = r1[col.pos], r2[col.pos]
      inc  += col.details.dist(x,y)**f
    return inc**f/n**f
  def label1(data,row):
    return row # usually rewritten by subclass

def bdom(x, y, tbl):
  x= label(tbl, x)
  y= label(tbl, y)
  betters = 0
  for col,better in tbl.objs:
    x1,y1 = x[col.pos], y[col.pos]
    if better(x1,y1) : betters += 1
    elif x1 != y1    : return False # must be worse, go quit
  return betters > 0

def cdom(x, y, tbl, ee= 2.718281828459):
  x= label(tbl, x)
  y= label(tbl, y)
  def w(better):
    return -1 if better == less else 1
  def expLoss(w,x1,y1,n):
    return -1*ee**( w*(x1 - y1) / n )
  def loss(x, y):
    losses= []
    n = min(len(x),len(y))
    for col,better in tbl.objs:
      x1 = x[col.pos] 
      y1 = y[col.pos] 
      loss += exploss( w(better),x1,y1,n)
    return sum(losses) / n
  l1= loss(x,y)
  l2= loss(y,x)
  return l1 < l2 if abs(l1 - l2)/l1 >= THE.cdomBigger else False

def sway( population, tbl, better= bdom) :
   def cluster(items, out):
    if len(items) < stop: 
      out.append(items) 
    else:
      west, east, wests, easts = split(items, int(len(items)/2)) 
    if not better(west,east,tbl): cluster( easts, out )  
    if not better(east,west,tbl): cluster( wests, out )
    return out
 
  def split(items, mid,west=None,east=None):
    cosine = lambda a,b,c: ( a*a + c*c - b*b )/( 2*c+ 0.0001 )
    west   = west or any(items)
    east   = east or any(items)
    while east.rid  == west.rid:
      east = any(items)
    c = tbl.distance(west, east)
    xs = {}
    for item in items:
       a = tbl.distance(item, west)
       b = tbl.distance(item, east)
       x = xs[ item.rid ] = cosine(a,b,c) # cosine rule
       if a > c * THE.swayBigger:
         redo += 1
         return split(items, mid, item, east)
       if b > c * THE.swayBigger:
         redo += 1
         return split(items, mid, west, item)   
    redo  = 0
    items = sorted(items, key= lambda item: xs[ item.rid ]) # sorted by 'x'
    return west, east, items[:mid], items[mid:]
  # --------
  stop= max(len(population)**THE.swayCull, THE.swayStop)
  return cluster(population, []),redo

def file2table(file):
  tbl= Table()
  src = open(file) if file else  sys.stdin
  for line in src:
    row = map(lambda z:z.strip(),
              line.split(","))
    if len(row)> 1:
      tbl(row)
  return tbl

def _demo1():
  tbl = file2table()
  for row in tbl.rows:
    print("")
    #print(row)
    cl = tbl.closest(row)
    far= tbl.furthest(row)
    print(tbl.distance(row,cl))
    print(tbl.distance(row,far))
  for pos,row1 in enumerate(tbl.rows):
    for  row2 in tbl.rows[pos:]:
      print(bdom(row1,row2,tbl))
    

#        def furthest(i,r1, better= more, init= 0):
#    most,out = init, None
#    for r2 in i.rows:
#      if id(r1) != id(r2):
#        tmp = i.distance(r1,r2)
#        if better(tmp, most):
#          most,out = tmp,r2
#    return out
#  def closest(i,r1):
#    return i.furthest(r1, better= less, init= 10**32)
