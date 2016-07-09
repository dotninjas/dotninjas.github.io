
""" __________________________________________________

# simplestats.py: simple basic stats

"""

from __future__ import division,print_function
import sys,math 
sys.dont_write_bytecode=True


def normalDiff(mu1,sd1,n1,mu2,sd2,n2): 
    nom   = mu2 - mu1
    denom = delta/((sd1/n1 + sd2/n2)**0.5) if s1+s2 else 1
    return nom/denom

def lstDiff(lst1,lst2):
 """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    tmp1 = tmp2 = 0
    n1,n2 = len(lst1), len(lst2)
    mu1   = sum(lst1) / n1
    mu2   = sum(lst2) / n2
    tmp1  = sum( (y1 - mu1)**2 for y1 in lst1 )
    tmp2  = sum( (y2 - mu2)**2 for y2 in lst2 )
    sd1   = ( tmp1 / (n1 - 1) )**0.5
    sd2   = ( tmp2 / (n2 - 1) )**0.5
    return normalDiff(mu1,sd1,n1,mu2,sd2,n2)

""" _________________________________________________

## Stats tricks

"""

def xtend(x,xs,ys):
  """given pairs ofs values, find the gap with x
     and extrapolate at that gap size across the y
    xtend(-5, [0,5,10,20], [0,10,20,40] ) ==> -10
    xtend(25, [0,5,10,20], [0,10,20,40] ) ==>  50
    xtend(40, [0,5,10,20], [0,10,20,40] ) ==>  80
  """ 
  x0, y0 = xs[0], ys[0]
  for x1,y1 in zip(xs,ys):  
    if x < x0 or x > xs[-1] or x0 <= x < x1:
      break
    x0, y0 = x1, y1
  gap = (x - x0)/(x1 - x0)
  print dict(x0=x0,x=x,x1=x1,gap=gap,y0=y0,y1=y1)
  return y0 + gap*(y1 - y0)

def ttestThreshold(df,conf=99,
         xs= [	         1,	    2,	   5,	   10,	  15,	   20,    25,	  30,	    60,	 100]
         ys={0.9:  [ 3.078, 1.886, 1.476, 1.372, 1.341, 1.325, 1.316, 1.31,  1.296, 1.29], 
             0.95: [ 6.314, 2.92,  2.015, 1.812, 1.753, 1.725, 1.708, 1.697, 1.671, 1.66], 
             0.99: [31.821, 6.965, 3.365, 2.764, 2.602, 2.528, 2.485, 2.457, 2.39,  2.364]}):
  return xtend(df,xs,ys[conf])

def ttestSame(lst1,lst2,conf=95):
   df = min(len(lst1) - 1, len(lst2) - 1)
   return ttestThreshold(df) < lstDiff(lst1,lst2)

def chi2Threshold(df,conf=99,
         xs  =  [       1    ,      2,      5,     10,    15,
                        20   ,     25,     30,     60,   100],
         ys= {99 : [  0.000,  0.020,  0.554,  2.558,  5.229,
                        8.260, 11.524, 14.953, 37.485, 70.065], 
                95 : [  0.004,  0.103,  1.145,  3.940,  7.261,
                       10.851, 14.611, 18.493, 43.188, 77.929], 
                90 : [  0.016,  0.211,  1.610,  4.865,  8.547,
                       12.443, 16.473, 20.599, 46.459, 82.358]}):
  return xtend(df,xs,ys[conf])

def chi2Same(obs1,obs2):
  obs12,tot1,tot2,r,c = {},0,0,2,0
  for k,v in obs1.items():
    c    += 1
    tot1 += v
    obs12[k] = obs12.get(k,0) + v
  for k,v in obs2.items():
    tot2 += v
    obs12[k] = obs12.get(k,0) + v
  tots    = tot1 + tot2
  expect1 = { k:tot1*v/tots for k,v in obs12.items() }
  expect2 = { k:tot2*v/tots for k,v in obs12.items() }
  chi     = [ (obs1[k]  - expect)**2/expect for k,expect in expect1.items() ] + [ 
              (obs2[k]  - expect)**2/expect for k,expect in expect2.items() ]
  df      = (r-1)*(c-1)
  return  chi2Threshold(df) < sum(chi)
