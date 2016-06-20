# Python 101

REad this book:

## My Conventions

- Indentaion always with 2 spaces.
- Not `self` but `i` (saves sooo much width)
- For data-only classes, I use `o` which kinda emulates structs in Javascript.
- Many functions have demo scripts. So the file X.py might have
  the file Xok.py for the demos.

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