from __future__ import division,print_function
import sys,re,random
sys.dont_write_bytecode=True

def less(x,y): return x < y
def more(x,y): return x > y
def max(x,y):  return x if x>y else y
def min(x,y):  return x if x<y else y

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

class Rows:
  def __init__(i):
    i.all = []
    i.cols, i.wants, i.decisions = {}, [],[],[]
  def __call__(i,row):
    if i.cols:
      for pos,cell in enumerate(row):
        row[pos] = i.cols[pos].add(cell)
      i.all += [row]
    else:  
      for pos,cell in enumerate(row):
        col = i.cols[pos] = Col(pos,cell)
        print(cell)
        if   cell[0] == ">" : i.wants     += [(col,more,less)]
        elif cell[0] == "<" : i.wants     += [(col,less,more)]
        else                : i.decisions += [col]
  def distance(i,r1,r2):
    inc,n = 0, 10**-32
    for col in i.decisions:
      n    += 1
      x, y  = r1[col.pos], r2[col.pos]
      inc  += col.about.dist(x,y)
    return inc**2/n**2
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
  def bdom(i,r1,r2):
    betters = 0
    for col,better,worse in i.wants:
      x,y = r1[col.pos], r2[col.pos]
      if better(x,y): betters += 1
      if worse(x,y) : return False
    return betters > 0
  def cdom(i,x, y,space,bigEnough=0.01):
    ee = 2.718281828459
    def w(better):
      return -1 if better == less else 1
    def expLoss(w,x,y,n):
      return -1*ee**( w*(x - y) / n )
    def loss(x, y):
      losses= []
      n = min(len(x),len(y))
      for col,better,_ in i.wants:
        x1 = col.about.norm( x[col.pos] )
        y1 = col.about.norm( y[col.pos] )
        loss += exploss( w(better),x1,y1,n)
      return sum(losses) / n
    l1 = loss(x,y)
    l2 = loss(y,x)
    return l1 < l2 if abs(l1 - l2) >= bigEnough else False


def bdom(x,y,rows): return rows.bdom(x,y)
def cdom(x,y,rows): return rows.cdom(x,y)

def sway( population, rows, better= cdom,
                            e=0.5, least=20) :
  def cluster(items, out): 
    if    len(items) < enough: 
          out += [items] 
    else: west, east, westItems, eastItems = split(items, int(len(items)/2)) 
          if not better(west,east,rows): cluster( eastItems, out )  
          if not better(east,west,rows): cluster( westItems, out )
    return out
  def split(items, middle): 
    rand = random.choose( items) # 'FASTMAP', step1
    east = rows.furthest(rand, items) # 'FASTMAP', step2
    west = rows.furthest(east, items) # east,west are now 2 distant items
    c    = rows.distance(west, east)
    lst  = []
    for x in items:  
       a   = rows.distance(x,west)
       b   = rows.distance(x,east)
       # find the distance of 'x' along the line running west to east
       lst += [( a*a + c*c - b*b )/( 2*c+ 0.0001 ),x] # cosine rule
    items = map(lambda z:z[1],
                sorted(items)) # sorted by 'd'
    return west, east, items[:middle], items[middle:] 
  enough= max(len(population)**n, least) # why 20? central limit theorem
  return cluster(population, [])
  
rows=Rows()

for line in sys.stdin:
  row = map(lambda z:z.strip(),line.split(","))
  if row:
    rows(row)
    
for row in rows.all:
  print("")
  print(row)
  cl = rows.closest(row)
  far= rows.furthest(row)
  print(cl, rows.distance(row,cl))
  print(far, rows.distance(row,far))
  
  
print("keys",rows.cols.keys())
print("more",map(lambda z:z.pos, rows.more))
print("less", map(lambda z:z.pos, rows.less))
print("decs",map(lambda z:z.pos, rows.decisions))
