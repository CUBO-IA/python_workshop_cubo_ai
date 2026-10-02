"""
TUPLE (tuple) - Python's ordered, IMMUTABLE sequence.

What is a tuple?
----------------
A tuple is an ordered collection of items written in round parentheses:

    point = (3, 5)

A tuple looks like a list but with one huge difference: it CANNOT be changed
after it is created. Once you make a tuple, its items and their order are
locked in. Think of it as a list carved out of stone.

How does it work?
-----------------
* ORDERED and INDEXED, just like a list.
* IMMUTABLE: no append, no remove, no assignment to an index.
* DUPLICATES ALLOWED, just like a list.
* HASHABLE (if all its items are hashable), so it CAN be a dict key or a
  set member -- unlike a list.
* SINGLE-ITEM tuples need a trailing comma: `(5,)` not `(5)`. Without the
  comma, `(5)` is just the integer 5 in parentheses.
* Tuples are slightly faster and use less memory than lists.
* Use a tuple for fixed data: coordinates, RGB colours, database rows,
  function return values, and dictionary keys.

Run this file:  python3 tuple.py
"""


# ---------------------------------------------------------------------------
# 1. Creating tuples
# ---------------------------------------------------------------------------
# Parentheses around comma-separated values.
point = (3, 5)
pair = "hello", "world"        # the parentheses are optional here
empty = ()
single = (42,)
colors = ("red", "green", "blue")

print("point                ->", point)             # (3, 5)
print("pair (no parens)     ->", pair)              # ('hello', 'world')
print("empty tuple          ->", empty, " length:", len(empty))
print("single (trailing ,)  ->", single, " type:", type(single).__name__)  # tuple
print("colors               ->", colors)
print("type(point)          ->", type(point))       # <class 'tuple'>

# THE MOST COMMON MISTAKE -- the trailing comma:
print("\n--- the trailing comma trap ---")
print("type((5))            ->", type((5)).__name__)          # int!  not tuple
print("type((5,))           ->", type((5,)).__name__)         # tuple (correct)
print("(5) == 5             ->", (5) == 5)                    # True
print("(5,) == 5            ->", (5,) == 5)                   # False


# ---------------------------------------------------------------------------
# 2. Indexing and slicing (same as lists)
# ---------------------------------------------------------------------------
colors = ("red", "green", "blue", "yellow")
#   index:   0      1       2       3
print("\n--- indexing on colours ---")
print("colors[0]            ->", colors[0])     # 'red'
print("colors[-1]           ->", colors[-1])    # 'yellow'
print("len(colors)          ->", len(colors))   # 4
print("colors[1:3]          ->", colors[1:3])   # ('green', 'blue')
print("colors[::-1]         ->", colors[::-1])  # reversed tuple
print("colors[:]  (copy)    ->", colors[:])     # a new tuple


# ---------------------------------------------------------------------------
# 3. Immutability -- what you CANNOT do
# ---------------------------------------------------------------------------
# Every one of these raises TypeError. They are shown commented out so the
# file runs cleanly.
colors = ("red", "green", "blue")
#
# colors[0] = "yellow"   -> TypeError: 'tuple' object does not support item assignment
# colors.append("pink")  -> AttributeError: 'tuple' object has no attribute 'append'
# colors.remove("red")   -> AttributeError: 'tuple' object has no attribute 'remove'
# colors.sort()          -> AttributeError: 'tuple' object has no attribute 'sort'
# del colors[0]          -> TypeError: 'tuple' object doesn't support item deletion
#
print("\n--- immutability ---")
print("tuples have no append/remove/sort methods at all")
print("hasattr(colors,'append') ->", hasattr(colors, "append"))  # False

# To "change" a tuple you build a brand new one:
updated = ("yellow",) + colors[1:]
print("rebuilt tuple         ->", updated)   # ('yellow', 'green', 'blue')

# Tuples support only these sequence methods (no mutating ones):
print("tuple methods        ->", [m for m in dir(colors)
                                  if not m.startswith('_')][:6], "...")


# ---------------------------------------------------------------------------
# 4. Tuples are hashable (unlike lists)
# ---------------------------------------------------------------------------
# Because a tuple cannot change, Python can compute a stable hash for it.
# That makes tuples usable as dictionary keys and set members.
location = (3, 5)
locations = {location: "corner of the room"}
print("\n--- hashable ---")
print("dict keyed by tuple  ->", locations[(3, 5)])

unique = {(1, 2), (1, 2), (3, 4)}   # duplicates collapse
print("duplicates collapse  ->", unique)   # {(1, 2), (3, 4)}

# This is a very common pattern: a tuple key of (row, col) indexing a grid.
# A nested LIST needs two separate indexes: grid[r][c].
grid = [[1, 2], [3, 4]]
r, c = 0, 1
print("grid[r][c]           ->", grid[r][c])      # 2

