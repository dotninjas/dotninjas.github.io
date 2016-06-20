from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from tubs import *

@ok
def _sym():
  print(Sym(list('i have gone to seek a great perhaps')))

@ok
def _col():
  rseed(1)
  n= Num( [ 600 , 470 , 170 , 430 , 300])
  print(n,n.sd())
