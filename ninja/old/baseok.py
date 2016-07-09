import sys
sys.dont_write_bytecode=True # don't write irritating .pyc files

from base import *


b = mycopy(The)

b.misc.round=1000

print(b)

print(The)


print(22)
o1 = o(n=0.11111111111)
print("<",The.misc.round)
assert str(o1) == "<n: 0.1111>"
Then = mycopy(The)
The.misc.round = 2
assert str(o1) == '<n: 0.11>'
print("=",The.misc.round)
The = mycopy(Then)
print(">",The.misc.round)
print("...")
print("!!",str(o1))

#assert str(o1) == "<n: 0.1111>"
#assert str(o1) == '<n: 0.1111>'

#print("!!",str(o1))
#print(">>>",str(o1))
#assert str(o1) == "<n: 0.1111>"
#print(">",The.misc.round)
oks()
