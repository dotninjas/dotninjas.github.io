from __future__ import division
import random

rseed = random.seed
r     = random.random
weibul = random.weibullvariate
any    = random.choice

def r3(f)    : return round(f, 3)
def r3s(lst) : return map(r3,lst)

def r2(f)    : return round(f, 2)
def r2s(lst) : return map(r2,lst)

class o:
  def __init__(i,**d)    : i.__dict__.update(**d)
  
the = o(SAMPLE = o(max=256))

def chi2(obs1,obs2):
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
  return sum(chi), chi2Threshold(df)

def _chi2():
  male  =  dict(rep=200, dem=150, ind=50)
  female = dict(rep=250, dem=300, ind=50)
  print chi2(male, female)
  print ""
  dem = dict(favor=138, indiff=83, opposed=64)
  rep = dict(favor=64,  indiff=67, opposed=84)
  print chi2(dem, rep)
  

def chi2Threshold(df,conf=99,
         ns  =  [       1    ,      2,      5,     10,    15,
                        20   ,     25,     30,     60,   100],
         vals= {99 : [  0.000,  0.020,  0.554,  2.558,  5.229,
                        8.260, 11.524, 14.953, 37.485, 70.065], 
                95 : [  0.004,  0.103,  1.145,  3.940,  7.261,
                       10.851, 14.611, 18.493, 43.188, 77.929], 
                90 : [  0.016,  0.211,  1.610,  4.865,  8.547,
                       12.443, 16.473, 20.599, 46.459, 82.358]}):
  return xtend(df,ns,vals[conf])

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

def mofn(lst,m=10,n=100):
  if len(lst) < n:
    return mofn(lst + lst,m,n)
  inc  = int(len(lst)/m)
  return sorted(lst)[0::inc]

_chi2()
class Sample:
  "Keep, at most, 'size' things."
  def __init__(i, init=[], size=None):
    i.max = size or the.SAMPLE.max
    i.n, i.all, i.ordered = 0, [], False
    map(i.__iadd__,init)
  def report(i):
    i.all, i.ordered = sorted(i.all), True
    q  = int(len(i.all)/4)
    q1 = i.all[q]
    q2 = i.all[q*2]
    q3 = i.all[q*3]
    return q2, q3 - q1
  def __iadd__(i,x):
    i.ordered = False
    i.n += 1
    now  = len(i.all)
    if now < i.max:
      i.all += [x]
    elif r() <= now/i.n:
      i.all[ int(r() * now) ]= x
    return i

def _sample1(  repeats=1000, samples=512, m=100, cache=512):
  #s=Sample()
  aas = [1,2,3,4,5]
  bbs = [0.5,1,1.5,5]
  for _ in xrange(repeats):
    a  = any(aas)
    b  = any(bbs)
    s1 = [weibul(a,b) for _ in xrange(samples)]
    s2 = [weibul(a,b) for _ in xrange(samples)]
    
    sum1,sum2  = sum(s1), sum(s2)
    s1 = [x/sum1 for x in s1]
    s2 = [x/sum2 for x in s2]
    
    s3 = mofn( Sample(s2,cache).all,  m)
    s1 = mofn( s1,                    m)
    s2 = mofn( s2,                    m)
        
    diff1 = r3s([abs(x-y) for x,y in zip(s1,s2)])
    diff2 = r3s([abs(x-y) for x,y in zip(s1,s3)])
    yield sum(diff1) / len(s2),  sum(diff2) / len(s3)

def _sample():
  rseed(10293082)
  p = lambda x: round(x,4)
  print("cache x=twof y=1f1cache z=y/x")
  for c in [32,64,128,256,512]:
    one,two=[],[]
    for  x,y in _sample1(cache=c,m=6):
      one += [x]
      two += [y]
    n1 = p(sum(one) / len(one))
    n2 = p(sum(two) / len(two))
    print c, n1, n2, r2(n2/n1)

_sample()
