"""

# knn.py : tricks for reading and writing an arff file

(C) 2016 tim@menzies.us, MIT license

"""

from __future__ import division,print_function
import sys,argparse
sys.dont_write_bytecode=True
from arff import *
from abcd import *

def knn(train,tests, k=1):
  abcd=Abcd("train","raw")
  train = Arff(train).reads().rows
  for test in  Arff(tests).read1():
    abcd(actual  = test.y[0],
         predict = train.knn(test, k=k))
  print("")
  return abcd.report()

if __name__ == "__main__":
  x = args(
    "kNearest neighbor",
    #arg   #type #default       #meta  #help
    ("-k", int,  1,            'k',    "use k nearest neighbors"),
    ("-t", str,  'train.arff', "File", "training set (arff file)"),
    ("-T", str, 'test.arff',   "File", "test set (arff file)"))
  knn(x.t, x.T, x.k)
