"""# rows.py : tricks for storing rows of data.

(C) 2016 tim@menzies.us, MIT license

"""
from __future__ import division,print_function
import sys,math 
sys.dont_write_bytecode=True

"""
## `Rows` : The top-down story      

In data mining we deal with pairs of indepdent and dependent data

In optimization, we deal with decision and objectives 

For example, if a house has doors, location, rooms, salesPrice, maintenanceCost then

- doors, location, rooms are independent decisions 
- and `salesPrice, maintenanceCost` might be dependent things we want to predict with a  data miner
- or `salesPrice, maintenanceCost` might be objectives we want to maximize, minimize (respectively) with an optimizer.

Note that the synonyms: independent= decision and dependent=objective.  Those words
are far too long to type into code all the time so....

A `Row` is something that can be divided into into `x,y` columns.

- The `x` columns can be used for indepednent or decision attributes;
- The `y` columns can be used for depednent or objective d attributes;

Note that either `x` or `y` can be empty.

"""
class Row:
  def __init__(i,x=None,y=None):
    i.x = x or []
    i.y = y or []
"""

Since `x` or `y` can be empty, we keep a seperate set of  `Log`s  for each `x` and `y`. 

In the following, we build a `Rows` class that can keep a list of `Row`s while
keeping summaries of all the the `x` and `y` columns in a `Log` (one `Log` for
each column).

```
#      x1, x2, x3,    x4      y1, y2 
      -------------------    -------
Row(x=[ 0,  1,  2,   red], y=[ 3,  4])
Row(x=[ 2,  3,  4, green], y=[ 6,  6])
Row(x=[ 1,  2,  3,   red], y=[ 4,  5])
```

If we add these to `Rows` then:

-  In the summary objects for `x1,x2,x3` we will see means of 1,2,3;
-  In the summary objects for `x4` we will see a mode 
   of `green` and frequency counts for `red,green` of 2,1;
-  In the summary objects for `y1,y2` we will see means of 4,5.

## `Rows`: the bottom-up story.

If the beginning was the thing and the thing was a `Num` or a `Sym`.

And the things needed a place to gather and so was created the `Log`
that `Sample`d some of the `Thing`s while keeping summaries on all the the
`Thing`s seen too date. And the `Log` was smart in that you just kept throwing stuff at it and it worked out if if you were throwing `Num`s or `Sym`s.

And somethings we say lots of data arriving at the same time and so was created the `Logs` that held multiple `Log`s.

And the data being thown at the `Logs` was `Row` which had two parts:
and `x` list and a `y` list.

And `Rows` was a place made to store many `Row`s and the `Rows` kept summaries
of the data in one `Logs` for `x` and another `Logs` for `y`.

So `Rows` have 2 `Logs` and each `Logs` has many `Log` and each `Log` has one
`Thing` (and that `Thing`) could be a `Num` or a `Sym`).

## Less Informally:

A `Log` is a place to store columns of data:

- Columns contain either symbols or numbers.  
- Columns have headers called `Sym` and `Num` and store summaires about
  symbolic or numeric columns, respectively.
- When a `Row` is dumped into a `Logs`, the column headers are automatically
  updated with information from that row

Important note:

- While `Row`s contain all the raw data, columns only contain a _summary_
  of the data seen in each column.

"""


from tricks import * 

The.rows = o(few     = 256,
             keepLog = False,
             keepRows= True)

def isMissing(x):
  "Null cells in columns contain '?'"
  return x == "?"

"""

## `Thing`

`Thing`s have two sub-classes: `Num` and `Sym`.

"""
class Thing:
  def __init__(i,inits=[],get=same):
    i.reset()
    i._get = get
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    x = i._get(x)
    if not isMissing(x): i.add(x)
    return i
  def __isub__(i,x):
    x = i._get(x)
    if not isMissing(x): i.sub(x)
    return i
  def __repr__(i):
    return str(kv(i.__dict__))
