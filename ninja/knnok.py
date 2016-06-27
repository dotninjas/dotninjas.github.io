from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from knn import *

@ok
def _knn():
  knn('data/weather.arff','data/weather.arff').report()
  
@ok
def _knn1():
  knn('data/diabetes.arff','data/diabetes.arff').report()

oks()
  
