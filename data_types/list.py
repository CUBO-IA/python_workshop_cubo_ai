"""
LIST (list) - Python's ordered, mutable, growable sequence.

What is a list?
---------------
A list is an ordered collection of items stored in square brackets, separated
by commas:

    fruits = ["apple", "banana", "cherry"]

Think of it as a numbered, expandable row of boxes. A list can hold values of
any type -- including other lists -- and it is the default "collection" to
reach for in Python.

How does it work?
-----------------
* ORDERED: items keep their position; `[10, 20] != [20, 10]`.
* MUTABLE: you can add, remove, and replace items after creation.
* INDEXED: positions start at 0; negative indices count from the end.
* DUPLICATES ALLOWED: `[1, 1, 2]` is a perfectly valid list.
* HETEROGENEOUS: `[1, "two", 3.0, True, [5]]` is allowed (though usually
  a list of one consistent type is cleaner).
* Lists are mutable, so they are NOT hashable and cannot be dict keys.
* Nested lists are how you model grids, tables, and matrices.

Run this file:  python3 list.py
"""


# ---------------------------------------------------------------------------
# 1. Creating lists
# ---------------------------------------------------------------------------
# Square brackets, comma-separated.
fruits = ["apple", "banana", "cherry"]
mixed = [1, "two", 3.0, True, None]     # any types allowed
nested = [[1, 2], [3, 4]]                # a list of lists (a 2x2 grid)

print("fruits               ->", fruits)
print("mixed types          ->", mixed)
print("nested list          ->", nested)
print("type(fruits)         ->", type(fruits))          # <class 'list'>
print("isinstance(fruits,list)->", isinstance(fruits, list))

# The empty list -- note: [] not {} (that's a dict) and not () (that's a tuple)
empty = []
print("empty list           ->", empty, " length:", len(empty))

# Important: [] creates a NEW empty list each time. Sharing one is a bug.
a = []
b = []
a.append("oops")
print("\nshared vs separate lists -> b is:", b)  # b stays empty. Good.
# But this IS a bug:
shared = []
alias = shared
alias.append("mutated")
print("aliased list mutated ->", shared)   # shared also changed! Avoid this.


# ---------------------------------------------------------------------------
# 2. Indexing and negative indexing
# ---------------------------------------------------------------------------
items = ["a", "b", "c", "d", "e"]
#  index:   0   1   2   3   4
#  neg:    -5  -4  -3  -2  -1
print("\n--- indexing on ['a','b','c','d','e'] ---")
print("items[0]  (first)   ->", items[0])    # 'a'
print("items[2]            ->", items[2])    # 'c'
print("items[-1] (last)    ->", items[-1])   # 'e'
print("items[-2]           ->", items[-2])   # 'd'
print("len(items)          ->", len(items))  # 5

# Out of range -> IndexError:
# items[10]  -> IndexError: list index out of range


# ---------------------------------------------------------------------------
# 3. Slicing
# ---------------------------------------------------------------------------
# Syntax: items[start : stop : step]  (stop is EXCLUSIVE)
print("\n--- slicing ---")
print("items[1:3]          ->", items[1:3])   # ['b', 'c']
print("items[:2]           ->", items[:2])    # ['a', 'b']
print("items[3:]           ->", items[3:])    # ['d', 'e']
print("items[:]  (copy)    ->", items[:])     # full copy
print("items[::2]          ->", items[::2])   # ['a', 'c', 'e'] every other
print("items[::-1] reverse ->", items[::-1])  # ['e', 'd', 'c', 'b', 'a']
print("items[-2:]          ->", items[-2:])   # ['d', 'e']


# ---------------------------------------------------------------------------
# 4. Adding and removing items
# ---------------------------------------------------------------------------
shopping = ["milk", "bread"]

# append() adds ONE item to the END.
shopping.append("eggs")
print("\nafter append         ->", shopping)

# insert() adds at a specific position.
shopping.insert(0, "butter")
print("after insert(0,...)  ->", shopping)

# extend() adds MANY items (another list).
shopping.extend(["jam", "honey"])
print("after extend([...])  ->", shopping)

# remove() deletes the FIRST matching value.
shopping.remove("bread")
print("after remove('bread')->", shopping)

