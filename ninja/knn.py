"""

# knn.py : tricks for reading and writing an arff file

(C) 2016 tim@menzies.us, MIT license

"""

from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from arff import *
from abcd import *

def knn(train,tests, xy=xx):
  abcd=Abcd("train","raw")
  train = Arff(train).reads().rows
  for test in  Arff(tests).read1():
    near = train.closest(test,xy)
    print("")
    print(id(near)==id(test))
    print(xy(near))
    print(xy(test))
    predicted = near.y[0]
    actual    = test.y[0]
    abcd(actual, predicted)
  return abcd
    
    
    
    
