# Python 101

REad this book:

## Watch this manifesto

https://www.youtube.com/watch?v=nIonZ6-4nuU

## My Conventions

- Indentaion always with 2 spaces.
- Not `self` but `i` (saves sooo much width)
- For data-only classes, I use `o` which kinda emulates structs in Javascript.
- Many functions have demo scripts. So the file X.py might have
  the file Xok.py for the demos.

- Options stored in a global nested dictionary called `The`.

Wrong way to access those options (since in the following, `this` is
evaluated once at load time and never can be changed):

```python
class XYZ:
 def __init__(i, this=The.this):
   i.this = this
   ...
   
```

Right way (options reset everytime this is called):

```python
class XYZ:
 def __init__(i, this=None):
   i.this = this or The.this
   ...
```

Finally, some variables contain HUGE amounts of data and confuse debugging (due to their very long
  print strings). I mark these variables with a leading `_` and use `__repr__` methods
  that know not to print those confusing variables. For an example of that, see below.

```python
class o:
  def __init__(i, **adds): i.__dict__.update(adds)
  def __repr__(i)        : return str(kv(i.__dict__))


def kv(d, private="_",
       places=None):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,places or The.tricks.round) if isa(x,float) else x
  return ['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]
```


## Writing Demo Files

In this example, we write a file `tricksok.py` to
test the file `tricks.py`.

First 3 lines (standard stuff):

```python
from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
```

The next line imports the file you want to demo (in this
case `tricks.py`:

```python
from tricks import *
```

Now write functions annotated by `@ok`; e.g.

```
@ok
def _rand():
  """Seed control: the same `random` nums will
     print after resetting the seed"""
  rseed(1)
  print([r() for _ in range(5)])
  rseed(1)
  print([r() for _ in range(5)])
```

You can write as many of these annocated functions as you like.
Optionally, you can add doc strings to the functions (these
will be printed along with the demo output).

## Running the demo files.

The following code will load and run all the `@ok`
functions

```python
python tricksok.py
```