# pop() removes by index and RETURNS the removed item.
removed = shopping.pop()        # removes the last item by default
print("pop() removed        ->", removed, " now:", shopping)
removed_first = shopping.pop(0) # remove from the front
print("pop(0) removed       ->", removed_first, " now:", shopping)

# clear() empties the list entirely.
temp = [1, 2, 3]
temp.clear()
print("after clear()        ->", temp)


# ---------------------------------------------------------------------------
# 5. Changing and sorting
# ---------------------------------------------------------------------------
# Lists are mutable: you can assign to an index.
numbers = [10, 20, 30]
numbers[1] = 99
print("\nafter numbers[1]=99  ->", numbers)

# sort() sorts IN PLACE and returns None.
scores = [88, 42, 95, 67]
scores.sort()                   # ascending by default
print("after sort()         ->", scores)

scores.sort(reverse=True)       # descending
print("after sort(reverse)  ->", scores)

# sorted() returns a NEW sorted list and leaves the original alone.
original = [3, 1, 2]
new_sorted = sorted(original)
print("\noriginal (unchanged) ->", original)
print("sorted(original)      ->", new_sorted)

# sort by a custom key (e.g. sort by string length):
words = ["pear", "fig", "banana"]
words.sort(key=len)
print("sort by length       ->", words)

# Reverse in place:
letters = [1, 2, 3]
letters.reverse()
print("after reverse()      ->", letters)


# ---------------------------------------------------------------------------
# 6. Other useful list methods
# ---------------------------------------------------------------------------
nums = [1, 2, 2, 3, 2, 4]

print("\n--- other methods ---")
print("len(nums)            ->", len(nums))       # 6
print("nums.count(2)        ->", nums.count(2))   # 3 occurrences
print("2 in nums            ->", 2 in nums)       # True
print("nums.index(3)        ->", nums.index(3))   # position of first 3
print("max(nums)            ->", max(nums))
print("min(nums)            ->", min(nums))
print("sum(nums)            ->", sum(nums))
print("copy = nums[:]       ->", nums[:])         # shallow copy

# Copying correctly: list.copy() or slice, NOT just assigning a new name.
original = [1, 2, 3]
shallow = original.copy()      # independent copy
shallow.append(4)
print("\nafter copy+append: original ->", original, " copy ->", shallow)

# Nested lists need a deep copy (see the note below):
import copy
matrix = [[1, 2], [3, 4]]
deep = copy.deepcopy(matrix)   # fully independent, even inner lists
print("deepcopy of matrix  ->", deep)


# ---------------------------------------------------------------------------
# 7. List comprehensions
# ---------------------------------------------------------------------------
# A list comprehension builds a new list from an expression in a single line.
# It is the Pythonic way to transform or filter a list.
#
#   [expression for item in iterable if condition]
#
# Regular loop:
squares = []
for n in range(5):
    squares.append(n * n)
print("\nloop squares         ->", squares)

# Same thing as a comprehension (cleaner and usually faster):
squares = [n * n for n in range(5)]
print("comprehension squares->", squares)

# Transform: uppercase every word
words = ["hello", "world"]
upper = [w.upper() for w in words]
print("uppercase words      ->", upper)

# Filter: keep only even numbers
numbers = [1, 2, 3, 4, 5, 6]
evens = [n for n in numbers if n % 2 == 0]
print("even numbers         ->", evens)

# Filter + transform together: lengths of long words
long_lengths = [len(w) for w in words if len(w) > 3]
print("lengths of long words->", long_lengths)


# ---------------------------------------------------------------------------
# 8. Nested lists (2D structures)
# ---------------------------------------------------------------------------
# A list of lists is how you store a grid, table, or matrix.
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

print("\n--- nested lists ---")
print("grid                 ->", grid)
print("grid[0]  (row 0)     ->", grid[0])       # [1, 2, 3]
print("grid[1][2] (r1,c2)   ->", grid[1][2])    # 6
print("row lengths          ->", [len(row) for row in grid])  # [3, 3, 3]

# Looping over every element in a 2D list:
total = 0
for row in grid:
    for cell in row:
        total += cell
print("sum of all cells     ->", total)         # 45

