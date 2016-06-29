from __future__ import division,print_function
import sys,re,random
sys.dont_write_bytecode=True

"""
Warning: no normalization on objectives. eval
functions need to be well-behaved i.e. ideally 0..1
but realistically, not deliver numbers that are
orders of magnitude different
"""

UNKNOWN="?"
LOVE=">"
HATE="<"
KLASS="="

def less(x,y): return x < y
def more(x,y): return x > y
def max(x,y) : return x if x>y else y
def min(x,y) : return x if x<y else y

def atom(x):
  try: return float(x),Num
  except ValueError: return x,Sym

class Num:
  def __init__(i):
    i.lo  = 10**32
    i.hi  = -1*10**32
  def add(i,x):
    x = float(x)
    if x < i.lo: i.lo = x
    if x > i.hi: i.hi = x
    return x
  def norm(i,x):
    return (x - i.lo) / (i.hi - i.lo + 10**-32)
  def dist(i,x,y):
    return i.norm(x) - i.norm(y)

class Sym:
  def __init__(i) : pass
  def add(i,x)    : return x
  def norm(i,x)   : return x
  def dist(i,x,y) : return 0 if x==y else 1

class Col:
  "something that can handle  Nums or Syms"
  def __init__(i, pos, txt):
    i.txt, i.pos,i.about = txt,pos,None
  def add(i,x):
    if i.about is None:
      x,what  = atom(x)
      i.about = what()
    return i.about.add(x)

class Data:
  def __init__(i):
    i.all = []
    i.evals=0
    i.cols, i.objs, i.decs, i.klass = {}, [],[],[],[]
  def __call__(i,row):
    if i.cols:
      for pos,cell in enumerate(row):
        row[pos] = i.cols[pos].add(cell)
      i.all += [row]
    else:  
      for pos,cell in enumerate(row):
        col = i.cols[pos] = Col(pos,cell)
        if   cell[0] == LOVE  : i.objs  += [(col,more)]
        elif cell[0] == HATE  : i.objs  += [(col,less)]
        elif cell[0] == KLASS : i.klass += [col]
        else                  : i.decs  += [col]
        
      for col in i.objs : col.about = Num()
      for col in i.klass: col.about = Sym()
  def distance(i,r1,r2,f=2):
    inc,n = 0, 10**-32
    for col in i.decs:
      n    += 1
      x, y  = r1[col.pos], r2[col.pos]
      inc  += col.about.dist(x,y)**f
    return inc**f/n**f
  def furthest(i,r1, better= more, init= 0):
    most,out = init, None
    for r2 in i.all:
      if id(r1) != id(r2):
        tmp = i.distance(r1,r2)
        if better(tmp, most):
          most,out = tmp,r2
    return out
  def closest(i,r1):
    return i.furthest(r1, better= less, init= 10**32)
  def eval1(i,row): return row # usually rewritten by subclass
  def eval0(i,row): return i.eval(row, free=True)
  def eval(i,row, free=False):
    for col,_ in i.objs:
      if row[col.pos] == UNKNOWN:
        row = i.eval1(row)
        if not free:
          i.evals += 1
      else:
        break
    return row

def bdom(x,y,data):
  x= data.eval(x)
  y= data.eval(y)
  betters = 0
  for col,better in data.objs:
    x1,y1 = x[col.pos], y[col.pos]
    if better(x1,y1) : betters += 1
    elif x1 != y1    : return False # must be worse
  return betters > 0

def cdom(x, y, data,bigEnough=0.01, ee= 2.718281828459):
  x= data.eval(x)
  y= data.eval(y)
  def w(better):
    return -1 if better == less else 1
  def expLoss(w,x1,y1,n):
    return -1*ee**( w*(x1 - y1) / n )
  def loss(x, y):
    losses= []
    n = min(len(x),len(y))
    for col,better in data.objs:
      x1 = x[col.pos] 
      y1 = y[col.pos] 
      loss += exploss( w(better),x1,y1,n)
    return sum(losses) / n
  l1 = loss(x,y)
  l2 = loss(y,x)
  return l1 < l2 if abs(l1 - l2) >= bigEnough else False

def sway( population, data, better= cdom,
                            e=0.5, least=20) :
  def cluster(items, out): 
    if    len(items) < enough: 
          out += [items] 
    else: west, east, westItems, eastItems = split(items, int(len(items)/2)) 
          if not better(west,east,data): cluster( eastItems, out )  
          if not better(east,west,data): cluster( westItems, out )
    return out
  def split(items, middle): 
    rand = random.choose( items) # 'FASTMAP', step1
    east = data.furthest(rand, items) # 'FASTMAP', step2
    west = data.furthest(east, items) # east,west are now 2 distant items
    c    = data.distance(west, east)
    lst  = []
    for x in items:  
       a   = data.distance(x,west)
       b   = data.distance(x,east)
       # find the distance of 'x' along the line running west to east
       lst += [( a*a + c*c - b*b )/( 2*c+ 0.0001 ),x] # cosine rule
    items = map(lambda z:z[1],
                sorted(items)) # sorted by 'd'
    return west, east, items[:middle], items[middle:]
  # --------
  enough= max(len(population)**n, least) # why 20? central limit theorem
  return cluster(population, [])
  
data=Data()

for line in sys.stdin:
  row = map(lambda z:z.strip(),line.split(","))
  if row:
    data(row)
    
for row in data.all:
  print("")
  print(row)
  cl = data.closest(row)
  far= data.furthest(row)
  print(cl, data.distance(row,cl))
  print(far, data.distance(row,far))
  
  
print("keys",data.cols.keys())
print("more",map(lambda z:z.pos, data.more))
print("less", map(lambda z:z.pos, data.less))
print("decs",map(lambda z:z.pos, data.decs))
