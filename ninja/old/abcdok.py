from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from abcd import *

@ok
def demo():
  apple,orange,pear,durian="apple","orange","pear","durian"
  data = [("ram", "demo"),
          (apple, orange),(  apple, apple),( apple, pear),
          ( apple, durian), ( orange, apple)]
  abcd  = None
  for actual, predicted in data:
    if abcd:
      abcd(actual, predicted)
    else:
      abcd = Abcd( actual, predicted )
  abcd.report()

oks()
  
