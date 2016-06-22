"""

# arff.py : tricks for reading and writing an arff file

(C) 2016 tim@menzies.us, MIT license

"""

from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from rows import *


"""_______________________________________________________________________

This code reads a data file of the following form:

    @RELATION iris
    
    @ATTRIBUTE sepallength  NUMERIC
    @ATTRIBUTE sepalwidth   NUMERIC
    @ATTRIBUTE class        {Iris-setosa,Iris-versicolor,Iris-virginica}
  
    @DATA
    5.1,3.5,Iris-setosa
    4.9,3.0,Iris-setosa
    4.7,3.2,Iris-setosa
    ...

The `rows` after `@data` are stored in `Tubs` (where it is assumed the last
cell in each row is the class).  Other information is stored in a list of
`attributes` and the name of the `relation`.

The input rows from a file are all strings so first they are coerced to floats,
ints, or strings using `thing`.  Next, the coerced row is sent through a
customisable `prep` (which defaults to `same`).

Note that when reading the @XXX tags, `Arff` uses a case-insensitive match
(see the use of `re.IGNORECASE`, below).

"""
class Arff:
  def __init__(i, f, prep=same):
    i.rows = Rows()
    i.attributes = []
    i.relation   = 'relation'
    i.prep       = prep
    i.reads(f)
  def empty(i,x):
    return re.match('^[ \t]*$',x)
  def at(i,x,txt):
    return re.match('^[ \t]*@'+txt,x,re.IGNORECASE)
  def header(i):
    return ", ".join(i.attributes)
  def reads(i,f):
    data = False
    with open(f)  as fs:
      for line in fs:
        line = re.sub(r'(["\'\r\n]|#.*)', "", line)
        if line:
          if not i.empty(line): # skip blank lines
            if data:
              line = line.split(",")
              line = map(thing,line)
              indep= line[:-1]
              dep  = [line[-1]]
              row = i.prep(Row(x=indep,y=dep))
              i.rows += row
            else:
              line = line.split()
              if i.at(line[0],'RELATION'):
                i.relation = line[1]
              elif i.at(line[0],'ATTRIBUTE'):
                i.attributes += [line[1]]
              elif i.at(line[0],'DATA'):
                data=True
  def write(i):
    lines=[]
    lines += ["@relation "+i.relation + "\n"]
    for pos,attr in enumerate(i.attributes):
      col = i.rows.col(pos)
      txt=""
      if isa(col,Num):
        txt = "real"
      else:
        vals = set([i.rows.cell(row,pos) for row in i.rows._all]) 
        txt = "{ " + ', '.join(vals)+ " }"
      lines += [ "@attribute "+attr+ " " + txt ]
    lines += ["\n@data\n"]
    for row in i.rows._all:
      lines += [ ', '.join(map(str,row.x + row.y)) ]
    return lines
    