"""

### `Sym`

Incrementally adds and subtracts symbol counts as well the most common symbol
       (the `mode`). Can report column `entropy`.

"""  
class Sym(Thing):
  def reset(i):
    i.counts, i.most, i.mode, i.n = {},0,None,0
  def add(i,x):
    i.n += 1
    new = i.counts[x] = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new,x
  def sub(i,x):
    i.n -= 1
    i.counts[x] -= 1
    if x == i.mode:
      i.most, i.mode = None,None
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
"""

### `Num`

Incrementally adds and subtracts numners to a Gaussian, tracking `mu` and
       `sd()` as we go.  Smallest and largest values seen are 'lo' and `up`.  Can
       report column `standard deviation`.

"""
class Num(Thing):
  def reset(i):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
  def add(i,x):
    """Incremental addition using ??Knuths 1964 method, see
       https://goo.gl/gk32eX."""
    i.n += 1
    if x < i.lo: i.lo=x
    if x > i.up: i.up=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    """During subtraction, if counts go negative, cap them at zero."""
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  def sd(i):
    "Measures how varied are the measures from the mean."
    return 0 if i.n <= 2 else (i.m2/(i.n - 1))**0.5
  def small(i,cohen=0.3):
    return i.sd()*cohen

"""

## `Sample`

A place to keep, at most, a 'few' things.

"""

class Sample:
  def __init__(i, init=[], few=None):
    i.few = The.rows.few if few is None else flse
    i.n, i.some, i.ordered = 0, [], False
    map(i.__iadd__,init)
  def report(i):
    i.some, i.ordered = sorted(i.some), True
    q  = int(len(i.some)/4)
    return i.some[q*2], i.some[q*3] - i.some[q]
  def __iadd__(i,x):
    i.ordered = False
    i.n += 1
    now  = len(i.some)
    if now < i.few:
      i.some += [x]
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
    return i
"""

## `Log`
 
`Log`umns are places to sample a stream of `Thing`s (and it will work out if you
are working with `Num`s or `Sym`s). The summary of the `Thing`s is kept in `about`.

The type of `Thing` is defermined by the first non-empty entry seen.

"""

class Log:
  def __init__(i,few=None):
    i.sample=Sample(few= few)
    i.about = None
  def __iadd__(i,x):
    if not isMissing(x):
      if i.about is None:
        i.about = Sym() if isSym(x) else Num()
      i.about  += x
      i.sample += x
    return i
    
"""


## `Logs`   

- Holds a set of `Log`s
- When a new `Row` is added, updates column summaries.
- When processing a `Row`,  if a cell is empty (defined by `isMissing`) then we skip over it.
- Before summarizing a row in a column header, the row is filted via some `get`
  function (which defaults to `same`; i.e.  use the whole row, as is).

Note that `Logs`s may or may not not store the `rows` 

"""
class Logs:
  def __init__(i,get = same,keep=None):
    i.cols = None  # i.cols[i] is a summary of column i.
    i._get = get
    i.keep = The.rows.keepLog if keep is None else keep
    i._all  = []
  def __iadd__(i,lst):
    lst = i._get(lst)
    if i.cols is None:
      print(1)
      i.cols = {j:Log() for j,_ in enumerate(lst)}
    for j,val in enumerate(lst):
      i.cols[j] += val
    if i.keep:
      i.all.append(lst)
    return i

"""

## `Rows`
 
A `Rows` is a place to store many `Row`s and summaries about those rows.
Those summaries are stored in two `Logs`s.

- The `x` field holds a `Log` of any independent data;
- The `y` field holds a `Log` of any dependent data (e.g. one of more class
  variables).
- When a row is added to a `Rows`, its `x,y` components are sent to two
  seperate _Logs_
0 The knowledge of how to access `x`, or
 `y` out of the row is given to a `Rows` when it is created (see the following
 `Rows.get` attribute).

First, need accessors to _x,y_ fields:

"""
def xx(z): return z.x
def yy(z): return z.y

class Rows:
  def __init__(i,xx=xx,yy=yy,keep=None):
    i.x=Logs(xx)
    i.y=Logs(yy)
    i.keep = The.rows.keepRows if keep is None else keep
    i._all = []
  def __iadd__(i,row):
    i.x += row
    i.y += row
    if i.keep:
      print("+")
      i._all.append(row)
    return i
  def col(i,pos):
    if  pos < len(i.x.cols):
      return i.x.cols[pos]
    else:
      return i.y.cols[len(i.x.cols) - pos ]
  def cell(i,row,pos):
     if  pos < len(i.x.cols):
      return row.x[pos]
     else:
      return row.y[len(i.x.cols) - pos]

