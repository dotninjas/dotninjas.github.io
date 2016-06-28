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
    near         = train.knn(test, k=k)
    abcd(actual  = test.y[0],
         predict = near)
  return abcd.report()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="kNearest neighbor")
  p=parser.add_argument
  p("-k",   type=int,
    default=1, metavar='k',
    help="use k nearest neighbors")
  p("-t",type=str, metavar="File",default='train.arff',
    help="training set (arff file)")
  p("-T",type=str, metavar="File",default='test.arff',
    help="test set (arff file)")
  args = parser.parse_args()
  knn(args.t, args.T, args.k)
