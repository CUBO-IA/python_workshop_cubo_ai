# Python Data Types: Complete Beginner's Guide

A companion to the ten scripts in this folder. Each file focuses on one data
type, explains what it is, and ends with runnable examples, common mistakes,
and best practices.

## Table of Contents

1. [Introduction](#introduction)
2. [None](#none-noneType) — the absence of a value
3. [Booleans](#booleans-bool)
4. [Integers](#integers-int)
5. [Floats](#floats-float)
6. [Complex](#complex-complex)
7. [Strings](#strings-str)
8. [Lists](#lists-list)
9. [Tuples](#tuples-tuple)
10. [Dictionaries](#dictionaries-dict)
11. [Sets](#sets-set)
12. [Choosing the right type](#choosing-the-right-type)
13. [Related notes](#related-notes)

---

## Introduction

Python has a small set of built-in data types. Between them they cover almost
everything you write in day-to-day Python, and knowing them well is the
foundation for everything else — functions, classes, and the standard library
all build on these.

### The ten types at a glance

| Type | Example | Mutable | Ordered | Hashable | Notes |
|---|---|---|---|---|---|
| `NoneType` | `None` | — | — | ✅ | Signals "no value" |
| `bool` | `True` | — | — | ✅ | Subclass of `int` |
| `int` | `42` | ❌ | — | ✅ | Arbitrary precision |
| `float` | `3.14` | ❌ | — | ✅ | Approximate (IEEE 754) |
| `complex` | `3 + 4j` | ❌ | — | ✅ | Real + imaginary parts |
| `str` | `"hello"` | ❌ | ✅ | ✅ | Sequence of characters |
| `list` | `[1, 2, 3]` | ✅ | ✅ | ❌ | Default collection |
| `tuple` | `(1, 2, 3)` | ❌ | ✅ | ✅ | Immutable, hashable |
| `dict` | `{"a": 1}` | ✅ | ✅ | ❌* | Key–value mapping |
| `set` | `{1, 2, 3}` | ✅ | ❌ | ✅ | Unique items only |

\* A dict is unhashable, but its **keys** must be hashable.

### Numeric tower

`bool` → `int` → `float` → `complex` form a widening tower. Mixing them in
arithmetic works and always produces the widest type involved, so
`1 + 1.5 + 1j` is simply `2.5 + 1j`. You never have to convert manually.

### Mutable vs immutable

* **Mutable** (`list`, `dict`, `set`) — can be changed in place after creation.
* **Immutable** (`int`, `float`, `complex`, `str`, `tuple`, `None`, `bool`) —
  every "change" produces a brand-new object.

Immutable types are hashable and safe to share; mutable ones cannot be used as
dictionary keys or set members.

### Running the examples

Each script runs standalone and prints annotated output:

```bash
python3 boolean.py
python3 complex.py
```

> **Note:** you can run these from inside this folder. They are named after
> types (`strings.py`, `list.py`, `set.py`, …), and the plural on `strings.py`
> deliberately avoids shadowing the standard-library `string` module — see
> [Related notes](#related-notes) for why that matters.

---

## None (NoneType)

**File:** [`none.py`](none.py)

`None` is the single value of the `NoneType` class. It represents the
*absence* of a value — no result, nothing found, not applicable, or unset.

```python
result = None
print(result)              # None
print(type(result))        # <class 'NoneType'>
```

The key idea is the difference between *an empty container* and *no container*:
`[]` is a real list holding zero items, while `None` means there is no list
here at all.

* **Singleton** — there is exactly one `None` object; everything points at it.
* **Falsy but not equal** — `bool(None)` is `False`, yet `None == False` and
  `None == 0` are both `False`.
* **Compare with `is`** — always `is None`, never `== None`.
* **You get it for free** — a function with no `return`, a failed `dict.get()`,
  or a regex `.search()` with no match all produce `None`.
* **Nearly inert** — arithmetic, `len()`, and method calls all raise.

```python
if value is None:          # correct
    ...
if value == None:          # wrong style
    ...

def add(item, bucket=None):
    if bucket is None:      # avoids the mutable-default trap
        bucket = []
    bucket.append(item)
    return bucket
```

Annotate optional returns so callers know to check:

```python
def find_user(user_id: int) -> dict | None: ...
```

---

## Booleans (bool)

**File:** [`boolean.py`](boolean.py)

`True` or `False` — capitalised in Python. The type of every yes/no answer, and
the result of every comparison.

```python
5 == 5          # True
is_logged_in = True
can_log_in = (user == "ada") and (password == "hunter2")
```

* `and`, `or`, and `not` combine and negate booleans.
* **Short-circuiting** — `and` and `or` stop as soon as the answer is known,
  which is the standard way to guard a risky operation.
* **Truthiness** — most values convert to `True` in a condition. Only `False`,
  `None`, zero, empty containers, and empty strings are falsy.
* `bool` subclasses `int`, so `True + True == 2`.

```python
if items:                 # preferred
    ...
if len(items) > 0:        # works, but clumsier
    ...
```

---

## Integers (int)

**File:** [`integer.py`](integer.py)

Whole numbers with no decimal point and **no size limit** — no overflow, and
no `int`/`long` split.

```python
x = 42
population = 8_000_000_000      # underscores for readability
print(2 ** 100)                 # a 31-digit number, exactly
```

* Operators: `+ - * / // % **` and `divmod(a, b)`.
* `/` always returns a **float**; `//` floor division returns an **int**.
* Immutable, hashable, safe to use as a dict key.
* Write `0b1010`, `0o17`, `0xFF` for binary, octal, and hex literals.

```python
7 / 2      # 3.5  (float)
7 // 2     # 3    (int)
7 % 2      # 1    (remainder)
int(2.9)   # 2    (truncates — use round(2.9) to round)
```

---

## Floats (float)

**File:** [`float.py`](float.py)

Decimal numbers stored as 64-bit IEEE 754 binary fractions. Any number written
with a `.` or an exponent.

```python
pi = 3.14159
large = 1.5e10
print(0.1 + 0.2)         # 0.30000000000000004
```

Because binary cannot represent most decimals exactly, floats are
**approximate**. Never compare them for equality after arithmetic:

```python
0.1 + 0.2 == 0.3                  # False!
math.isclose(0.1 + 0.2, 0.3)      # True  ← use this
round(0.1 + 0.2, 10) == 0.3       # True  ← or this
```

* `round()` uses **banker's rounding** (half-to-even): `round(2.5) == 2`.
* Use `math.floor` / `math.ceil` for explicit direction.
* `float("inf")` and `float("nan")` exist; `nan == nan` is `False`.
* For money, use `decimal.Decimal` — it is base-10 and exact.

```python
f"{amount:.2f}"        # '1234.57'  display precision
```

---

## Complex (complex)

**File:** [`complex.py`](complex.py)

Numbers with a real and an imaginary part, where `j * j == -1`. Built into
Python with no imports, and they mix freely with `int` and `float`.

```python
z = 3 + 4j
print(z)               # (3+4j)
print(z.real, z.imag)  # 3.0 4.0  ← always floats
print(abs(z))          # 5.0    ← magnitude
```

* **Write `1j`, never `j`** — a bare `j` is just an undefined variable name.
* `.real` and `.imag` always return **floats**, even for whole numbers.
* `abs(z)` returns the magnitude as a float, not a complex value.
* `z.conjugate()` flips the sign of the imaginary part.
* **Not ordered** — `<`, `>`, `sorted()`, and `max()` all raise `TypeError`.
  Sort with `key=abs` instead.
* `0j` is falsy and equals `0`; any other complex value is truthy.

```python
import cmath
cmath.sqrt(-1)          # 1j   (math.sqrt(-1) raises ValueError)
cmath.polar(3 + 4j)     # (5.0, 0.927...)   magnitude + angle
cmath.phase(3 + 4j)     # 0.927...          angle in radians
```

Use `cmath`, not `math`, for complex maths. Complex numbers show up in signal
processing, Fourier analysis, electrical engineering, and quantum mechanics.

---

## Strings (str)

**File:** [`strings.py`](strings.py)

An immutable sequence of characters, written in quotes.

```python
name = 'Ada'
quote = "It's fine"        # use the other quote style to avoid escaping
path = r"C:\Users\ada"     # raw string: backslashes stay literal
```

* **Immutable** — `s[0] = 'J'` fails; string methods return *new* strings.
* **Sequences** — indexing (`s[0]`, `s[-1]`) and slicing (`s[1:4]`, `s[::-1]`).
* **Unicode-aware** — `len("café")` is 4, counting characters not bytes.
* **Hashable**, so usable as dict keys and set members.

```python
s = "Python"
s[0], s[-1], s[1:4], s[::-1]   # 'P', 'n', 'yth', 'nohtyP'

"a,b,c".split(",")             # ['a', 'b', 'c']
"-".join(["a", "b"])           # 'a-b'
"Hello".startswith("He")       # True

f"{name} is {age}"             # f-strings: the modern way to format
```

---

## Lists (list)

**File:** [`list.py`](list.py)

The default collection: an ordered, **mutable**, growable sequence in square
brackets.

```python
fruits = ["apple", "banana"]
fruits.append("cherry")     # add one
fruits.extend(["date"])     # add many
fruits.insert(0, "first")   # add at a position
fruits.remove("date")       # remove by value
last = fruits.pop()         # remove and return the last item
```

* **Ordered, mutable, duplicates allowed**, and may hold mixed types.
* Slicing, `len()`, `in`, and `max()`/`min()`/`sum()` all work.
* `.sort()` and `.reverse()` change in place and return **`None`**; `sorted()`
  and `reversed()` return new objects.
* **Aliasing trap** — `b = a` makes a second *reference*, not a copy. Use
  `a.copy()`, `a[:]`, or `copy.deepcopy()` for nested data.
* Comprehensions are the idiomatic way to transform or filter.

```python
squares = [n * n for n in range(5)]           # [0, 1, 4, 16]
evens   = [n for n in numbers if n % 2 == 0]  # filter
```

---

## Tuples (tuple)

**File:** [`tuple.py`](tuple.py)

An ordered, **immutable** sequence in round parentheses — a frozen list.

```python
point = (3, 5)
rgb = (255, 128, 0)
```

* Cannot be changed after creation: no `append`, no `remove`, no index
  assignment. Build a new tuple instead.
* **Hashable**, so — unlike a list — it can be a dict key or a set member.
  This is why `(row, col)` works as a grid key.
* Slightly faster and smaller than a list.
* **Single-item tuples need a trailing comma**: `(5,)` is a tuple, `(5)` is
  just the int `5`.

```python
x, y = (10, 20)        # unpacking
a, b = b, a            # swap without a temp variable
rgb = 255, 128, 0      # parentheses optional when returning
```

Use a tuple for data that should not change, and as a compound dict key.

---

## Dictionaries (dict)

**File:** [`dictionary.py`](dictionary.py)

A key–value mapping in curly braces. You look data up *by key*, not by
position.

```python
person = {"name": "Ada", "age": 36}
person["city"] = "London"        # add or overwrite
person.update({"age": 37})       # merge several
age = person.pop("age")          # remove and return
```

* **Keys must be unique and hashable** — strings, numbers, and tuples work;
  lists and dicts raise `TypeError`. Values can be anything.
* **Insertion order is preserved** (Python 3.7+), so iteration is predictable.
* Very fast lookup, insert, and delete (average O(1)).

```python
person.get("email")           # None instead of raising KeyError
person.get("email", "n/a")    # supply your own default

for name, score in scores.items():   # loop over key AND value
    ...

squares = {n: n * n for n in range(4)}   # dict comprehension
```

Nested dicts model structured data — and `.get()` chains safely where a key
might be missing:

```python
settings["user"]["lang"]                        # direct
settings.get("nope", {}).get("lang", "unknown")  # safe
```

---

## Sets (set)

**File:** [`set.py`](set.py)

An **unordered** collection holding each item at most once, with very fast
membership tests.

```python
colours = {"red", "green", "blue"}
{"a", "a", "b"}      # -> {'a', 'b'}  duplicates vanish
```

* **Unique and unordered** — there is no index and no guaranteed order, so
  `s[0]` raises `TypeError` and iteration order can vary between runs.
  Use `sorted(s)` when order matters.
* **Mutable**, but the items inside must be hashable.
* Great for de-duplication and fast `x in my_set` checks.

```python
list(set([1, 2, 2, 3]))        # [1, 2, 3] — deduplicate
sorted(set([3, 1, 2]))         # [1, 2, 3] — deduplicate, stable order

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
a | b        # union          everything in either
a & b        # intersection   common to both
a - b        # difference     in a, not in b
a ^ b        # symmetric      in either, not both
```

> `{}` is an **empty dict**, not an empty set. Use `set()`.

---

## Choosing the right type

A quick reference for the decision you will actually face:

| You need | Use | Why |
|---|---|---|
| A yes/no answer | `bool` | Reads clearly, no magic numbers |
| A count or ID | `int` | Exact, no overflow |
| A measurement | `float` | Natural for decimals |
| A number with √−1 | `complex` | Built in, no imports |
| Text | `str` | Immutable and hashable |
| An ordered, changing collection | `list` | The default |
| Ordered data that must not change | `tuple` | Immutable, hashable |
| Named records | `dict` | Key–value lookup |
| Uniqueness or fast membership | `set` | Duplicates collapse |
| "No value" | `None` | The absence of data |

Two rules that resolve most remaining doubt:

1. **Reach for `list` by default**, then switch to something else when you have
   a reason (must be hashable, must not change, order is irrelevant).
2. **Match the data, not the operations.** If you find yourself writing
   `item[0]`, `item[1]`, and `item[2]` on something that has a *name*, it
   probably wants to be a `dict` or a small class instead.

---

## Related notes

### A stray section

The original `intro.md` carried a "Key Principles" section describing type
hiding, MRO overriding, and multiple inheritance, ending with a `class D(A, B,
C)` example. That material is about object-oriented Python rather than data
types, so it does not fit this guide. It has been moved out of the
documentation above rather than deleted — the code is preserved below verbatim
for reference.

> **This snippet does not run as written.** `main()` calls `D("hello")`, but `D`
> inherits from `A`, `B`, and `C`, none of which define `__init__`, so `D()`
> takes no arguments:
>
> ```
> TypeError: D() takes no arguments
> ```
>
> It is kept unaltered so the original text is not lost. The `h` method is also
> odd: it is defined without `self`, so it is really a plain function attached
> to the class rather than a bound method.

```python
class A:
    def f(self):
        return "A"

class B:
    def g(self, x):
        return "B"

class C:
    pass

class D(A, B, C):
    def h(x):  # Returns a new class with both A and B methods
        return f"{C.__name__}(x) = {A.f() if x else 'None'} ({B.g(x)})"

def main():
    obj1 = D()
    obj2 = D("hello")
    print(obj1, "---", obj2)

if __name__ == "__main__":
    main()
```

### File naming caveat

Python resolves imports by searching `sys.path`, which includes the directory of
the script being run. A file named after a standard-library module can
therefore hijack that module.

This originally bit us: [`string.py`](strings.py) was renamed to
[`strings.py`](strings.py) precisely because of it. The failure mode is
confusing — the real error surfaces inside a standard-library file and points
nowhere near your code:

```
File ".../logging/__init__.py", line 29, in <module>
  from string import Template
File ".../console/ejercicios/string.py", line 38, in <module>
  nombre = input("Escribe tu nombre: ")
EOFError: EOF when reading a line
```

A stdlib `import string` loaded our exercise and ran it from top to bottom,
which then tried to prompt for input.

The current state of this folder:

| This folder | Standard library |
|---|---|
| `strings.py` | *(plural — no collision)* |
| `list.py` | *(no stdlib module — safe)* |
| `set.py` | *(no stdlib module — safe)* |
| `tuple.py` | *(no stdlib module — safe)* |
| `none.py` | *(no stdlib module — safe)* |

No filename here shadows a standard-library module, so scripts in this folder
are safe to run in place. If you add a file later, prefer a plural or a
distinct name — and be careful with names like `string.py`, `types.py`,
`code.py`, `random.py`, or `json.py`.