# Flatten a 2D list into 1D:
flat = [cell for row in grid for cell in row]
print("flattened grid       ->", flat)


# ---------------------------------------------------------------------------
# 9. Aliasing and copying (a classic Python trap)
# ---------------------------------------------------------------------------
# Assigning a list to a second name does NOT copy it -- both names point to
# the SAME list. To get a real copy use .copy(), slicing [:], or copy.deepcopy.
a = [1, 2, 3]
b = a            # b is an ALIAS of a, not a copy!
b.append(4)
print("\n--- aliasing ---")
print("a (changed too!)    ->", a)
print("b                   ->", b)

c = a.copy()     # now this is an independent copy
c.append(5)
print("a (unchanged)       ->", a)
print("c                   ->", c)

# Rule of thumb: if you did not call .copy()/[:]/deepcopy, it is the same list.


# ---------------------------------------------------------------------------
# 10. Tuples vs lists (when to use which)
# ---------------------------------------------------------------------------
# Use a list when the contents will change. Use a tuple when they should not
# (see tuple.py). A tuple is also slightly faster and can be a dict key.
mutable = [1, 2, 3]     # list: can change
immutable = (1, 2, 3)   # tuple: cannot change
print("\n--- list vs tuple ---")
print("type(mutable)        ->", type(mutable).__name__)
print("type(immutable)      ->", type(immutable).__name__)

# A tuple is hashable, so it can be a dict key. A list is NOT hashable.
try:
    hash(mutable)
    print("list as dict key works -> True")
except TypeError as e:
    print("list as dict key FAILS ->", e)   # lists are unhashable

hash(immutable)
print("tuple as dict key works -> True")


# ---------------------------------------------------------------------------
# 11. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The list errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: append in a loop over the SAME list -> confusing behaviour
    # or an infinite loop, because the list grows as you iterate.
    # Instead loop over range(len(x)) or build a new list.
    # We show the safe version here.
    nums = [1, 2, 3]
    result = [x * 2 for x in nums]   # safe: builds a NEW list
    print("  1. loop over a new list, not one you're appending to ->", result)

    # MISTAKE 2: modifying a list while iterating it skips elements.
    # Safe fix: iterate over a copy: for x in list[:]
    # We demonstrate the safe pattern:
    data = [1, 2, 3, 4, 5]
    removed = [x for x in data if x % 2 == 1]   # keep odds
    print("  2. to remove while iterating, build a new list ->", removed)

    # MISTAKE 3: using + to combine lists when you meant to copy.
    # a = b + []  is a copy; a = b  is an alias.
    base = [1]
    combined = base + [2]    # new list
    print("  3. base + [2] makes a new list ->", combined, "base ->", base)

    # MISTAKE 4: .sort() and .reverse() return None (they change in place).
    # x = [3,1,2].sort()  -> x is None, not a sorted list!
    # Use sorted(x) if you want a new list.
    x = [3, 1, 2]
    y = sorted(x)            # correct: returns a new sorted list
    print("  4. .sort() returns None; sorted() returns a list ->", y)

    # MISTAKE 5: forgetting that strings and lists are different.
    # "abc" + "def" -> "abcdef"  (strings join)
    # ["a"] + ["b"] -> ["a","b"] (lists combine)
    print("  5. str+str concatenates; list+list combines:",
          ["a"] + ["b"])


# ---------------------------------------------------------------------------
# 12. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with lists:
      1. Use list comprehensions for simple transform/filter steps.
      2. Use .append() to add one item, .extend() to add many -- do not
         use append() in a loop for performance.
      3. Remember .sort() and .reverse() modify in place and return None;
         use sorted() / reversed() when you want a new list.
      4. Use a comprehension (`[x for x in y]`) to copy a list, or
         y[:], or y.copy(). A plain assignment creates an alias.
      5. Prefer `if items:` over `if len(items) > 0:` to test emptiness.
      6. Use .index() for position and `in` for membership; do not loop
         manually.
      7. Choose a list over a tuple unless you specifically need immutability
         or hashability.
    """
    print("--- best practices (see docstring) ---")
    print("empty check:", bool([]), bool([1]))   # False, True


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll list examples finished.")


if __name__ == "__main__":
    main()