# If you store the grid as a DICT keyed by (row, col) tuples, then a single
# tuple lookup replaces both indexes -- and the position stays meaningful.
grid_dict = {(0, 0): 1, (0, 1): 2, (1, 0): 3, (1, 1): 4}
print("grid_dict[(r, c)]     ->", grid_dict[(r, c)])   # 2
position = (0, 1)
print("named via tuple key  ->", grid_dict[position])  # 2


# ---------------------------------------------------------------------------
# 5. Unpacking -- the best feature of tuples
# ---------------------------------------------------------------------------
# You can take a tuple apart into separate variables in one line.
point = (10, 20)
x, y = point
print("\n--- unpacking ---")
print("x, y = (10, 20)      ->", (x, y))   # (10, 20)

# Swapping variables becomes trivial with tuples (no temp variable needed):
a, b = 1, 2
a, b = b, a
print("swapped a, b         ->", (a, b))   # (2, 1)

# Loop over tuples of data -- very common and very readable:
points = [(1, 2), (3, 4), (5, 6)]
for px, py in points:
    print(f"  point: x={px}, y={py}")

# Unpacking with a variable-length catch-all using *:
first, *middle, last = [1, 2, 3, 4, 5]
print("\nfirst, *middle, last ->", (first, middle, last))  # (1, [2,3,4], 5)


# ---------------------------------------------------------------------------
# 6. Functions and tuples
# ---------------------------------------------------------------------------
# Functions can RETURN a tuple, which is a neat way to return several values
# at once. This is cleaner than returning a list or a dict for small results.

def min_and_max(numbers):
    """Return the smallest and largest values as a tuple."""
    return min(numbers), max(numbers)   # no parentheses needed

lo, hi = min_and_max([4, 9, 2, 7])
print("\n--- returning tuples ---")
print("min_and_max result   ->", min_and_max([4, 9, 2, 7]))
print("lo, hi               ->", (lo, hi))   # 2, 9

# divmod() is a built-in that returns a tuple too:
print("divmod(17, 5)        ->", divmod(17, 5))   # (3, 2)


# ---------------------------------------------------------------------------
# 7. Checking membership and other basics
# ---------------------------------------------------------------------------
colors = ("red", "green", "blue")
print("\n--- basics ---")
print("'red' in colors      ->", "red" in colors)     # True
print("'pink' in colors     ->", "pink" in colors)    # False
print("colors.index('blue') ->", colors.index("blue"))# 2
print("colors.count('red')  ->", colors.count("red")) # 1
print("max(colors)          ->", max(colors))         # 'red' (alphabetical)
print("min(colors)          ->", min(colors))         # 'blue'
print("list(colors)         ->", list(colors))        # tuple -> list
print("sorted(colors)       ->", sorted(colors))      # returns a list


# ---------------------------------------------------------------------------
# 8. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The tuple errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: forgetting the trailing comma in a single-item tuple.
    # (5) is the int 5, NOT a tuple. (5,) is a tuple.
    print("  1. (5) is an", type((5)).__name__, "-- (5,) is a",
          type((5,)).__name__)

    # MISTAKE 2: trying to modify a tuple. Build a new one instead.
    t = (1, 2, 3)
    # t[0] = 99   -> TypeError
    new_t = (99,) + t[1:]
    print("  2. tuples are immutable; build a new one ->", new_t)

    # MISTAKE 3: confusing list append with tuple concatenation.
    lst = [1, 2]
    lst.append(3)          # lists: append
    tpl = (1, 2)
    tpl = tpl + (3,)       # tuples: add a new tuple
    print("  3. list.append(3) ->", lst, " tuple + (3,) ->", tpl)

    # MISTAKE 4: assuming a tuple is a "frozen list" you can edit later.
    # If you need to change it, use a list instead.

    # MISTAKE 5: `in` on a large tuple is O(n); for many membership checks
    # a set is faster. But for small tuples a tuple is fine.


# ---------------------------------------------------------------------------
# 9. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with tuples:
      1. Use a tuple for data that should not change (coordinates, constants,
         dict keys, function returns). Use a list when you will modify it.
      2. Remember the trailing comma for single-item tuples: (5,).
      3. Prefer unpacking (x, y = point) over indexing (x = point[0]).
      4. Use tuples as dictionary keys when you need a compound key
         (e.g. (row, col)).
      5. Return multiple values from a function as a tuple -- it is concise
         and idiomatic.
      6. Convert with tuple(list) or list(tuple) when you need to switch.
      7. Tuples are hashable only if all their items are hashable (a tuple
         containing a list is NOT hashable).
    """
    print("--- best practices (see docstring) ---")
    print("unpack a coordinate:", (lambda p: p[0] + p[1])((3, 4)))  # 7


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll tuple examples finished.")


if __name__ == "__main__":
    main()
