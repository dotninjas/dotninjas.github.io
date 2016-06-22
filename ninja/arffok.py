from __future__ import division,print_function
import sys,math
sys.dont_write_bytecode=True

from arff import * 

"""_______________________________________________________________________
## demo

For example, consider the file `weather.arff`:

    @relation weather
    @attribute outlook     {sunny,  overcast, rainy}
    @attribute temperature real
    @attribute humidity    real
    @attribute windy       {TRUE , FALSE}
    @attribute play        {yes  , no}
    @data
    sunny,       85,         85,       FALSE,  no
    sunny,       80,         90,       TRUE,   no
    overcast,    83,         86,       FALSE,  yes
    rainy,       70,         96,       FALSE,  yes
    rainy,       68,         80,       FALSE,  yes
    rainy,       65,         70,       TRUE,   no
    overcast,    64,         65,       TRUE,   yes
    sunny,       72,         95,       FALSE,  no
    sunny,       69,         70,       FALSE,  yes
    rainy,       75,         80,       FALSE,  yes
    sunny,       75,         70,       TRUE,   yes
    overcast,    72,         90,       TRUE,   yes
    overcast,    81,         75,       FALSE,  yes
    rainy,       71,         91,       TRUE,   no

"""

def tf(row):
  klass=row.y[0]
  if isinstance(klass,(int,float)):
    row.y[0] = 'true' if klass > 0 else 'false'
  return row

@ok
def _arff():
  """If we read this file and print the headers on the _x_ tub, we see the
     distributions of symbols and numbers in the independent (non-class)
     columns."""
  a=Arff('data/weather.arff')
  for n,log in a.rows.x.cols.items():
    print(n,log.thing)
#    print(x.thing)

"""
{0: ["counts: {'rainy': 5, 'overcast': 4, 'sunny': 5}", 'mode: sunny', 'most: 5', 'n: 14'], 
 1: ['lo: 64', 'm2: 561.43', 'mu: 73.57', 'n: 14', 'up: 85'], 
 2: ['lo: 65', 'm2: 1375.21', 'mu: 81.64', 'n: 14', 'up: 96'], 
 3: ["counts: {'TRUE': 6, 'FALSE': 8}", 'mode: FALSE', 'most: 8', 'n: 14']}
}

"""

@ok
def _arffWrite():
  """If we read this file and print the headers on the _x_ tub, we see the
     distributions of symbols and numbers in the independent (non-class)
     columns."""
  a=Arff('data/weather.arff')
  print('\n'.join(a.write()))


oks()

